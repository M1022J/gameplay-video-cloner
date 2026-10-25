#!/usr/bin/env python3
"""Provider-neutral adapter interface for image and video generation models (ybuild-ai/ai-game-art-pipeline-skill)."""
from dataclasses import dataclass
from typing import Optional

@dataclass
class AssetRequest:
    job_type: str
    prompt: str
    width: int = 512
    height: int = 512
    chroma_bg: str = "#FF00FF"
    reference_image: Optional[str] = None

class ArtProviderStub:
    def generate_image(self, req: AssetRequest) -> bytes:
        raise NotImplementedError("Wire to image_gen:generate_image or HTTP adapter.")
    def generate_video(self, req: AssetRequest, duration_sec: float = 3.0) -> bytes:
        raise NotImplementedError("Wire to async video provider adapter.")
