"""Tests for specs/temperature-converter. Each test names the acceptance criterion it covers."""
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "src", "converter.py")
sys.path.insert(0, os.path.join(ROOT, "src"))

from converter import convert  # noqa: E402

PLACES = 9  # design.md: compare with a small tolerance, not exact equality


class TestConvert(unittest.TestCase):
    def assertConverts(self, value, from_unit, to_unit, expected):
        self.assertAlmostEqual(convert(value, from_unit, to_unit), expected, places=PLACES)

    def test_ac1_100c_is_212f(self):
        self.assertConverts(100, "C", "F", 212)

    def test_ac2_0c_is_32f(self):
        self.assertConverts(0, "C", "F", 32)

    def test_ac3_32f_is_0c(self):
        self.assertConverts(32, "F", "C", 0)

    def test_ac4_minus40f_is_minus40c(self):
        self.assertConverts(-40, "F", "C", -40)

    def test_ac5_below_absolute_zero_raises(self):
        for value, unit in [(-300, "C"), (-500, "F"), (-0.01, "K")]:
            with self.subTest(value=value, unit=unit):
                with self.assertRaises(ValueError):
                    convert(value, unit, "K")

    def test_ac5_absolute_zero_itself_is_allowed(self):
        self.assertConverts(0, "K", "C", -273.15)

    def test_ac6_unknown_source_unit_raises(self):
        with self.assertRaises(ValueError):
            convert(10, "X", "C")

    def test_ac6_unknown_target_unit_raises(self):
        with self.assertRaises(ValueError):
            convert(10, "C", "X")

    def test_ac8_0c_is_273_15k(self):
        self.assertConverts(0, "C", "K", 273.15)

    def test_ac9_32f_is_273_15k(self):
        self.assertConverts(32, "F", "K", 273.15)

    def test_ac10_0k_is_minus273_15c(self):
        self.assertConverts(0, "K", "C", -273.15)

    def test_ac11_0k_is_minus459_67f(self):
        self.assertConverts(0, "K", "F", -459.67)

    def test_units_are_case_insensitive(self):
        self.assertConverts(0, "c", "k", 273.15)

    def test_same_unit_returns_same_value(self):
        self.assertConverts(42, "K", "K", 42)


class TestCli(unittest.TestCase):
    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, SCRIPT, *args], capture_output=True, text=True
        )

    def assertOutput(self, args, expected):
        result = self.run_cli(*args)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(result.stdout.strip(), expected)

    def test_ac7_output_rounded_with_unit(self):
        self.assertOutput(["100", "C", "F"], "212.00 F")

    def test_ac7_output_never_shows_negative_zero(self):
        # -17.78 C is -0.004 F, which would print as "-0.00"
        self.assertOutput(["-17.78", "C", "F"], "0.00 F")

    def test_ac12_kelvin_from_cli(self):
        self.assertOutput(["0", "C", "K"], "273.15 K")

    def test_ac12_two_argument_form_prints_usage(self):
        result = self.run_cli("100", "C")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Usage:", result.stdout)

    def test_ac5_ac6_cli_error_exits_1(self):
        result = self.run_cli("10", "C", "X")
        self.assertEqual(result.returncode, 1)
        self.assertIn("Error:", result.stdout)


if __name__ == "__main__":
    unittest.main()
