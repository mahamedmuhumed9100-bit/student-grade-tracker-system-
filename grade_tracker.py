# Student Grade Tracker
# Simple Python program to store student subjects and grades
# and calculate average, highest and lowest grades.

def get_grades():
    print("=== Student Grade Tracker ===\n")
    subjects = []
    grades = []

    while True:
        subject = input("Enter subject name (or press Enter to finish): ")
        if subject == "":
            break

        while True:
            try:
                grade = float(input(f"Enter grade for {subject} (0-100): "))
                if 0 <= grade <= 100:
                    break
                else:
                    print("Please enter a grade between 0 and 100.")
            except ValueError:
                print("Please enter a valid number.")
        subjects.append(subject)
        grades.append(grade)

    return subjects, grades


def calculate_statistics(grades):
    if not grades:
        return None, None, None

    average = sum(grades) / len(grades)
    highest = max(grades)
    lowest = min(grades)
    return average, highest, lowest


def display_report(subjects, grades):
    print("\n=== Grade Report ===")
    if not subjects:
        print("No subjects entered.")
        return

    for subject, grade in zip(subjects, grades):
        print(f"{subject}: {grade}")

    average, highest, lowest = calculate_statistics(grades)

    print("\n--- Summary ---")
    print(f"Number of subjects: {len(subjects)}")
    print(f"Average grade: {average:.2f}")
    print(f"Highest grade: {highest}")
    print(f"Lowest grade: {lowest}")

    if average >= 70:
        print("Overall Performance: Distinction level")
    elif average >= 60:
        print("Overall Performance: Merit level")
    elif average >= 50:
        print("Overall Performance: Pass level")
    else:
        print("Overall Performance: Below pass – needs improvement")


def main():
    subjects, grades = get_grades()
    display_report(subjects, grades)


if __name__ == "__main__":
    main()
