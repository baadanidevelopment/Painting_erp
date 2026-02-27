from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from pathlib import Path
from typing import Dict, List


DEFAULT_STAGES = [
    "concept",
    "sketch",
    "underpainting",
    "base_colors",
    "details",
    "varnish",
]


@dataclass
class Painting:
    title: str
    artist: str
    stages: Dict[str, bool] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.stages:
            self.stages = {stage: False for stage in DEFAULT_STAGES}

    @property
    def percent_complete(self) -> float:
        total = len(self.stages)
        done = sum(1 for complete in self.stages.values() if complete)
        return (done / total) * 100 if total else 0.0


class PaintingProgressTracker:
    def __init__(self, storage_path: str | Path = "paintings.json") -> None:
        self.storage_path = Path(storage_path)
        self.paintings: Dict[str, Painting] = {}
        self._load()

    def add_painting(self, title: str, artist: str) -> None:
        key = title.strip().lower()
        if key in self.paintings:
            raise ValueError(f"Painting '{title}' already exists")
        self.paintings[key] = Painting(title=title.strip(), artist=artist.strip())
        self._save()

    def complete_stage(self, title: str, stage: str) -> None:
        painting = self._get(title)
        stage_key = stage.strip().lower()
        if stage_key not in painting.stages:
            raise ValueError(f"Unknown stage '{stage}'")
        painting.stages[stage_key] = True
        self._save()

    def add_note(self, title: str, note: str) -> None:
        painting = self._get(title)
        painting.notes.append(note.strip())
        self._save()

    def progress_report(self) -> List[dict]:
        report = []
        for painting in self.paintings.values():
            report.append(
                {
                    "title": painting.title,
                    "artist": painting.artist,
                    "complete": round(painting.percent_complete, 1),
                    "stages": painting.stages,
                    "notes": painting.notes,
                }
            )
        return sorted(report, key=lambda p: p["title"].lower())

    def _get(self, title: str) -> Painting:
        key = title.strip().lower()
        if key not in self.paintings:
            raise ValueError(f"Painting '{title}' not found")
        return self.paintings[key]

    def _load(self) -> None:
        if not self.storage_path.exists():
            return
        data = json.loads(self.storage_path.read_text())
        self.paintings = {
            key: Painting(**value)
            for key, value in data.items()
        }

    def _save(self) -> None:
        payload = {key: asdict(painting) for key, painting in self.paintings.items()}
        self.storage_path.write_text(json.dumps(payload, indent=2))


if __name__ == "__main__":
    tracker = PaintingProgressTracker()
    if not tracker.paintings:
        tracker.add_painting("Sunset Over Harbor", "A. Rivera")
        tracker.complete_stage("Sunset Over Harbor", "concept")
        tracker.complete_stage("Sunset Over Harbor", "sketch")
        tracker.add_note("Sunset Over Harbor", "Finalize sky gradient in next session.")
    print(json.dumps(tracker.progress_report(), indent=2))
