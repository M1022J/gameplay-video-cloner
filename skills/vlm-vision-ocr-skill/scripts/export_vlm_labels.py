#!/usr/bin/env python3
"""
export_vlm_labels.py
Canonical 0..1000 VLM Coordinate Exporter to YOLO, YOLO-seg, Labelme, COCO, Pascal VOC, and CSV
Source: Autsunset/vision-label-skill (https://github.com/Autsunset/vision-label-skill)

Usage:
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format yolo --out-dir ./labels_out
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format labelme --out-dir ./labels_out
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format coco --out-dir ./labels_out
  python3 export_vlm_labels.py --image <img.png> --ann <img.raw.json> --format csv --out-dir ./labels_out
"""
import os
import csv
import json
import argparse
from pathlib import Path
from PIL import Image


def export_annotations(image_path: str, ann_json_path: str, fmt: str, out_dir: str):
    out_p = Path(out_dir)
    out_p.mkdir(parents=True, exist_ok=True)
    with Image.open(image_path) as im:
        w, h = im.size
    stem = Path(image_path).stem
    raw = json.loads(Path(ann_json_path).read_text(encoding="utf-8"))
    classes = raw.get("classes", [])
    anns = raw.get("annotations", [])

    for a in anns:
        if a["class_name"] not in classes:
            classes.append(a["class_name"])

    if fmt in ("yolo", "yolo-seg"):
        lines = []
        for a in anns:
            cid = classes.index(a["class_name"])
            ymin, xmin, ymax, xmax = a["bbox_1000"]
            if fmt == "yolo":
                cx = ((xmin + xmax) / 2.0) / 1000.0
                cy = ((ymin + ymax) / 2.0) / 1000.0
                bw = (xmax - xmin) / 1000.0
                bh = (ymax - ymin) / 1000.0
                lines.append(f"{cid} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")
            else:
                pts = a.get("polygon_1000", [[xmin, ymin], [xmax, ymin], [xmax, ymax], [xmin, ymax]])
                coord_str = " ".join(f"{px/1000.0:.6f} {py/1000.0:.6f}" for px, py in pts)
                lines.append(f"{cid} {coord_str}")
        out_txt = out_p / f"{stem}.txt"
        out_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")
        (out_p / "classes.txt").write_text("\n".join(classes) + "\n", encoding="utf-8")
        print(f"[export_vlm_labels] Exported {fmt.upper()} ({len(lines)} boxes) -> {out_txt}")

    elif fmt == "labelme":
        shapes = []
        for a in anns:
            ymin, xmin, ymax, xmax = a["bbox_1000"]
            x1, y1 = xmin / 1000.0 * w, ymin / 1000.0 * h
            x2, y2 = xmax / 1000.0 * w, ymax / 1000.0 * h
            shapes.append({
                "label": a["class_name"],
                "points": [[round(x1, 2), round(y1, 2)], [round(x2, 2), round(y2, 2)]],
                "group_id": None,
                "description": a.get("ocr_text", ""),
                "shape_type": "rectangle",
                "flags": {},
            })
        lm_doc = {"version": "5.4.1", "flags": {}, "shapes": shapes, "imagePath": Path(image_path).name, "imageData": None, "imageHeight": h, "imageWidth": w}
        out_f = out_p / f"{stem}.labelme.json"
        out_f.write_text(json.dumps(lm_doc, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[export_vlm_labels] Exported Labelme JSON -> {out_f}")

    elif fmt == "coco":
        coco = {
            "images": [{"id": 1, "file_name": Path(image_path).name, "width": w, "height": h}],
            "categories": [{"id": i + 1, "name": c} for i, c in enumerate(classes)],
            "annotations": [],
        }
        for idx, a in enumerate(anns, start=1):
            cid = classes.index(a["class_name"]) + 1
            ymin, xmin, ymax, xmax = a["bbox_1000"]
            bx = round(xmin / 1000.0 * w, 2)
            by = round(ymin / 1000.0 * h, 2)
            bw = round((xmax - xmin) / 1000.0 * w, 2)
            bh = round((ymax - ymin) / 1000.0 * h, 2)
            coco["annotations"].append({"id": idx, "image_id": 1, "category_id": cid, "bbox": [bx, by, bw, bh], "area": round(bw * bh, 2), "iscrowd": 0})
        out_f = out_p / f"{stem}.coco.json"
        out_f.write_text(json.dumps(coco, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"[export_vlm_labels] Exported COCO JSON -> {out_f}")

    elif fmt == "csv":
        out_f = out_p / f"{stem}.labels.csv"
        with open(out_f, "w", newline="", encoding="utf-8") as fp:
            writer = csv.writer(fp)
            writer.writerow(["som_id", "class_name", "confidence", "ocr_text", "xmin_px", "ymin_px", "width_px", "height_px", "sampled_hex"])
            for a in anns:
                bx, by, bw, bh = a["pixel_bbox"]
                writer.writerow([a["som_id"], a["class_name"], a["confidence"], a.get("ocr_text", ""), bx, by, bw, bh, a.get("sampled_median_hex", "")])
        print(f"[export_vlm_labels] Exported CSV -> {out_f}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export canonical 0..1000 VLM annotations to YOLO, Labelme, COCO, or CSV.")
    parser.add_argument("--image", required=True)
    parser.add_argument("--ann", required=True)
    parser.add_argument("--format", default="yolo", choices=["yolo", "yolo-seg", "labelme", "coco", "csv"])
    parser.add_argument("--out-dir", default="./labels_out")
    args = parser.parse_args()
    export_annotations(args.image, args.ann, args.format, args.out_dir)
