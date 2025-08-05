#!/usr/bin/env python3
"""Compare results from both solvers"""

from lp_optimizer.solvers.pulp_solver import PuLPSolver
from lp_optimizer.solvers.highs_solver import HiGHSSolver

# Test problem
objective = "x + y - 50"
constraints = """50x + 24y <= 2400
30x + 33y <= 2100
x >= 45
y >= 5"""

print("Testing both solvers with the same problem...")
print(f"Objective: Maximize {objective}")
print(f"Constraints:\n{constraints}\n")
print("-" * 60)

# Test PuLP solver
print("\n1. PuLP Solver (CBC):")
pulp_solver = PuLPSolver()
pulp_result = pulp_solver.solve(objective, constraints, is_maximize=True)

if pulp_result.get("success"):
    print(f"   Status: {pulp_result['status']}")
    print(f"   Optimal value: {pulp_result['optimal_value']:.2f}")
    print("   Solution:")
    for var, value in sorted(pulp_result['solution'].items()):
        print(f"     {var} = {value:.2f}")
else:
    print(f"   Failed: {pulp_result.get('error')}")

# Test HiGHS solver
print("\n2. HiGHS Solver (SciPy):")
highs_solver = HiGHSSolver()
highs_result = highs_solver.solve(objective, constraints, is_maximize=True)

if highs_result.get("success"):
    print(f"   Status: {highs_result['status']}")
    print(f"   Optimal value: {highs_result['optimal_value']:.2f}")
    print("   Solution:")
    for var, value in sorted(highs_result['solution'].items()):
        print(f"     {var} = {value:.2f}")
else:
    print(f"   Failed: {highs_result.get('error')}")

# Compare results
print("\n" + "-" * 60)
print("\nComparison:")
if pulp_result.get("success") and highs_result.get("success"):
    pulp_val = pulp_result['optimal_value']
    highs_val = highs_result['optimal_value']
    diff = abs(pulp_val - highs_val)
    
    print(f"✓ Both solvers found optimal solutions")
    print(f"  PuLP optimal value:  {pulp_val:.6f}")
    print(f"  HiGHS optimal value: {highs_val:.6f}")
    print(f"  Difference: {diff:.6f} ({diff/max(pulp_val, highs_val)*100:.2f}%)")
    
    # Check if solutions match
    match = True
    for var in sorted(pulp_result['solution'].keys()):
        pulp_var = pulp_result['solution'][var]
        highs_var = highs_result['solution'].get(var, 0)
        var_diff = abs(pulp_var - highs_var)
        if var_diff > 1e-6:
            match = False
            print(f"  Variable {var}: PuLP={pulp_var:.6f}, HiGHS={highs_var:.6f}, diff={var_diff:.6f}")
    
    if match:
        print("\n✓ Solutions match perfectly!")
else:
    print("✗ One or both solvers failed")