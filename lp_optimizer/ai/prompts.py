"""Prompt templates for LP problem formulation"""

SYSTEM_PROMPT = """You are an expert in formulating Linear Programming (LP) problems. 
Given a natural language description of an optimization problem, you must:

1. Identify the decision variables (what we need to decide)
2. Formulate the objective function (what to maximize or minimize)
3. Identify all constraints (limitations and requirements)
4. Express everything in standard LP format

Output format must be JSON with the following structure:
{
    "variables": ["x", "y"],  // List of variable names
    "variable_descriptions": {
        "x": "units of product X to produce",
        "y": "units of product Y to produce"
    },
    "objective_type": "maximize" or "minimize",
    "objective_function": "x + y - 50",  // Just the expression, no "Max Z =" prefix
    "constraints": [
        "50x + 24y <= 2400",
        "30x + 33y <= 2100",
        "x >= 45",
        "y >= 5"
    ],
    "constraint_descriptions": {
        "50x + 24y <= 2400": "Machine A time limit (40 hours = 2400 minutes)",
        "30x + 33y <= 2100": "Machine B time limit (35 hours = 2100 minutes)",
        "x >= 45": "Meet demand for product X",
        "y >= 5": "Meet demand for product Y"
    },
    "explanation": "Brief explanation of the formulation"
}

Important rules:
- Use simple variable names (x, y, z or x1, x2, x3)
- All variables are non-negative by default (don't include x >= 0 unless specifically stated)
- Convert all units consistently (e.g., hours to minutes)
- Include ALL constraints mentioned in the problem
- Be precise with coefficients and operators
"""

EXAMPLE_PROBLEMS = [
    {
        "description": """A company makes two products (X and Y) using two machines (A and B). 
Each unit of X requires 50 minutes on machine A and 30 minutes on machine B.
Each unit of Y requires 24 minutes on machine A and 33 minutes on machine B.

Starting stock: 30 units of X, 90 units of Y
Available time: Machine A = 40 hours, Machine B = 35 hours  
Demand: X = 75 units, Y = 95 units

Goal: Maximize the combined stock at the end of the week.""",
        "formulation": {
            "variables": ["x", "y"],
            "variable_descriptions": {
                "x": "units of product X to produce",
                "y": "units of product Y to produce",
            },
            "objective_type": "maximize",
            "objective_function": "x + y - 50",
            "constraints": [
                "50x + 24y <= 2400",
                "30x + 33y <= 2100",
                "x >= 45",
                "y >= 5",
            ],
            "constraint_descriptions": {
                "50x + 24y <= 2400": "Machine A time limit (40 hours = 2400 minutes)",
                "30x + 33y <= 2100": "Machine B time limit (35 hours = 2100 minutes)",
                "x >= 45": "Production must meet demand for X (75 - 30 initial stock)",
                "y >= 5": "Production must meet demand for Y (95 - 90 initial stock)",
            },
            "explanation": "The objective maximizes end-of-week stock: (x+30-75) + (y+90-95) = x + y - 50",
        },
    },
    {
        "description": """A diet problem: Create a minimum cost diet that meets nutritional requirements.
        
Foods available:
- Bread: $2 per unit, provides 30g protein, 50g carbs
- Milk: $3 per unit, provides 20g protein, 10g carbs
- Eggs: $4 per unit, provides 40g protein, 5g carbs

Daily requirements:
- At least 150g protein
- At least 100g carbs
- Maximum 5 units of any single food""",
        "formulation": {
            "variables": ["x1", "x2", "x3"],
            "variable_descriptions": {
                "x1": "units of bread",
                "x2": "units of milk",
                "x3": "units of eggs",
            },
            "objective_type": "minimize",
            "objective_function": "2x1 + 3x2 + 4x3",
            "constraints": [
                "30x1 + 20x2 + 40x3 >= 150",
                "50x1 + 10x2 + 5x3 >= 100",
                "x1 <= 5",
                "x2 <= 5",
                "x3 <= 5",
            ],
            "constraint_descriptions": {
                "30x1 + 20x2 + 40x3 >= 150": "Minimum protein requirement",
                "50x1 + 10x2 + 5x3 >= 100": "Minimum carbs requirement",
                "x1 <= 5": "Maximum bread units",
                "x2 <= 5": "Maximum milk units",
                "x3 <= 5": "Maximum eggs units",
            },
            "explanation": "Minimize cost while meeting nutritional requirements and quantity limits",
        },
    },
]
