# student-analysis

A Python program built with Object-Oriented Programming (OOP). It loads student
records from a CSV file, calculates averages and grades, identifies
scholarship-eligible students and generates a performance report.

**Author:** Brian (GitHub: briandebruno2-cyber)

## How to Run
```bash
python student_performance_system.py
```
Requires Python 3.8 or later and no external libraries. Run the program from the
folder containing `students.csv`. The report is printed on screen and also saved to
`performance_report.txt`.

## Project Files
| File | Purpose |
|---|---|
| `student_performance_system.py` | All classes and the main program |
| `students.csv` | Dataset of 8 students |
| `performance_report.txt` | Sample output of the program |

## Class Design
```
Student (abstract base class)
   └── AIUStudent
          └── ScholarshipStudent

PerformanceAnalyzer  --uses-->  a list of Student objects
```

## OOP Concepts and Where They Appear
| Concept | Implementation |
|---|---|
| Encapsulation | `Student` uses protected attributes (`_first_name`), a private `__marks` dictionary, properties, and a validated `set_mark()` method |
| Abstraction | `Student` inherits from `ABC` and declares the abstract method `describe()`, so it cannot be instantiated directly |
| Inheritance | `AIUStudent` inherits from `Student`; `ScholarshipStudent` inherits from `AIUStudent` and calls `super().__init__()` |
| Composition | `PerformanceAnalyzer` holds references to existing student objects instead of copying their data |
| Polymorphism | `describe()` and `generate_report()` behave differently for each student type |
| Method overriding | `ScholarshipStudent` overrides `describe()` and `generate_report()` |
| Method overloading (equivalent) | `calculate_average(*marks)` accepts different numbers of arguments |

## Dataset
`students.csv` contains the four given students plus four more. The columns are
StudentID, FName, LName, Programme, Math, English, Science and ScholarshipAmount.
A row with a ScholarshipAmount above 0 is loaded as a `ScholarshipStudent`; all
other rows are loaded as `AIUStudent`.

## Grading Scale and Scholarship Rule
| Average | Grade |
|---|---|
| 80 and above | A |
| 70 - 79 | B |
| 60 - 69 | C |
| 50 - 59 | D |
| Below 50 | F |

A scholarship student is **eligible** if their average is **at least 85**.

## How Polymorphism and Method Overriding Are Demonstrated
`AIUStudent` and `ScholarshipStudent` both have a method called `describe()`.
`ScholarshipStudent` overrides the `AIUStudent` version to show its scholarship
eligibility and amount. All students are stored in one list, and a loop calls
`student.describe()` on each one without checking its type. Python chooses the
correct version at run time based on the actual object, so regular students print
"Regular AIU student" and scholarship students print their eligibility and amount.
`generate_report()` is overridden in the same way: `ScholarshipStudent` calls
`super().generate_report()` and then adds the scholarship line.

## How Method Overloading Is Handled
Python does not support traditional overloading, because defining a second method
with the same name simply replaces the first. Instead I used variable-length
arguments in `calculate_average(self, *marks)`:

- `student.calculate_average()` averages the student's own stored marks.
- `student.calculate_average(70, 80, 90)` averages three marks given separately.
- `student.calculate_average(60, 70, 80, 90, 55)` averages any number of marks.

The method validates its input. Each mark must be a number (otherwise `TypeError`)
between 0 and 100 (otherwise `ValueError`), and an empty list cannot be averaged.
One method therefore supports several ways of calling it.

## Sample Output (summary)
- Total students: 8
- Highest average: 92.33 (Ruth Mwimali)
- Lowest average: 48.33 (Brian Kiprop)
- Overall class average: 75.58
- Scholarship eligible: Carlos Ndunda and Ruth Mwimali

The full report is in `performance_report.txt`.


