"""Student Grade Tracker.

Enter your modules, their credit values and your marks, and get a
credit-weighted average with a classification. Grades are saved to a JSON
file so they're still there next time you run it.

The calculation functions are pure (no input/print), which is what lets
tests/test_grade_tracker.py check them directly.
"""
import json
from dataclasses import asdict, dataclass
from pathlib import Path

DEFAULT_SAVE_FILE = Path("grades.json")
DEFAULT_CREDITS = 20

# (minimum average, label), checked from the top down
CLASSIFICATIONS = [
    (70, "Distinction"),
    (60, "Merit"),
    (50, "Pass"),
    (0, "Below pass - needs improvement"),
]


@dataclass
class Module:
    name: str
    grade: float
    credits: int = DEFAULT_CREDITS


@dataclass
class Summary:
    count: int
    weighted_average: float
    best: Module
    worst: Module
    classification: str


# ---------------- Validation ----------------

def parse_grade(text):
    """Turn user input into a grade between 0 and 100, or raise ValueError."""
    try:
        grade = float(text)
    except ValueError:
        raise ValueError("Please enter a number.")
    if not 0 <= grade <= 100:
        raise ValueError("Grades must be between 0 and 100.")
    return grade


def parse_credits(text):
    """Turn user input into a positive whole number of credits (blank = default)."""
    if not text.strip():
        return DEFAULT_CREDITS
    try:
        credits = int(text)
    except ValueError:
        raise ValueError("Credits must be a whole number.")
    if credits <= 0:
        raise ValueError("Credits must be greater than zero.")
    return credits


# ---------------- Calculations ----------------

def weighted_average(modules):
    """Credit-weighted mean: a 40-credit module counts twice as much as a 20-credit one."""
    total_credits = sum(m.credits for m in modules)
    if total_credits == 0:
        raise ValueError("Need at least one module to calculate an average.")
    return sum(m.grade * m.credits for m in modules) / total_credits


def classify(average):
    for minimum, label in CLASSIFICATIONS:
        if average >= minimum:
            return label
    raise ValueError(f"Invalid average: {average}")


def summarize(modules):
    """Return a Summary, or None if there are no modules."""
    if not modules:
        return None
    average = weighted_average(modules)
    return Summary(
        count=len(modules),
        weighted_average=average,
        best=max(modules, key=lambda m: m.grade),
        worst=min(modules, key=lambda m: m.grade),
        classification=classify(average),
    )


# ---------------- Saving and loading ----------------

def save_modules(modules, path=DEFAULT_SAVE_FILE):
    Path(path).write_text(json.dumps([asdict(m) for m in modules], indent=2))


def load_modules(path=DEFAULT_SAVE_FILE):
    """Load saved modules. A missing or corrupted file just means starting fresh."""
    try:
        data = json.loads(Path(path).read_text())
        return [Module(**item) for item in data]
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        return []


# ---------------- Console UI ----------------

def ask(prompt, parser):
    """Keep asking until `parser` accepts the answer."""
    while True:
        try:
            return parser(input(prompt))
        except ValueError as error:
            print(f"  {error}")


def enter_modules():
    modules = []
    while True:
        name = input("Module name (or press Enter to finish): ").strip()
        if not name:
            return modules
        grade = ask(f"  Mark for {name} (0-100): ", parse_grade)
        credits = ask(f"  Credits for {name} [{DEFAULT_CREDITS}]: ", parse_credits)
        modules.append(Module(name, grade, credits))


def print_report(modules):
    print("\n=== Grade Report ===")
    summary = summarize(modules)
    if summary is None:
        print("No modules entered yet.")
        return

    width = max(len(m.name) for m in modules)
    for m in modules:
        print(f"  {m.name:<{width}}  {m.grade:>5.1f}  ({m.credits} credits)")

    print("\n--- Summary ---")
    print(f"Modules:          {summary.count}")
    print(f"Weighted average: {summary.weighted_average:.2f}")
    print(f"Best:             {summary.best.name} ({summary.best.grade:g})")
    print(f"Needs most work:  {summary.worst.name} ({summary.worst.grade:g})")
    print(f"Classification:   {summary.classification}")


def main():
    print("=== Student Grade Tracker ===\n")
    modules = load_modules()
    if modules:
        print(f"Loaded {len(modules)} saved module(s) from {DEFAULT_SAVE_FILE}.\n")

    modules += enter_modules()
    save_modules(modules)
    print_report(modules)


if __name__ == "__main__":
    main()
