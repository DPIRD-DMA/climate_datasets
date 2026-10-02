import json
import stat
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
import registry  # noqa: E402

ADD_SCRIPT = REPO_ROOT / ".agents/skills/add-dataset/scripts/add_dataset.py"
UPDATE_SCRIPT = REPO_ROOT / ".agents/skills/update-dataset/scripts/update_dataset.py"


def dataset(name: str = "Alpha") -> dict:
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
        "access_types": ["Open", "NCI project"],
        "formats": ["NetCDF"],
        "timesteps": ["daily", "monthly"],
        "variable_tags": ["rainfall"],
        "resolution_km": 1,
        "start_year": 2000,
        "end_year": None,
        "domain": "Australia",
        "last_checked": "2026-10-02",
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

    def assert_add_rejected(self, candidate: dict, expected: str) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(ADD_SCRIPT, input_value=candidate)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(expected, result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_add_keeps_list_and_number_types(self) -> None:
        candidate = dataset("Beta")
        candidate.update(resolution_km=4.4, station_count=200, end_year=2100)
        result = self.run_script(ADD_SCRIPT, input_value=candidate)
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = self.read_registry()["datasets"][1]
        self.assertEqual(saved["access_types"], ["Open", "NCI project"])
        self.assertEqual(saved["resolution_km"], 4.4)
        self.assertEqual(saved["station_count"], 200)
        self.assertIsNone(self.read_registry()["datasets"][0]["end_year"])

    def test_add_accepts_null_resolution_for_station_data(self) -> None:
        candidate = dataset("Beta")
        candidate.update(resolution_km=None, station_count=200)
        result = self.run_script(ADD_SCRIPT, "--dry-run", input_value=candidate)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_add_rejects_value_outside_vocabulary(self) -> None:
        candidate = dataset("Beta")
        candidate["access_types"] = ["Public"]
        self.assert_add_rejected(candidate, "access_types has values outside data/vocab.json: Public")

    def test_add_rejects_unknown_domain(self) -> None:
        candidate = dataset("Beta")
        candidate["domain"] = "Mars"
        self.assert_add_rejected(candidate, "domain must be one of")

    def test_add_rejects_string_for_list_field(self) -> None:
        candidate = dataset("Beta")
        candidate["formats"] = "NetCDF"
        self.assert_add_rejected(candidate, "formats must be a non-empty list")

    def test_add_rejects_empty_and_duplicate_lists(self) -> None:
        candidate = dataset("Beta")
        candidate["timesteps"] = []
        self.assert_add_rejected(candidate, "timesteps must be a non-empty list")
        candidate["timesteps"] = ["daily", "daily"]
        self.assert_add_rejected(candidate, "timesteps contains duplicate values")

    def test_add_rejects_bad_numbers(self) -> None:
        for field, value in [
            ("resolution_km", "5"),
            ("resolution_km", True),
            ("resolution_km", 0),
            ("station_count", 1.5),
            ("start_year", None),
            ("start_year", "1990"),
        ]:
            with self.subTest(field=field, value=value):
                candidate = dataset("Beta")
                candidate[field] = value
                self.assert_add_rejected(candidate, field)

    def test_add_rejects_end_year_before_start_year(self) -> None:
        candidate = dataset("Beta")
        candidate.update(start_year=2000, end_year=1999)
        self.assert_add_rejected(candidate, "end_year is earlier than start_year")

    def test_add_rejects_malformed_last_checked(self) -> None:
        for value in ["2026-10-2", "02/10/2026", "20261002", "2026-13-01", "2026-02-30", 20261002]:
            with self.subTest(value=value):
                candidate = dataset("Beta")
                candidate["last_checked"] = value
                self.assert_add_rejected(candidate, "last_checked")

    def test_update_patch_replaces_list_field(self) -> None:
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "Alpha",
            input_value={"timesteps": ["hourly"], "resolution_km": 12.5},
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        saved = self.read_registry()["datasets"][0]
        self.assertEqual(saved["timesteps"], ["hourly"])
        self.assertEqual(saved["resolution_km"], 12.5)

    def test_update_rejects_value_outside_vocabulary_without_writing(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "Alpha",
            input_value={"variable_tags": ["rain"]},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("variable_tags has values outside data/vocab.json", result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)

    def test_update_rejects_wrong_type_without_writing(self) -> None:
        before = self.data_path.read_bytes()
        result = self.run_script(
            UPDATE_SCRIPT,
            "--name",
            "Alpha",
            input_value={"last_checked": "yesterday"},
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("last_checked must be an ISO date", result.stderr)
        self.assertEqual(self.data_path.read_bytes(), before)


class RegistryModuleTests(unittest.TestCase):
    def test_repo_vocabulary_is_valid(self) -> None:
        vocab = registry.load_vocab()
        for key in registry.LIST_FIELDS + registry.ENUM_FIELDS:
            self.assertTrue(vocab[key], key)

    def test_vocabulary_errors_catch_duplicates_and_missing_keys(self) -> None:
        vocab = registry.load_vocab()
        vocab["formats"] = ["NetCDF", "NetCDF"]
        del vocab["domain"]
        errors = registry.vocab_errors(vocab)
        self.assertIn("formats contains duplicate values.", errors)
        self.assertIn("domain must be a non-empty list.", errors)

    def test_every_vocabulary_value_validates(self) -> None:
        vocab = registry.load_vocab()
        for field in registry.LIST_FIELDS:
            self.assertIsNone(registry.check_structured(field, list(vocab[field]), vocab))
        for value in vocab["domain"]:
            self.assertIsNone(registry.check_structured("domain", value, vocab))

    def test_parse_text_converts_types(self) -> None:
        self.assertEqual(registry.parse_text("formats", "NetCDF, GeoTIFF"), ["NetCDF", "GeoTIFF"])
        self.assertEqual(registry.parse_text("resolution_km", "12"), 12)
        self.assertEqual(registry.parse_text("resolution_km", "4.4"), 4.4)
        self.assertIsNone(registry.parse_text("end_year", "null"))
        self.assertEqual(registry.parse_text("name", " Alpha "), "Alpha")
        with self.assertRaises(ValueError):
            registry.parse_text("start_year", "19xx")


if __name__ == "__main__":
    unittest.main()
