"""Configuration settings for LP optimizer"""

# Default example problem - Production Planning (1997 UG Exam)
DEFAULT_OBJECTIVE = "Max Z = x + y - 50"
DEFAULT_CONSTRAINTS = """50x + 24y <= 2400
30x + 33y <= 2100
x >= 45
y >= 5"""

# Example problem description
DEFAULT_PROBLEM_DESCRIPTION = """A company makes two products (X and Y) using two machines (A and B). 
Each unit of X requires 50 minutes on machine A and 30 minutes on machine B.
Each unit of Y requires 24 minutes on machine A and 33 minutes on machine B.

Starting stock: 30 units of X, 90 units of Y
Available time: Machine A = 40 hours, Machine B = 35 hours
Demand: X = 75 units, Y = 95 units

Goal: Maximize the combined stock at the end of the week."""

# UI Configuration
THEME_COLOR = "light"
CONTAINER_SIZE = "xl"

# Solver Configuration
DEFAULT_SOLVER = "pulp"
SOLVER_TIMEOUT = 60  # seconds

# Visualization Configuration
PLOT_RESOLUTION = 400
DEFAULT_MAX_BOUND = 20
OPTIMAL_POINT_COLOR = "red"
OPTIMAL_POINT_SIZE = 15

# Export Configuration
EXPORT_FORMATS = ["svg", "png", "pdf"]
DEFAULT_EXPORT_FORMAT = "svg"

# AI Configuration
GEMINI_MODEL = "gemini-2.5-pro"
GEMINI_API_KEY = ""  # Set via environment variable
GEMINI_TEMPERATURE = 0.3  # Lower for more consistent output
GEMINI_MAX_TOKENS = 8192
GEMINI_THINKING_BUDGET = -1  # Enable thinking mode
