import importlib.util
import unittest
from pathlib import Path


FIXTURE = Path(__file__).parent / "fixtures" / "vulnerable_app" / "app.py"
SPEC = importlib.util.spec_from_file_location("synthetic_vulnerable_app", FIXTURE)
APP = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(APP)


class RecordingDatabase:
    def __init__(self):
        self.calls = []

    def execute(self, query, parameters):
        self.calls.append((query, parameters))


class SyntheticDemoTests(unittest.TestCase):
    def test_authorized_update_is_length_limited_and_tenant_scoped(self):
        database = RecordingDatabase()

        result = APP.update_note(
            {"id": "user-1", "tenant_id": "tenant-a"},
            "tenant-a",
            "note-7",
            {"body": "A valid note"},
            database,
        )

        self.assertEqual(result, {"updated": "note-7", "tenant": "tenant-a"})
        self.assertEqual(len(database.calls), 1)
        query, parameters = database.calls[0]
        self.assertIn("WHERE id = %s AND tenant_id = %s", query)
        self.assertEqual(parameters, ("A valid note", "note-7", "tenant-a"))

    def test_actor_from_another_tenant_is_rejected_without_database_write(self):
        database = RecordingDatabase()

        with self.assertRaises(PermissionError):
            APP.update_note(
                {"id": "user-2", "tenant_id": "tenant-b"},
                "tenant-a",
                "note-7",
                {"body": "Attempted cross-tenant update"},
                database,
            )

        self.assertEqual(database.calls, [])

    def test_oversized_note_is_rejected_without_database_write(self):
        database = RecordingDatabase()

        with self.assertRaises(ValueError):
            APP.update_note(
                {"id": "user-1", "tenant_id": "tenant-a"},
                "tenant-a",
                "note-7",
                {"body": "x" * 2049},
                database,
            )

        self.assertEqual(database.calls, [])

    def test_note_at_2048_character_limit_is_accepted(self):
        database = RecordingDatabase()
        body = "x" * 2048

        APP.update_note(
            {"id": "user-1", "tenant_id": "tenant-a"},
            "tenant-a",
            "note-7",
            {"body": body},
            database,
        )

        self.assertEqual(database.calls[0][1], (body, "note-7", "tenant-a"))

    def test_non_string_note_body_is_rejected_without_database_write(self):
        database = RecordingDatabase()

        with self.assertRaises(ValueError):
            APP.update_note(
                {"id": "user-1", "tenant_id": "tenant-a"},
                "tenant-a",
                "note-7",
                {"body": ["not", "a", "string"]},
                database,
            )

        self.assertEqual(database.calls, [])


if __name__ == "__main__":
    unittest.main()
