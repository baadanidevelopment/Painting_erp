# Painting Progress Tracker

A lightweight Python tracker for monitoring the completion of painting stages.

## Features
- Add paintings and artist names
- Track stage completion from concept through varnish
- Add free-form notes per painting
- Persist data to a local JSON file
- Generate a sortable progress report

## Quick start

```bash
python3 tracker.py
```

This runs a small demo (first run only) and prints a JSON report.

## Use in your own script

```python
from tracker import PaintingProgressTracker

tracker = PaintingProgressTracker("my_paintings.json")
tracker.add_painting("Golden Field", "R. Kim")
tracker.complete_stage("Golden Field", "concept")
tracker.add_note("Golden Field", "Try palette knife for texture.")

print(tracker.progress_report())
```

## Run tests

```bash
python3 -m unittest -v
```
