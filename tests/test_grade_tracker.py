import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from grade_tracker import (  # noqa: E402
    Module, classify, load_modules, parse_credits, parse_grade, save_modules,
    summarize, weighted_average,
)


@pytest.mark.parametrize("text, expected", [("0", 0), ("100", 100), ("72.5", 72.5)])
def test_parse_grade_accepts_valid_marks(text, expected):
    assert parse_grade(text) == expected


@pytest.mark.parametrize("text", ["-1", "100.1", "abc", ""])
def test_parse_grade_rejects_invalid_marks(text):
    with pytest.raises(ValueError):
        parse_grade(text)


def test_parse_credits_defaults_when_blank():
    assert parse_credits("  ") == 20


@pytest.mark.parametrize("text", ["0", "-10", "7.5", "ten"])
def test_parse_credits_rejects_invalid_values(text):
    with pytest.raises(ValueError):
        parse_credits(text)


def test_weighted_average_weights_by_credits():
    modules = [Module("Programming", 80, 40), Module("Maths", 50, 20)]
    # (80*40 + 50*20) / 60 = 70, whereas a plain average would give 65
    assert weighted_average(modules) == pytest.approx(70)


def test_weighted_average_needs_modules():
    with pytest.raises(ValueError):
        weighted_average([])


@pytest.mark.parametrize("average, label", [
    (70, "Distinction"), (69.99, "Merit"), (60, "Merit"),
    (50, "Pass"), (49.9, "Below pass - needs improvement"), (0, "Below pass - needs improvement"),
])
def test_classify_boundaries(average, label):
    assert classify(average) == label


def test_summarize_reports_best_and_worst_modules():
    modules = [Module("Databases", 65), Module("Networks", 48), Module("Web Dev", 81)]
    summary = summarize(modules)
    assert summary.best.name == "Web Dev"
    assert summary.worst.name == "Networks"
    assert summary.count == 3
    assert summary.classification == "Merit"


def test_summarize_empty_returns_none():
    assert summarize([]) is None


def test_save_then_load_round_trips(tmp_path):
    path = tmp_path / "grades.json"
    modules = [Module("Programming", 78.5, 40), Module("Maths", 62)]
    save_modules(modules, path)
    assert load_modules(path) == modules


def test_load_missing_file_starts_fresh(tmp_path):
    assert load_modules(tmp_path / "nope.json") == []


def test_load_corrupted_file_starts_fresh(tmp_path):
    path = tmp_path / "grades.json"
    path.write_text("{not valid json")
    assert load_modules(path) == []
