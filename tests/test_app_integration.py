#!/usr/bin/env python3
"""Integration test for the LP optimizer app with both solvers"""

import sys
import time
from dash.testing.application_runners import import_app


def test_app_with_both_solvers():
    """Test the app with both PuLP and HiGHS solvers"""
    print("Testing LP Optimizer App Integration...")
    
    try:
        # Import the app
        app = import_app("lp_optimizer.app")
        print("✓ App imported successfully")
        
        # Check that all expected components exist
        layout = app.layout
        print("✓ App layout loaded")
        
        # Test callback registration
        callback_count = len(app.callback_map)
        print(f"✓ {callback_count} callbacks registered")
        
        # Test solver imports
        from lp_optimizer.solvers import PuLPSolver
        from lp_optimizer.solvers.highs_solver import HiGHSSolver
        print("✓ Both solvers imported successfully")
        
        # Quick solver test
        test_objective = "x + y"
        test_constraints = "x + y <= 10\nx >= 0\ny >= 0"
        
        pulp_solver = PuLPSolver()
        pulp_result = pulp_solver.solve(test_objective, test_constraints, True)
        print(f"✓ PuLP solver works: optimal_value = {pulp_result['optimal_value']}")
        
        highs_solver = HiGHSSolver()
        highs_result = highs_solver.solve(test_objective, test_constraints, True)
        print(f"✓ HiGHS solver works: optimal_value = {highs_result['optimal_value']}")
        
        # Verify results match
        assert abs(pulp_result['optimal_value'] - highs_result['optimal_value']) < 0.001
        print("✓ Both solvers produce consistent results")
        
        print("\n✅ All integration tests passed!")
        print("\nYou can now run the app with: python main.py")
        print("The app will be available at http://localhost:8050")
        print("\nFeatures:")
        print("- Manual input mode with solver selection (HiGHS or PuLP)")
        print("- AI assistant mode for natural language problem input")
        print("- Graphical visualization of 2D problems")
        print("- Solver log display")
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    test_app_with_both_solvers()