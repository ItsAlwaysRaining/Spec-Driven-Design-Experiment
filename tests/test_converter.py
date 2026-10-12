"""Tests for specs/temperature-converter. Each test names the acceptance criterion it covers."""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "src", "converter.py")
sys.path.insert(0, os.path.join(ROOT, "src"))

from converter import convert  # noqa: E402


class TestConvert(unittest.TestCase):
    def test_ac1_100c_is_212f(self):
        self.assertEqual(convert(100, "C"), (212, "F"))

    def test_ac2_0c_is_32f(self):
        self.assertEqual(convert(0, "C"), (32, "F"))

    def test_ac3_32f_is_0c(self):
        self.assertEqual(convert(32, "F"), (0, "C"))

    def test_ac4_minus40f_is_minus40c(self):
        self.assertEqual(convert(-40, "F"), (-40, "C"))

    def test_ac5_below_absolute_zero_raises(self):
        with self.assertRaises(ValueError):
            convert(-300, "C")
        with self.assertRaises(ValueError):
            convert(-500, "F")

    def test_ac6_unknown_unit_raises(self):
        with self.assertRaises(ValueError):
            convert(10, "K")


class TestCli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *args], capture_output=True, text=True
        )

    def test_ac7_output_rounded_with_unit(self):
        result = self.run_cli("100", "C")
        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout.strip(), "212.00 F")

    def test_ac5_ac6_cli_error_exits_1(self):
        result = self.run_cli("10", "K")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error:", result.stdout)


if __name__ == "__main__":
    unittest.main()
