"""
Configuration for Week 1 Assignment: Chapters 0 and 1
Update this file with expected outputs for each assignment.
"""

# Assignment metadata
ASSIGNMENT_NAME = "Week 1: Intro to Python"
NOTEBOOKS_TO_GRADE = [
    "00_intro/01_excercises_markdown.ipynb",
    "01_elements/01_excercises_print.ipynb",
    "01_elements/02_excercises_for-loops.ipynb",
    "01_elements/04_exercises_calculator.ipynb",
]

# Commit analysis criteria
MIN_COMMITS = 3
MIN_DESCRIPTIVE_RATIO = 0.5  # At least half of commits should be descriptive

# Test configuration for each notebook
# Cell indices are 0-based (first cell = 0)
TEST_CONFIGS = {
    "00_intro/01_excercises_markdown.ipynb": {
        "questions": {
            "Q1": {
                "type": "essay",
                "cell_index": 7,  # Markdown cell with Bundesliga table
                "points": 3,
                "description": "Create formatted table with rankings"
            },
            "Q2": {
                "type": "essay",
                "cell_index": 9,  # Markdown cell with Einstein quote
                "points": 2,
                "description": "Display quote with proper formatting"
            },
            "Q3": {
                "type": "essay",
                "cell_index": 11,  # Markdown cell with image
                "points": 2,
                "description": "Integrate image from URL"
            }
        }
    },
    
    "01_elements/01_excercises_print.ipynb": {
        "questions": {
            "Q1": {
                "type": "code",
                "cell_index": 3,  # The cell with print(...)
                "expected_outputs": ["Hello World"],
                "points": 2,
                "description": "Print 'Hello World' using concatenation"
            },
            "Q2": {
                "type": "essay",
                "cell_index": 5,  # Markdown cell with answer
                "points": 2,
                "description": "Explain operator overloading"
            },
            "Q3": {
                "type": "code",
                "cell_index": 8,  # The cell with print(...)
                "expected_outputs": ["Hello World"],
                "points": 2,
                "description": "Print 'Hello World' without concatenation"
            },
            "Q4": {
                "type": "code",
                "cell_index": 11,  # The for loop cell
                "expected_outputs": [
                    "1 2 3 4 5 6 7 8 9 10",  # With spaces
                    "12345678910"  # Without spaces
                ],
                "points": 2,
                "description": "Print 1-10 on one line"
            }
        }
    },
    
    "01_elements/02_excercises_for-loops.ipynb": {
        "questions": {
            "Q1": {
                "type": "code",
                "cell_index": 8,  # for number in numbers: if ...: print(...)
                "expected_outputs": [
                    "3 12 6 9",      # With spaces
                    "31269",         # Without spaces
                    "3  12  6  9",   # Extra spaces (flexible matching will handle)
                ],
                "points": 2,
                "description": "Print numbers divisible by 3"
            },
            "Q2": {
                "type": "code",
                "cell_index": 10,  # for element in [...]: if ...: print(...)
                "expected_outputs": [
                    "7 8 5 3 2 6 9 1 4",   # With spaces
                    "785326914",           # Without spaces
                ],
                "points": 2,
                "description": "Print single-digit numbers"
            },
            "Q3": {
                "type": "code",
                "cell_index": 13,  # for number in sorted(numbers): if ...: print(...)
                "expected_outputs": [
                    "1 3 5 7 9 11",   # With spaces
                    "1357911",        # Without spaces
                ],
                "points": 2,
                "description": "Print odd numbers from sorted list"
            },
            "Q4": {
                "type": "code",
                "cell_index": 16,  # for number in [0-9]: print(...)
                "expected_outputs": [
                    "0 1 2 3 4 5 6 7 8 9",   # With spaces
                    "0123456789",            # Without spaces
                ],
                "points": 1,
                "description": "Print 0-9 on one line"
            },
            "Q5": {
                "type": "code",
                "cell_index": 18,  # for number in range(...): print(...)
                "expected_outputs": [
                    "0 1 2 3 4 5 6 7 8 9",   # With spaces
                    "0123456789",            # Without spaces
                ],
                "points": 2,
                "description": "Use range() to print 0-9"
            },
            "Q6": {
                "type": "code",
                "cell_index": 20,  # for number in range(...): print(...)
                "expected_outputs": [
                    "1 2 3 4 5 6 7 8 9 10",   # With spaces
                    "12345678910",            # Without spaces
                ],
                "points": 2,
                "description": "Use range() to print 1-10"
            },
            "Q7": {
                "type": "code",
                "cell_index": 22,  # for number in range(...): print(...)
                "expected_outputs": [
                    "2 4 6 8 10",   # With spaces
                    "246810",       # Without spaces
                ],
                "points": 2,
                "description": "Use range() with step to print even numbers"
            }
        }
    },
    
    "01_elements/04_exercises_calculator.ipynb": {
        "questions": {
            "Q1": {
                "type": "code",
                "cell_index": 8,  # Volume calculation
                "expected_outputs": [
                    "99.80164096",    # Full precision
                    "99.8016",        # Reasonable precision
                    "99.80",          # Rounded
                ],
                "points": 2,
                "description": "Calculate volume of sphere"
            },
            "Q2.1": {
                "type": "code",
                "cell_index": 12,  # Single expression calculation
                "expected_outputs": ["25"],
                "points": 2,
                "description": "Calculate (b-a)//9 ** 2 in one expression"
            },
            "Q2.2": {
                "type": "code",
                "cell_index": 15,  # Underscore _
                "expected_outputs": ["25"],
                "points": 1,
                "description": "Use underscore to reference previous result"
            },
            "Q2.3a": {
                "type": "code",
                "cell_index": 17,  # b - a
                "expected_outputs": ["45"],
                "points": 1,
                "description": "First step: b - a"
            },
            "Q2.3b": {
                "type": "code",
                "cell_index": 18,  # _ // 9
                "expected_outputs": ["5"],
                "points": 1,
                "description": "Second step: divide by 9"
            },
            "Q2.3c": {
                "type": "code",
                "cell_index": 19,  # _ ** 2
                "expected_outputs": ["25"],
                "points": 1,
                "description": "Third step: square the result"
            }
        }
    },
}

# Point allocations for overall grading
POINTS = {
    "completeness": 20,  # All questions attempted
    "correctness": 40,   # Correct answers from autograder
    "pythonic": 10,      # Code quality (mostly manual, linting provides guidance)
    "iterative": 10,     # Commit history
    "knowledge": 20,     # Essay questions (manual grading)
}

TOTAL_POINTS = sum(POINTS.values())


def get_notebook_config(notebook_path: str):
    """
    Get test configuration for a specific notebook.
    
    Args:
        notebook_path: Path to notebook (relative to repo root)
        
    Returns:
        Test configuration dictionary or None if not configured
    """
    return TEST_CONFIGS.get(notebook_path, {"questions": {}})


def get_all_configured_notebooks():
    """
    Get list of all notebooks that have test configurations.
    
    Returns:
        List of notebook paths with configurations
    """
    return [nb for nb, config in TEST_CONFIGS.items() if config.get("questions")]
