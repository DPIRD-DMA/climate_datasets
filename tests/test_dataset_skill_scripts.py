import json
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
ADD_SCRIPT = REPO_ROOT / ".agents/skills/add-dataset/scripts/add_dataset.py"
UPDATE_SCRIPT = REPO_ROOT / ".agents/skills/update-dataset/scripts/update_dataset.py"


def dataset(name: str = "Alpha") -> dict[str, str]:
    return {
        "name": name,
        "category": "Station observations",
        "resolution": "1 km",
        "format": "NetCDF",
        "variables": "Rainfall",
        "method": "Observed",
        "access_conditions": "Free",
        "temporal_coverage": "2000-present",
        "spatial_domain": "Australia",
        "update_frequency": "Daily",
        "license": "CC BY 4.0",
        "provider_contact": "",
        "source_url": "https://example.com/data",
    }


class DatasetSkillScriptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.data_path = Path(self.temp_dir.name) / "datasets.json"
        self.registry = {"metadata": {"version": 1}, "datasets": [dataset()]}
        self.data_path.write_text(json.dumps(self.registry), encoding="utf-8")

    def run_script(self, script: Path, *args: str, input_value: dict) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, str(script), "--data-path", str(self.data_path), *args],
            input=json.dumps(input_value),
            text=True,
            capture_output=True,
            check=False,
        )

    def read_registry(self) -> dict:
        return json.loads(self.data_path.read_text(encoding="utf-8"))

    def test_add_preserves_top_level_keys(self) -> None:
        self.data_path.chmod(0o640)
        result = self.run_script(ADD_SCRIPT, input_value=dataset("Beta"))
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = self.read_registry()
        self.assertEqual(saved["metadata"], {"version": 1})
        self.assertEqual([item["name"] for item in saved["datasets"]], ["Alpha", "Beta"])
        self.assertEqual(stat.S_IMODE(self.data_path.stat().st_mode), 0o640)

    def test_add_dry_run_does_not_write(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(ADD_SCRIPT, "--dry-run", input_value=dataset("Beta"))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_add_rejects_case_insensitive_duplicate(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(ADD_SCRIPT, input_value=dataset("alpha"))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_update_patch_preserves_top_level_keys(self) -> None:
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "alpha",
            input_value={"access_conditions": "Registration"},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = self.read_registry()
        self.assertEqual(saved["metadata"], {"version": 1})
        self.assertEqual(saved["datasets"][0]["access_conditions"], "Registration")

    def test_replace_rejects_incomplete_object_without_writing(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "Alpha",
            "--replace",
            input_value={"name": "Alpha"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Missing required fields", result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_update_rejects_unknown_field_without_writing(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "Alpha",
            input_value={"typo_field": "value"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Unknown fields", result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_fuzzy_update_requires_explicit_selection(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "Alph",
            input_value={"access_conditions": "Registration"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Re-run with --select", result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
