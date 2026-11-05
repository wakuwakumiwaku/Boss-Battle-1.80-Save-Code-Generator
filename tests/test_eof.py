"""Exercise real stdin truncation, not a mocked encoder or input helper."""
from pathlib import Path
import subprocess
import sys
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'save.py'


class EndOfInputTests(unittest.TestCase):
    def test_eof_at_each_prompt_is_a_clear_nonzero_exit(self):
        for stdin, field in [('', 'Username'), ('Player\n', 'Level'), ('Player\n1\n', 'XP')]:
            with self.subTest(field=field):
                result = subprocess.run([sys.executable, str(SCRIPT)], input=stdin,
                                        text=True, capture_output=True, timeout=5)
                self.assertNotEqual(result.returncode, 0)
                self.assertNotIn('Traceback', result.stderr, 'truncated stdin is not a programming error')
                self.assertIn('input ended before ' + field, result.stderr)
                self.assertNotIn('Generated Code:', result.stdout)

    def test_final_value_without_newline_is_complete_input(self):
        result = subprocess.run([sys.executable, str(SCRIPT)], input='J\n1\n1',
                                text=True, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, '')
        self.assertIn('Generated Code:', result.stdout)


if __name__ == '__main__':
    unittest.main()
