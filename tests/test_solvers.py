#!/usr/bin/env python3
"""Comprehensive test suite for LP solvers"""

import unittest
from lp_optimizer.solvers.pulp_solver import PuLPSolver
from lp_optimizer.solvers.highs_solver import HiGHSSolver


class TestLPSolvers(unittest.TestCase):
    """Test cases for both PuLP and HiGHS solvers"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.pulp_solver = PuLPSolver()
        self.highs_solver = HiGHSSolver()
        self.tolerance = 1e-4
    
    def test_example_problem(self):
        """Test the example problem from the documentation"""
        objective = "x + y - 50"
        constraints = """50x + 24y <= 2400
30x + 33y <= 2100
x >= 45
y >= 5"""
        
        # Test PuLP
        pulp_result = self.pulp_solver.solve(objective, constraints, is_maximize=True)
        self.assertTrue(pulp_result['success'])
        self.assertEqual(pulp_result['status'], 'optimal')
        self.assertAlmostEqual(pulp_result['optimal_value'], 51.25, places=2)
        self.assertAlmostEqual(pulp_result['solution']['x'], 45.0, places=2)
        self.assertAlmostEqual(pulp_result['solution']['y'], 6.25, places=2)
        
        # Test HiGHS
        highs_result = self.highs_solver.solve(objective, constraints, is_maximize=True)
        self.assertTrue(highs_result['success'])
        self.assertEqual(highs_result['status'], 'optimal')
        self.assertAlmostEqual(highs_result['optimal_value'], 51.25, places=2)
        self.assertAlmostEqual(highs_result['solution']['x'], 45.0, places=2)
        self.assertAlmostEqual(highs_result['solution']['y'], 6.25, places=2)
        
        # Compare results
        self.assertAlmostEqual(
            pulp_result['optimal_value'], 
            highs_result['optimal_value'], 
            delta=self.tolerance
        )
    
    def test_simple_maximization(self):
        """Test a simple maximization problem"""
        objective = "3x + 2y"
        constraints = """x + y <= 4
2x + y <= 5
x >= 0
y >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=True)
            self.assertTrue(result['success'])
            self.assertEqual(result['status'], 'optimal')
            # Optimal solution should be x=1, y=3 with value 9
            self.assertAlmostEqual(result['optimal_value'], 9.0, delta=self.tolerance)
            self.assertAlmostEqual(result['solution']['x'], 1.0, delta=self.tolerance)
            self.assertAlmostEqual(result['solution']['y'], 3.0, delta=self.tolerance)
    
    def test_simple_minimization(self):
        """Test a simple minimization problem"""
        objective = "2x + 3y"
        constraints = """x + 2y >= 4
x + y >= 3
x >= 0
y >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=False)
            self.assertTrue(result['success'])
            self.assertEqual(result['status'], 'optimal')
            # Optimal solution should be x=2, y=1 with value 7
            self.assertAlmostEqual(result['optimal_value'], 7.0, delta=self.tolerance)
            self.assertAlmostEqual(result['solution']['x'], 2.0, delta=self.tolerance)
            self.assertAlmostEqual(result['solution']['y'], 1.0, delta=self.tolerance)
    
    def test_infeasible_problem(self):
        """Test an infeasible problem"""
        objective = "x + y"
        constraints = """x + y <= 1
x + y >= 2
x >= 0
y >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=True)
            self.assertFalse(result['success'])
            self.assertIn(result['status'], ['infeasible', 'not_solved'])
    
    def test_unbounded_problem(self):
        """Test an unbounded problem"""
        objective = "x + y"
        constraints = """x - y >= 1
x >= 0
y >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=True)
            # Some solvers might find a large solution rather than detecting unboundedness
            if result['success']:
                # If it found a solution, it should be very large
                self.assertGreater(result['optimal_value'], 1000)
            else:
                self.assertEqual(result['status'], 'unbounded')
    
    def test_equality_constraints(self):
        """Test problem with equality constraints"""
        objective = "2x + 3y"
        constraints = """x + y = 10
