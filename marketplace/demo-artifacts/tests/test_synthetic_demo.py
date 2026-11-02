import unittest
from types import SimpleNamespace
from unittest.mock import Mock

from fixtures.vulnerable_app.app import update_note


class UpdateNoteTests(unittest.TestCase):
    def setUp(self):
        self.actor = SimpleNamespace(tenant_id="tenant-a")
        self.database = Mock()

    def test_updates_note_for_matching_tenant(self):
        result = update_note(
            self.actor,
            "tenant-a",
            17,
            {"body": "A note"},
            self.database,
        )

        query, parameters = self.database.execute.call_args.args
        self.assertIn("WHERE id = %s AND tenant_id = %s", query)
        self.assertEqual(parameters, ("A note", 17, "tenant-a"))
        self.assertEqual(result, {"updated": 17, "tenant": "tenant-a"})

    def test_rejects_actor_from_another_tenant(self):
        with self.assertRaises(PermissionError):
            update_note(
                self.actor,
                "tenant-b",
                17,
                {"body": "A note"},
                self.database,
            )

        self.database.execute.assert_not_called()

    def test_rejects_non_string_body(self):
        for body in (None, 42, ["not", "a", "string"]):
            with self.subTest(body=body):
                with self.assertRaises(ValueError):
                    update_note(
                        self.actor,
                        "tenant-a",
                        17,
                        {"body": body},
                        self.database,
                    )

        self.database.execute.assert_not_called()

    def test_rejects_body_over_2048_characters(self):
        with self.assertRaises(ValueError):
            update_note(
                self.actor,
                "tenant-a",
                17,
                {"body": "x" * 2049},
                self.database,
            )

        self.database.execute.assert_not_called()

    def test_accepts_body_of_exactly_2048_characters(self):
        body = "x" * 2048
        update_note(
            self.actor,
            "tenant-a",
            17,
            {"body": body},
            self.database,
        )

        self.database.execute.assert_called_once_with(
            "UPDATE notes SET body = %s WHERE id = %s AND tenant_id = %s",
            (body, 17, "tenant-a"),
        )


if __name__ == "__main__":
    unittest.main()
