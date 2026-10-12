"""Tests for the US-5 browser page (src/gui.py). Each test names the acceptance criterion it covers."""
import os
import sys
import threading
import unittest
import urllib.error
import urllib.request
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))

import converter  # noqa: E402
import gui  # noqa: E402

RANKINE = {"R": (0.0, 5 / 9)}  # a unit that does not exist yet, for AC-17


class TestConversionLines(unittest.TestCase):
    def test_ac14_shows_every_other_unit(self):
        self.assertEqual(gui.conversion_lines("100", "C"), ["212.00 F", "373.15 K"])

    def test_ac14_source_unit_is_not_repeated(self):
        for unit in converter.UNITS:
            with self.subTest(unit=unit):
                lines = gui.conversion_lines("300", unit)
                self.assertEqual(len(lines), len(converter.UNITS) - 1)
                self.assertFalse(any(line.endswith(" " + unit) for line in lines))

    def test_ac15_never_negative_zero(self):
        self.assertEqual(gui.conversion_lines("-17.78", "C")[0], "0.00 F")

    def test_ac16_not_a_number_is_rejected(self):
        for text in ["", "   ", "abc", "nan", "inf", "-inf"]:
            with self.subTest(text=text):
                with self.assertRaisesRegex(ValueError, "Enter a number"):
                    gui.conversion_lines(text, "C")

    def test_ac16_below_absolute_zero_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "Below absolute zero"):
            gui.conversion_lines("-300", "C")

    def test_surrounding_spaces_and_lower_case_unit_are_accepted(self):
        self.assertEqual(gui.conversion_lines(" 0 ", "k"), ["-273.15 C", "-459.67 F"])

    def test_ac17_new_unit_appears_in_results(self):
        with mock.patch.dict(converter.UNITS, RANKINE):
            self.assertIn("491.67 R", gui.conversion_lines("0", "C"))
            self.assertIn("0.00 C", gui.conversion_lines("491.67", "R"))


class TestRenderPage(unittest.TestCase):
    def test_ac13_form_has_value_field_and_every_unit(self):
        page = gui.render_page(None, "C")
        self.assertIn('name="value"', page)
        self.assertIn('name="unit"', page)
        for unit in converter.UNITS:
            self.assertIn(f'<option value="{unit}"', page)

    def test_first_load_shows_no_results_or_error(self):
        page = gui.render_page(None, "C")
        self.assertNotIn("Error", page)
        self.assertNotIn("212.00", page)

    def test_ac14_results_are_shown(self):
        page = gui.render_page("100", "C")
        self.assertIn("212.00 F", page)
        self.assertIn("373.15 K", page)

    def test_ac16_keeps_value_and_unit_after_converting(self):
        page = gui.render_page("100", "K")
        self.assertIn('value="100"', page)
        self.assertIn('<option value="K" selected', page)

    def test_ac16_error_replaces_results(self):
        page = gui.render_page("abc", "C")
        self.assertIn("Error: Enter a number", page)
        self.assertIn('value="abc"', page)

    def test_ac16_unknown_unit_from_address_shows_error(self):
        self.assertIn("Error: Unit must be one of C, F, K", gui.render_page("100", "X"))

    def test_ac17_new_unit_appears_in_unit_list(self):
        with mock.patch.dict(converter.UNITS, RANKINE):
            self.assertIn('<option value="R"', gui.render_page(None, "C"))

    def test_entered_value_is_escaped(self):
        page = gui.render_page("<script>alert(1)</script>", "C")
        self.assertNotIn("<script>", page)
        self.assertIn("&lt;script&gt;", page)

    def test_minimal_formatting_no_css_or_javascript(self):
        page = gui.render_page("100", "C")
        for marker in ["<style", "style=", "<script", "<link", "<img"]:
            self.assertNotIn(marker, page)


class TestServer(unittest.TestCase):
    def setUp(self):
        self.server = gui.make_server()
        self.port = self.server.server_address[1]
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()

    def fetch(self, path):
        url = f"http://127.0.0.1:{self.port}{path}"
        with urllib.request.urlopen(url, timeout=5) as response:
            return response.status, response.headers.get_content_type(), response.read().decode("utf-8")

    def test_ac18_listens_on_localhost_and_a_free_port(self):
        self.assertEqual(self.server.server_address[0], "127.0.0.1")
        self.assertNotEqual(self.port, 0)

    def test_ac18_serves_a_conversion(self):
        status, content_type, body = self.fetch("/?value=100&unit=C")
        self.assertEqual(status, 200)
        self.assertEqual(content_type, "text/html")
        self.assertIn("212.00 F", body)

    def test_first_load_serves_the_empty_form(self):
        status, _, body = self.fetch("/")
        self.assertEqual(status, 200)
        self.assertIn('name="value"', body)
        self.assertNotIn("Error", body)

    def test_ac16_server_keeps_running_after_an_error(self):
        _, _, body = self.fetch("/?value=abc&unit=C")
        self.assertIn("Error: Enter a number", body)
        _, _, body = self.fetch("/?value=0&unit=C")
        self.assertIn("32.00 F", body)

    def test_ac16_submitting_an_empty_field_shows_an_error(self):
        _, _, body = self.fetch("/?value=&unit=C")
        self.assertIn("Error: Enter a number", body)

    def test_other_paths_return_404(self):
        with self.assertRaises(urllib.error.HTTPError) as caught:
            self.fetch("/favicon.ico")
        self.assertEqual(caught.exception.code, 404)


if __name__ == "__main__":
    unittest.main()
