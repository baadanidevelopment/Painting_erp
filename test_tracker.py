import tempfile
import unittest
from pathlib import Path

from tracker import PaintingProgressTracker


class TestPaintingProgressTracker(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.path = Path(self.tmp.name) / "store.json"
        self.tracker = PaintingProgressTracker(self.path)

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def test_add_and_complete_stage(self):
        self.tracker.add_painting("Morning Light", "Maya")
        self.tracker.complete_stage("Morning Light", "concept")

        report = self.tracker.progress_report()
        self.assertEqual(len(report), 1)
        self.assertEqual(report[0]["title"], "Morning Light")
        self.assertEqual(report[0]["complete"], 16.7)

    def test_persists_data(self):
        self.tracker.add_painting("Forest Path", "Noah")
        self.tracker.complete_stage("Forest Path", "concept")
        self.tracker.add_note("Forest Path", "Need warmer tones in foreground")

        reloaded = PaintingProgressTracker(self.path)
        report = reloaded.progress_report()[0]
        self.assertEqual(report["artist"], "Noah")
        self.assertEqual(report["notes"], ["Need warmer tones in foreground"])

    def test_duplicate_raises(self):
        self.tracker.add_painting("Ocean View", "Lina")
        with self.assertRaises(ValueError):
            self.tracker.add_painting("Ocean View", "Lina")


if __name__ == "__main__":
    unittest.main()
