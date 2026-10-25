# Swarm Orchestration, Teammate Inboxes & DAG Task Queues (`kieranklaassen/orchestrating-swarms`)

- **DAG Auto-Unblocking (`blockedBy`)**: Task #1 locks `Constants` and `EventBus`; upon completion it automatically unblocks parallel Tasks #2 (`Physics`), #3 (`2D/3D Skeletal Rig & Juice`), and #4 (`HUD & Audio Synth`).
