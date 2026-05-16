import unittest

from tier2 import normalize_extension


class TestNormalization(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(normalize_extension("Zba"), "zba")

    def test_rv_prefix(self):
        self.assertEqual(normalize_extension("RV64M"), "m")

    def test_underscore(self):
        self.assertEqual(normalize_extension("rv_zicsr"), "zicsr")


class TestCrossReference(unittest.TestCase):
    def test_set_operations(self):

        json_ext = {"m", "a", "f", "zba"}
        manual_ext = {"m", "a", "d", "zba"}

        matched = json_ext & manual_ext
        json_only = json_ext - manual_ext
        manual_only = manual_ext - json_ext

        self.assertEqual(matched, {"m", "a", "zba"})
        self.assertEqual(json_only, {"f"})
        self.assertEqual(manual_only, {"d"})


if __name__ == "__main__":
    unittest.main()
