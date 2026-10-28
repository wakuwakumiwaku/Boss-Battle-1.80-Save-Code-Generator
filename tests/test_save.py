"""Offline CLI regression tests; SAVE_SCRIPT can select an archived baseline."""

import contextlib
import io
import os
from pathlib import Path
import runpy
import subprocess
import sys
import unittest
from unittest.mock import patch


SCRIPT = Path(os.environ.get(
    "SAVE_SCRIPT", str(Path(__file__).resolve().parents[1] / "save.py")
))

# Exact outputs captured from the original encoder for each of its six keys.
VALID_CODES = [
    ("", 0, 0, ["1-JJJJJJ-JJ", "2-AAAAAA-AA", "3-999999-99",
                 "4-777777-77", "5-JJJJJJ-JJ", "6-YYYYYY-YY"]),
    ("JC", 100, 1679615, ["1-GGGGYH-IS", "2-WWWW97-PH", "3-4444QV-3I",
                          "4-3333WK-R4", "5-ZZZZ9V-EW", "6-QQQQNA-LH"]),
    ("jc", 100, 1679615, ["1-GGGGYH-IY", "2-WWWW97-P9", "3-4444QV-3Q",
                          "4-3333WK-RW", "5-ZZZZ9V-E9", "6-QQQQNA-LN"]),
    ("J", 1, 1, ["1-JJJCJC-YY", "2-AAA0A0-99", "3-999292-QQ",
                  "4-777M7M-WW", "5-JJJUJU-99", "6-YYYXYX-NN"]),
    ("A user", 35, 35, ["1-JJJGJG-FI", "2-AAAWAW-6P", "3-999494-Y3",
                        "4-777373-PR", "5-JJJZJZ-HE", "6-YYYQYQ-1L"]),
    ("MiXeD", 36, 36, ["1-JJCJCJ-YD", "2-AA0A0A-9N", "3-992929-QJ",
                       "4-77M7M7-W5", "5-JJUJUJ-9D", "6-YYXYXY-NK"]),
    ("Player", 99, 46655, ["1-JGGGYR-IH", "2-AWWW9F-P7", "3-9444Q8-3V",
                          "4-7333W6-RK", "5-JZZZ9X-EV", "6-YQQQNM-LA"]),
    ("Player", 100, 46656, ["1-CJJJYH-3H", "2-0AAA97-J7", "3-2999QV-RV",
                           "4-M777WK-HK", "5-UJJJ9V-2V", "6-XYYYNA-2A"]),
]


class SaveInputTests(unittest.TestCase):
    def assert_refused(self, level, xp, field, minimum, maximum):
        stdout = io.StringIO()
        stderr = io.StringIO()
        failure = None
        with patch("builtins.input", side_effect=["Player", level, xp]), \
                patch("random.randint", return_value=1) as randint, \
                contextlib.redirect_stdout(stdout), \
                contextlib.redirect_stderr(stderr):
            try:
                runpy.run_path(str(SCRIPT), run_name="__main__")
            except (Exception, SystemExit) as exc:
                failure = exc
        if not isinstance(failure, SystemExit):
            self.fail("invalid input must exit clearly, not generate a code or crash: {!r}".format(failure))
        self.assertNotIn(failure.code, (None, 0))
        message = str(failure.code) + stderr.getvalue() + stdout.getvalue()
        self.assertIn(
            "{} must be an integer between {} and {}".format(field, minimum, maximum),
            message,
        )
        self.assertNotIn("Generated Code:", stdout.getvalue())
        self.assertNotIn("Traceback", message)
        randint.assert_not_called()

    def test_negative_level_is_refused(self):
        for value in ("-1", "-36", "-999999999999999999999"):
            with self.subTest(value=value):
                self.assert_refused(value, "0", "Level", 0, 100)

    def test_level_above_promised_limit_is_refused(self):
        for value in ("101", "1295", "1296", "999999999999999999999"):
            with self.subTest(value=value):
                self.assert_refused(value, "0", "Level", 0, 100)

    def test_negative_xp_is_refused(self):
        for value in ("-1", "-36", "-1679616", "-999999999999999999999"):
            with self.subTest(value=value):
                self.assert_refused("0", value, "XP", 0, 1679615)

    def test_xp_over_four_digit_width_is_refused(self):
        for value in ("1679616", "999999999999999999999"):
            with self.subTest(value=value):
                self.assert_refused("0", value, "XP", 0, 1679615)

    def test_non_integer_level_is_refused(self):
        for value in ("", " ", "1.5", "abc", "NaN"):
            with self.subTest(value=value):
                self.assert_refused(value, "0", "Level", 0, 100)

    def test_non_integer_xp_is_refused(self):
        for value in ("", " ", "1.5", "abc", "NaN"):
            with self.subTest(value=value):
                self.assert_refused("0", value, "XP", 0, 1679615)

    def test_original_codes_for_all_six_keys_and_boundaries(self):
        for name, level, xp, codes in VALID_CODES:
            for key, code in enumerate(codes, 1):
                with self.subTest(name=name, level=level, xp=xp, key=key):
                    stdout = io.StringIO()
                    with patch("builtins.input", side_effect=[name, str(level), str(xp)]), \
                            patch("random.randint", return_value=key) as randint, \
                            contextlib.redirect_stdout(stdout):
                        runpy.run_path(str(SCRIPT), run_name="__main__")
                    self.assertEqual(stdout.getvalue(), "Generated Code: {}\n".format(code))
                    randint.assert_called_once_with(1, 6)

    def test_integer_whitespace_and_signs_stay_accepted(self):
        stdout = io.StringIO()
        with patch("builtins.input", side_effect=["J", " +1 ", " 01 "]), \
                patch("random.randint", return_value=1), contextlib.redirect_stdout(stdout):
            runpy.run_path(str(SCRIPT), run_name="__main__")
        self.assertEqual(stdout.getvalue(), "Generated Code: 1-JJJCJC-YY\n")

    def test_real_cli_refuses_without_a_traceback(self):
        for stdin, expected in (("Player\n101\n0\n", "Level"),
                                ("Player\n0\n1679616\n", "XP"),
                                ("Player\nnope\n0\n", "Level")):
            with self.subTest(stdin=stdin):
                result = subprocess.run([sys.executable, str(SCRIPT)], input=stdin,
                                        text=True, capture_output=True, timeout=5)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(expected + " must be an integer between", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("Generated Code:", result.stdout)

    def test_real_cli_valid_random_code_is_one_of_original_six(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], input="J\n1\n1\n",
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        code = result.stdout.split("Generated Code: ")[-1].strip()
        self.assertIn(code, VALID_CODES[3][3])


if __name__ == "__main__":
    unittest.main()
