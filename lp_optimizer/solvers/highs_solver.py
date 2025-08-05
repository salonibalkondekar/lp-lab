"""HiGHS-based solver for linear programming problems using SciPy"""

import numpy as np
from scipy.optimize import linprog
from typing import Dict, List, Tuple

from ..utils.parser import parse_objective, parse_constraint


class MockProblem:
    """Mock problem object for visualization compatibility"""
    def __init__(self, variable_names):
        self._variables = variable_names
    
    def variables(self):
        """Return mock variables for compatibility"""
        return [type('MockVar', (), {'name': var})() for var in self._variables]


class HiGHSSolver:
    """Linear Programming solver using HiGHS via SciPy"""

    def __init__(self):
        self.solver_log = ""
        self.variables = []
        self.c = None
        self.A_ub = None
        self.b_ub = None
        self.A_eq = None
        self.b_eq = None

    def solve(
        self, objective_text: str, constraints_text: str, is_maximize: bool
    ) -> Dict:
        """
        Solve the LP problem using HiGHS (via SciPy)

        Args:
            objective_text: String representation of objective function
            constraints_text: String representation of constraints (one per line)
            is_maximize: Whether to maximize (True) or minimize (False)

        Returns:
            Dictionary containing solution results
        """
        try:
            # Parse objective (now returns constant too)
            obj_coeffs, variable_names, obj_constant = parse_objective(objective_text)
            self.variables = sorted(variable_names)  # Ensure consistent ordering
            
            # Create coefficient vector (negate if maximizing since scipy minimizes)
            self.c = np.array([obj_coeffs.get(var, 0) for var in self.variables])
            if is_maximize:
                self.c = -self.c
            
            # Initialize constraint matrices
            A_ub_list = []
            b_ub_list = []
            A_eq_list = []
            b_eq_list = []
            
            # Parse and process constraints
            constraint_lines = [
                c.strip() for c in constraints_text.strip().split("\n") if c.strip()
            ]
            parsed_constraints = []
            
            for constraint_text in constraint_lines:
                try:
                    coeffs, op, rhs = parse_constraint(constraint_text, self.variables)
                    parsed_constraints.append((coeffs, op, rhs))
                    
                    # Create constraint row
                    row = [coeffs.get(var, 0) for var in self.variables]
                    
                    if op == "<=":
                        A_ub_list.append(row)
                        b_ub_list.append(rhs)
                    elif op == ">=":
                        # Convert >= to <= by negating
                        A_ub_list.append([-x for x in row])
                        b_ub_list.append(-rhs)
                    else:  # op == "="
                        A_eq_list.append(row)
                        b_eq_list.append(rhs)
                        
                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Error parsing constraint '{constraint_text}': {str(e)}"
                    }
            
            # Convert to numpy arrays if we have constraints
            self.A_ub = np.array(A_ub_list) if A_ub_list else None
            self.b_ub = np.array(b_ub_list) if b_ub_list else None
            self.A_eq = np.array(A_eq_list) if A_eq_list else None
            self.b_eq = np.array(b_eq_list) if b_eq_list else None
            
            # Solve using HiGHS
            res = linprog(
                self.c,
                A_ub=self.A_ub,
                b_ub=self.b_ub,
                A_eq=self.A_eq,
                b_eq=self.b_eq,
                bounds=(0, None),  # All variables non-negative
                method="highs",
                options={"disp": True}
            )
            
            # Create solver log
            self.solver_log = f"HiGHS Solver Status: {res.message}\\n"
            self.solver_log += f"Iterations: {res.nit}\\n"
            self.solver_log += f"Success: {res.success}\\n"
            if hasattr(res, 'slack'):
                self.solver_log += f"\\nSlack variables: {res.slack}\\n"
            
            # Get results
            if res.success:
                solution = {var: res.x[i] for i, var in enumerate(self.variables)}
                # Adjust optimal value for maximization and add back the constant term
                optimal_value = -res.fun if is_maximize else res.fun
                optimal_value += obj_constant  # Add the constant term back
                
                return {
                    "success": True,
                    "status": "optimal",
                    "solution": solution,
                    "optimal_value": optimal_value,
                    "objective_value": optimal_value,
                    "variables": solution,
                    "variable_names": self.variables,
                    "objective_coeffs": obj_coeffs,
                    "objective_constant": obj_constant,
                    "constraints": parsed_constraints,
                    "solver_log": self.solver_log,
                    "log": self.solver_log,
                    "is_maximize": is_maximize,
                    "problem": MockProblem(self.variables),
                }
            else:
                return {
                    "success": False,
                    "status": self._get_status_string(res),
                    "solver_log": self.solver_log,
                    "log": self.solver_log,
                    "error": f"Optimization failed: {self._get_status_string(res)}",
                }
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_status_string(self, result) -> str:
        """Convert scipy result status to string"""
        if result.status == 0:
            return "optimal"
        elif result.status == 1:
            return "iteration_limit"
        elif result.status == 2:
            return "infeasible"
        elif result.status == 3:
            return "unbounded"
        else:
            return "unknown"