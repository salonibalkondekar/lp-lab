"""Library of example LP problems"""

EXAMPLE_PROBLEMS_LIBRARY = {
    "production": {
        "title": "Production Planning",
        "description": """A company makes two products (X and Y) using two machines (A and B). 
Each unit of X requires 50 minutes on machine A and 30 minutes on machine B.
Each unit of Y requires 24 minutes on machine A and 33 minutes on machine B.

Starting stock: 30 units of X, 90 units of Y
Available time: Machine A = 40 hours, Machine B = 35 hours
Demand: X = 75 units, Y = 95 units

Goal: Maximize the combined stock at the end of the week.""",
        "objective": "Max Z = x + y - 50",
        "constraints": """50x + 24y <= 2400
30x + 33y <= 2100
x >= 45
y >= 5""",
    },
    "diet": {
        "title": "Diet Problem",
        "description": """Create a minimum cost diet that meets nutritional requirements.
        
Foods available:
- Bread: $2 per unit, provides 30g protein, 50g carbs
- Milk: $3 per unit, provides 20g protein, 10g carbs  
- Eggs: $4 per unit, provides 40g protein, 5g carbs

Daily requirements:
- At least 150g protein
- At least 100g carbs
- Maximum 5 units of any single food

Goal: Minimize the total cost while meeting all nutritional requirements.""",
        "objective": "Min Z = 2x1 + 3x2 + 4x3",
        "constraints": """30x1 + 20x2 + 40x3 >= 150
50x1 + 10x2 + 5x3 >= 100
x1 <= 5
x2 <= 5
x3 <= 5""",
    },
    "transportation": {
        "title": "Transportation Problem",
        "description": """A company has two warehouses and three retail stores.

Warehouse capacities:
- Warehouse A: 100 units
- Warehouse B: 150 units

Store demands:
- Store 1: 80 units
- Store 2: 70 units
- Store 3: 90 units

Shipping costs per unit:
- From A to Store 1: $5, Store 2: $7, Store 3: $9
- From B to Store 1: $8, Store 2: $4, Store 3: $6

Goal: Minimize total shipping cost while meeting all store demands.""",
        "objective": "Min Z = 5x11 + 7x12 + 9x13 + 8x21 + 4x22 + 6x23",
        "constraints": """x11 + x12 + x13 <= 100
x21 + x22 + x23 <= 150
x11 + x21 >= 80
x12 + x22 >= 70
x13 + x23 >= 90""",
    },
    "portfolio": {
        "title": "Portfolio Optimization",
        "description": """An investor has $10,000 to invest in three assets.

Asset details:
- Stock A: Expected return 12%, maximum investment $6,000
- Stock B: Expected return 9%, maximum investment $4,000
- Bonds C: Expected return 5%, no limit

Risk constraints:
- At least 30% must be in bonds
- No more than 50% in any single stock

Goal: Maximize expected return.""",
        "objective": "Max Z = 0.12x1 + 0.09x2 + 0.05x3",
        "constraints": """x1 + x2 + x3 <= 10000
x1 <= 6000
x2 <= 4000
x3 >= 3000
x1 <= 5000
x2 <= 5000""",
    },
    "custom": {
        "title": "Custom Problem",
        "description": """Enter your own optimization problem here.

Describe:
- What you're trying to optimize (maximize profit, minimize cost, etc.)
- The decision variables (what needs to be decided)
- The constraints (limitations, requirements, etc.)
- Any specific conditions or requirements

Be as detailed as possible for better AI formulation.""",
        "objective": "",
        "constraints": "",
    },
}
