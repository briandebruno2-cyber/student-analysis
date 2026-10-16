"""
Student Performance Analysis System
===================================
Loads student records from a CSV file, calculates performance metrics,
identifies scholarship-eligible students and prints a performance report.

OOP concepts demonstrated
-------------------------
* Encapsulation   - private/protected attributes, properties, validated setters
* Abstraction     - Student is an abstract base class (ABC) with an abstract method
* Inheritance     - Student -> AIUStudent -> ScholarshipStudent
* Composition     - PerformanceAnalyzer *holds* Student objects (does not copy data)
* Polymorphism    - describe() / generate_report() behave differently per object type
* Overriding      - ScholarshipStudent overrides describe() and generate_report()
* "Overloading"   - calculate_average() uses default/variable-length arguments
"""

import csv
from abc import ABC, abstractmethod


SUBJECTS = ("Math", "English", "Science")   # subjects stored for every student
SCHOLARSHIP_THRESHOLD = 85                  # minimum average for eligibility
MIN_MARK, MAX_MARK = 0, 100                 # valid range for any mark



class Student(ABC):
    """Abstract base class representing any student.

    It cannot be instantiated directly because it has an abstract method
    (describe) that every concrete subclass must implement.
    """

    def __init__(self, student_id, first_name, last_name, programme, marks):
        # Protected attributes (single underscore): for use by this class
        # and its subclasses, accessed from outside only through properties.
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme

        # Private attribute (double underscore -> name mangling).
        # Marks can only be changed through set_mark(), which validates them.
        self.__marks = {}
        for subject, mark in marks.items():
            self.set_mark(subject, mark)

   
    @property
    def student_id(self):
        return self._student_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def full_name(self):
        return f"{self._first_name} {self._last_name}"

    # Programme can be read AND updated (with a simple validation)
    @property
    def programme(self):
        return self._programme

    @programme.setter
    def programme(self, new_programme):
        if not new_programme or not str(new_programme).strip():
            raise ValueError("Programme cannot be empty.")
        self._programme = str(new_programme).strip()

   
    @staticmethod
    def _validate_mark(mark):
        """Return the mark as a float if valid, otherwise raise an error."""
        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise TypeError(f"Mark must be a number, got {mark!r}.")
        if not MIN_MARK <= mark <= MAX_MARK:
            raise ValueError(f"Mark must be between {MIN_MARK} and {MAX_MARK}, got {mark}.")
        return float(mark)

    def set_mark(self, subject, mark):
        """Add or update the mark for one subject (validated)."""
        self.__marks[subject] = self._validate_mark(mark)

    def get_mark(self, subject):
        """Return the mark for one subject."""
        return self.__marks[subject]

    def get_marks(self):
        """Return a COPY of the marks so outside code cannot modify the original."""
        return dict(self.__marks)

    
    def calculate_average(self, *marks):
        """Calculate an average. Works in three ways:

        1. student.calculate_average()            -> average of the student's own marks
        2. student.calculate_average(70, 80, 90)  -> average of three marks supplied separately
        3. student.calculate_average(60, 70, 80, 90, 55) -> any number of marks

        Python has no true method overloading, so *marks (variable-length
        arguments) lets ONE method accept many different call patterns.
        """
        if not marks:                       # no arguments -> use stored marks
            marks = tuple(self.__marks.values())
        if len(marks) == 0:
            raise ValueError("No marks available to average.")
        validated = [self._validate_mark(m) for m in marks]   # validation
        return sum(validated) / len(validated)

    @property
    def average(self):
        """Average of this student's own marks."""
        return self.calculate_average()

    def get_grade(self):
        """Convert the average into a letter grade."""
        avg = self.average
        if avg >= 80:
            return "A"
        if avg >= 70:
            return "B"
        if avg >= 60:
            return "C"
        if avg >= 50:
            return "D"
        return "F"

    
    @abstractmethod
    def describe(self):
        """Return a one-line description specific to the student type."""

    
    def generate_report(self):
        """Return a formatted multi-line report for this student."""
        lines = [
            f"Student ID : {self.student_id}",
            f"Name       : {self.full_name}",
            f"Programme  : {self.programme}",
            "Marks      : " + ", ".join(f"{s}={m:.0f}" for s, m in self.get_marks().items()),
            f"Average    : {self.average:.2f}",
            f"Grade      : {self.get_grade()}",
            f"Type       : {self.describe()}",
        ]
        return "\n".join(lines)

    def __str__(self):
        return f"{self.student_id} - {self.full_name} ({self.average:.2f}, grade {self.get_grade()})"



class AIUStudent(Student):
    """A regular student (no scholarship)."""

    def describe(self):
        return "Regular AIU student (no scholarship)"



