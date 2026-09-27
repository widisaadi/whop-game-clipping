"""Timing and source-selection regressions; no media encoding or external services."""
import json
import unittest

from render_retention import ROOT, check_picture, validate, workspace_path


class EditValidationTests(unittest.TestCase):
    def setUp(self):
        self.edit = json.loads((ROOT / "campaigns/how_to_fisch/edits/09_fish_fight_back.json").read_text())
        self.catalog = json.loads(workspace_path(self.edit["catalog"]).read_text())
        self.probes = {entry["src"]: {"duration": 30} for entry in self.catalog.values()}
        self.probes[self.edit["voice"]] = {"duration": 27.4}

    def test_remaps_reordered_voice_without_timeline_drift(self):
        plan = validate(self.edit, self.catalog, self.probes)
        self.assertEqual(plan["frames"], 585)
        self.assertEqual(plan["duration"], 19.5)
        self.assertEqual(plan["cues"][-3][0], 16.46)
        self.assertEqual(plan["cues"][-1][1], 19.5)

    def test_rejects_encoded_frame_drift_and_wrong_fit_dimensions(self):
        plan = validate(self.edit, self.catalog, self.probes)
        probe = {"duration": 19.5, "video": {"fps": 30, "nb_frames": 585, "width": 1080, "height": 1920}}
        check_picture(probe, plan, 1080, 1920)
        probe["video"]["nb_frames"] = 588
        with self.assertRaisesRegex(ValueError, "frame count"):
            check_picture(probe, plan, 1080, 1920)
        probe["video"].update(nb_frames=585, width=760, height=1350)
        with self.assertRaisesRegex(ValueError, "dimensions"):
            check_picture(probe, plan, 1080, 1920)

    def test_cannot_label_selling_clip_as_boss_fight(self):
        self.edit["shots"][4]["clip"] = "35"
        with self.assertRaisesRegex(ValueError, "does not support"):
            validate(self.edit, self.catalog, self.probes)

    def test_rejects_source_that_ends_before_cut(self):
        self.probes[self.catalog["25"]["src"]]["duration"] = 2
        with self.assertRaisesRegex(ValueError, "beyond"):
            validate(self.edit, self.catalog, self.probes)

    def test_rejects_one_frame_drift(self):
        self.edit["shots"][0]["frames"] += 1
        with self.assertRaisesRegex(ValueError, "duration mismatch"):
            validate(self.edit, self.catalog, self.probes)

    def test_rejects_overlapping_captions(self):
        self.edit["voice_segments"][0]["cues"][1][0] = 1.8
        with self.assertRaisesRegex(ValueError, "overlaps"):
            validate(self.edit, self.catalog, self.probes)

    def test_rejects_nonfinite_time(self):
        self.edit["voice_segments"][0]["out"] = float("nan")
        with self.assertRaisesRegex(ValueError, "finite"):
            validate(self.edit, self.catalog, self.probes)

    def test_rejects_unreviewed_footage(self):
        self.catalog["32"]["reviewed"] = False
        with self.assertRaisesRegex(ValueError, "review"):
            validate(self.edit, self.catalog, self.probes)

    def test_rejects_paths_outside_workspace(self):
        with self.assertRaisesRegex(ValueError, "inside"):
            workspace_path("../outside.mp4")


if __name__ == "__main__":
    unittest.main()
