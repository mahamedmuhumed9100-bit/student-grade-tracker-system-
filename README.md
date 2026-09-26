# Student Grade Tracker (Python)

[![Tests](https://github.com/mahamedmuhumed9100-bit/student-grade-tracker-system-/actions/workflows/ci.yml/badge.svg)](https://github.com/mahamedmuhumed9100-bit/student-grade-tracker-system-/actions/workflows/ci.yml)

A command-line tool for tracking university module marks. Enter each module's
mark and credit value, and it works out your **credit-weighted average** and
classification — and remembers your modules between runs.

```text
=== Grade Report ===
  Programming   78.0  (40 credits)
  Maths         55.0  (20 credits)
  Web Dev       81.0  (20 credits)

--- Summary ---
Modules:          3
Weighted average: 73.00
Best:             Web Dev (81)
Needs most work:  Maths (55)
Classification:   Distinction
```

## Features

- **Credit-weighted average** — a 40-credit module counts twice as much as a
  20-credit one, the way universities actually calculate it (a plain average
  of the example above would give 71.3, not 73)
- Classification: Distinction (70+), Merit (60+), Pass (50+)
- Shows your best module and the one that needs the most work
- **Saves to `grades.json`** so you can add modules over the year; a missing or
  corrupted file is handled gracefully
- Input validation that re-asks instead of crashing (marks 0–100, positive
  whole-number credits)

## Design

The calculation functions (`weighted_average`, `classify`, `summarize`, the
parsers) are **pure** — they never call `input()` or `print()`. All console I/O
lives in a few small functions at the bottom of the file. That split is what
makes the logic easy to test: 25 pytest tests cover grade boundaries, invalid
input, weighting, and save/load round-trips, and GitHub Actions runs them on
every push.

## Running it

Python 3.9+ with no extra libraries:

```bash
python grade_tracker.py
```

## Running the tests

```bash
pip install pytest
pytest -v
```

## What I'd add next

- Assessment-level marks (e.g. coursework 40% + exam 60%) inside each module
- A "what do I need in my exam to get a Distinction?" calculator
- Export the report to CSV
