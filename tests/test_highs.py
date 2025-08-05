#!/usr/bin/env python3
"""Test the HiGHS solver implementation"""

from lp_optimizer.solvers.highs_solver import HiGHSSolver

# Test with the example problem from the user
objective = "x + y - 50"
constraints = """50x + 24y <= 2400
30x + 33y <= 2100
x >= 45
y >= 5"""

print("Testing HiGHS solver with example problem...")
print(f"Objective: Maximize {objective}")
print(f"Constraints:\n{constraints}\n")

# Create and run solver
solver = HiGHSSolver()
result = solver.solve(objective, constraints, is_maximize=True)

# Display results
if result.get("success"):
    print("✓ Optimization successful!")
    print(f"Status: {result['status']}")
    print(f"Optimal value: {result['optimal_value']:.2f}")
    print("\nOptimal solution:")
    for var, value in result['solution'].items():
        print(f"  {var} = {value:.2f}")
    print(f"\nEnd-of-week stock: {result['optimal_value']:.2f} units")
    print(f"HiGHS iterations: {result['solver_log'].split('Iterations: ')[1].split('\\n')[0]}")
else:
    print(f"✗ Optimization failed: {result.get('error', 'Unknown error')}")
    print(f"Status: {result.get('status', 'Unknown')}")

# Test that the mock problem object works
if result.get("success") and result.get("problem"):
    print(f"\n✓ Mock problem object created with {len(result['problem'].variables())} variables")