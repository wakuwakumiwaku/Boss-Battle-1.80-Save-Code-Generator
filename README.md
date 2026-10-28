# Boss Battle 1.80 Save Code Generator (updated 30.01.25)
requires Python 3.9.0 

Online live version: http://wakutest.pythonanywhere.com/

## Local usage

Run `python save.py` with Python 3.9 or newer. Enter your case-sensitive
username, an integer level from **0 to 100**, and integer XP from **0 to 1679615**
(inclusive, the maximum that fits four base36 digits). Invalid numeric input
prints a field-specific error and exits nonzero without generating a code.
Valid inputs retain the existing encoding and random choice among six keys.

## Tests

```sh
python -m unittest discover -s tests -v
```

These offline tests check input refusal and exact original output codes for all
six keys. They do not verify codes in the game.