class ScholarshipStudent(AIUStudent):
    """A student who has applied for / holds a scholarship."""

    def __init__(self, student_id, first_name, last_name, programme, marks,
                 scholarship_amount=0):
        # super() runs the parent constructor so we don't duplicate its code
        super().__init__(student_id, first_name, last_name, programme, marks)
        self.scholarship_amount = scholarship_amount

    @property
    def scholarship_amount(self):
        return self._scholarship_amount

    @scholarship_amount.setter
    def scholarship_amount(self, amount):
        if amount < 0:
            raise ValueError("Scholarship amount cannot be negative.")
        self._scholarship_amount = amount

    def is_eligible(self):
        """True when the average meets the scholarship threshold."""
        return self.average >= SCHOLARSHIP_THRESHOLD

    # Overridden method (same name as in AIUStudent, different behaviour)
    def describe(self):
        status = "ELIGIBLE" if self.is_eligible() else "NOT eligible"
        return (f"Scholarship student - {status} "
                f"(amount: KES {self.scholarship_amount:,.0f})")

    # Overridden to add scholarship details, reusing the parent's output
    def generate_report(self):
        base_report = super().generate_report()
        eligibility = "Yes" if self.is_eligible() else "No"
        return base_report + f"\nScholarship: Eligible = {eligibility}"



class PerformanceAnalyzer:
    """Analyses a collection of Student objects.

    Composition: it keeps references to existing Student objects
    instead of copying their data.
    """

    def __init__(self, students):
        if not students:
            raise ValueError("At least one student is required.")
        self._students = list(students)

    def highest_average(self):
        """Return the student with the highest average."""
        return max(self._students, key=lambda s: s.average)

    def lowest_average(self):
        """Return the student with the lowest average."""
        return min(self._students, key=lambda s: s.average)

    def class_average(self):
        """Return the average of all student averages."""
        return sum(s.average for s in self._students) / len(self._students)

    def eligible_students(self):
        """Return all scholarship students who meet the threshold."""
        return [s for s in self._students
                if isinstance(s, ScholarshipStudent) and s.is_eligible()]

    
    def generate_report(self):
        """Return the full report: every student plus a class summary."""
        line = "=" * 60
        parts = [line, "STUDENT PERFORMANCE REPORT".center(60), line]

        for student in self._students:
            parts.append(student.generate_report())   # polymorphic call
            parts.append("-" * 60)

        best, worst = self.highest_average(), self.lowest_average()
        eligible = self.eligible_students()
        parts += [
            "CLASS SUMMARY".center(60),
            line,
            f"Total students        : {len(self._students)}",
            f"Highest average       : {best.average:.2f} ({best.full_name})",
            f"Lowest average        : {worst.average:.2f} ({worst.full_name})",
            f"Overall class average : {self.class_average():.2f}",
            f"Scholarship eligible  : {len(eligible)} "
            f"({', '.join(s.full_name for s in eligible) or 'none'})",
            line,
        ]
        return "\n".join(parts)



def load_students(csv_path):
    """Read the CSV and return a list of Student objects.

    Rows with a ScholarshipAmount above 0 become ScholarshipStudent objects;
    all other rows become AIUStudent objects.
    """
    students = []
    with open(csv_path, newline="", encoding="utf-8") as file:
        for row_number, row in enumerate(csv.DictReader(file), start=2):
            try:
                marks = {subject: float(row[subject]) for subject in SUBJECTS}
                amount = float(row.get("ScholarshipAmount") or 0)
                details = (row["StudentID"], row["FName"], row["LName"],
                           row["Programme"], marks)
                if amount > 0:
                    students.append(ScholarshipStudent(*details, scholarship_amount=amount))
                else:
                    students.append(AIUStudent(*details))
            except (KeyError, ValueError, TypeError) as error:
                print(f"Skipping CSV line {row_number}: {error}")
    return students



def demonstrate_polymorphism(students):
    """Task 5: same method name, different behaviour per object type."""
    print("\nPOLYMORPHISM DEMO - calling describe() on a mixed list")
    print("-" * 60)
    for student in students:
        # Python decides at run time which describe() to call
        print(f"{type(student).__name__:<18} {student.full_name:<16} -> {student.describe()}")


def demonstrate_flexible_method(student):
    """Task 6: one method, several ways to call it, with validation."""
    print("\nFLEXIBLE METHOD DEMO - calculate_average()")
    print("-" * 60)
    print("No arguments (own marks)   :", f"{student.calculate_average():.2f}")
    print("Three separate marks       :", f"{student.calculate_average(70, 80, 90):.2f}")
    print("Five marks (variable)      :", f"{student.calculate_average(60, 70, 80, 90, 55):.2f}")
    try:
        student.calculate_average(70, 150)
    except ValueError as error:
        print("Invalid mark rejected      :", error)
    try:
        student.calculate_average(70, "eighty")
    except TypeError as error:
        print("Wrong type rejected        :", error)


def main():
    students = load_students("students.csv")
    analyzer = PerformanceAnalyzer(students)

    report = analyzer.generate_report()
    print(report)

    demonstrate_polymorphism(students)
    demonstrate_flexible_method(students[0])

    # Save the report to a text file as well
    with open("performance_report.txt", "w", encoding="utf-8") as out:
        out.write(report)
    print("\nReport saved to performance_report.txt")


if __name__ == "__main__":
    main()