2x + y <= 15
x >= 0
y >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=True)
            self.assertTrue(result['success'])
            self.assertEqual(result['status'], 'optimal')
            # Solution should satisfy x + y = 10
            self.assertAlmostEqual(
                result['solution']['x'] + result['solution']['y'], 
                10.0, 
                delta=self.tolerance
            )
    
    def test_negative_coefficients(self):
        """Test problem with negative coefficients"""
        objective = "5x - 2y"
        constraints = """x + y <= 10
-x + 2y <= 8
x >= 0
y >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=True)
            self.assertTrue(result['success'])
            self.assertEqual(result['status'], 'optimal')
            # Optimal solution should be x=10, y=0 with value 50
            self.assertAlmostEqual(result['optimal_value'], 50.0, delta=self.tolerance)
            self.assertAlmostEqual(result['solution']['x'], 10.0, delta=self.tolerance)
            self.assertAlmostEqual(result['solution']['y'], 0.0, delta=self.tolerance)
    
    def test_multiple_variables(self):
        """Test problem with more than 2 variables"""
        objective = "x + 2y + 3z"
        constraints = """x + y + z <= 10
2x + y + z <= 12
x + 2y + z <= 11
x >= 0
y >= 0
z >= 0"""
        
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve(objective, constraints, is_maximize=True)
            self.assertTrue(result['success'])
            self.assertEqual(result['status'], 'optimal')
            # Verify all variables are non-negative
            for var in ['x', 'y', 'z']:
                self.assertGreaterEqual(result['solution'][var], -self.tolerance)
    
    def test_solver_specific_features(self):
        """Test solver-specific return values"""
        objective = "2x + y"
        constraints = """x + y <= 5
x >= 0
y >= 0"""
        
        # Test PuLP specific features
        pulp_result = self.pulp_solver.solve(objective, constraints, is_maximize=True)
        self.assertIn('problem', pulp_result)
        self.assertIn('log', pulp_result)
        self.assertIsNotNone(pulp_result['problem'])
        
        # Test HiGHS specific features
        highs_result = self.highs_solver.solve(objective, constraints, is_maximize=True)
        self.assertIn('problem', highs_result)
        self.assertIn('log', highs_result)
        # Mock problem should have variables method
        self.assertTrue(hasattr(highs_result['problem'], 'variables'))
        self.assertTrue(callable(highs_result['problem'].variables))
    
    def test_error_handling(self):
        """Test error handling for malformed inputs"""
        # Test invalid objective
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve("invalid objective", "x >= 0", True)
            self.assertFalse(result['success'])
            self.assertIn('error', result)
        
        # Test invalid constraints
        for solver in [self.pulp_solver, self.highs_solver]:
            result = solver.solve("x + y", "invalid constraint", True)
            self.assertFalse(result['success'])
            self.assertIn('error', result)


class TestSolverConsistency(unittest.TestCase):
    """Test that both solvers produce consistent results"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.pulp_solver = PuLPSolver()
        self.highs_solver = HiGHSSolver()
        self.tolerance = 1e-3
    
    def compare_results(self, objective, constraints, is_maximize):
        """Helper to compare results from both solvers"""
        pulp_result = self.pulp_solver.solve(objective, constraints, is_maximize)
        highs_result = self.highs_solver.solve(objective, constraints, is_maximize)
        
        # Both should succeed or both should fail
        self.assertEqual(pulp_result['success'], highs_result['success'])
        
        if pulp_result['success'] and highs_result['success']:
            # Compare optimal values
            self.assertAlmostEqual(
                pulp_result['optimal_value'],
                highs_result['optimal_value'],
                delta=self.tolerance,
                msg=f"Optimal values differ: PuLP={pulp_result['optimal_value']}, HiGHS={highs_result['optimal_value']}"
            )
            
            # Compare solutions
            for var in pulp_result['solution']:
                self.assertAlmostEqual(
                    pulp_result['solution'][var],
                    highs_result['solution'][var],
                    delta=self.tolerance,
                    msg=f"Variable {var} differs: PuLP={pulp_result['solution'][var]}, HiGHS={highs_result['solution'][var]}"
                )
    
    def test_consistency_basic_problems(self):
        """Test consistency on basic problems"""
        test_cases = [
            # (objective, constraints, is_maximize)
            ("2x + 3y", "x + y <= 10\nx >= 0\ny >= 0", True),
            ("x + y", "2x + y >= 10\nx + 2y >= 8\nx >= 0\ny >= 0", False),
            ("3x + 4y + 2z", "x + y + z <= 10\n2x + y <= 15\nx >= 0\ny >= 0\nz >= 0", True),
        ]
        
        for objective, constraints, is_maximize in test_cases:
            with self.subTest(objective=objective):
                self.compare_results(objective, constraints, is_maximize)


if __name__ == '__main__':
    unittest.main(verbosity=2)