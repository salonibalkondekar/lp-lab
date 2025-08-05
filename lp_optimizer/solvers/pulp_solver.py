"""PuLP-based solver for linear programming problems"""

import pulp
import tempfile
import os
from typing import Dict, List, Tuple

from ..utils.parser import parse_objective, parse_constraint


class PuLPSolver:
    """Linear Programming solver using PuLP library"""

    def __init__(self):
        self.prob = None
        self.variables = {}
        self.solver_log = ""

    def solve(
        self, objective_text: str, constraints_text: str, is_maximize: bool
    ) -> Dict:
        """
        Solve the LP problem using PuLP

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

            # Create PuLP problem
            if is_maximize:
                self.prob = pulp.LpProblem("LP_Problem", pulp.LpMaximize)
            else:
                self.prob = pulp.LpProblem("LP_Problem", pulp.LpMinimize)

            # Create variables (non-negative by default)
            self.variables = {
                var: pulp.LpVariable(var, lowBound=0) for var in variable_names
            }

            # Set objective
            self.prob += pulp.lpSum(
                [obj_coeffs.get(var, 0) * self.variables[var] for var in variable_names]
            )

            # Parse and add constraints
            constraint_lines = [
                c.strip() for c in constraints_text.strip().split("\n") if c.strip()
            ]
            parsed_constraints = []

            for constraint_text in constraint_lines:
                try:
                    coeffs, op, rhs = parse_constraint(constraint_text, variable_names)
                    parsed_constraints.append((coeffs, op, rhs))

                    # Add to PuLP problem
                    lhs_expr = pulp.lpSum(
                        [coeffs[var] * self.variables[var] for var in variable_names]
                    )

                    if op == "<=":
                        self.prob += lhs_expr <= rhs
                    elif op == ">=":
                        self.prob += lhs_expr >= rhs
                    else:  # op == '='
                        self.prob += lhs_expr == rhs

                except Exception as e:
                    return {
                        "success": False,
                        "error": f"Error parsing constraint '{constraint_text}': {str(e)}"
                    }

            # Solve the problem
            self._solve_with_logging()

            # Get results
            if self.prob.status == pulp.LpStatusOptimal:
                solution = {var: self.variables[var].varValue for var in variable_names}
                optimal_value = pulp.value(self.prob.objective)
                # Add the constant term back to the objective value
                optimal_value += obj_constant

                return {
                    "success": True,
                    "status": "optimal",
                    "solution": solution,
                    "optimal_value": optimal_value,
                    "objective_value": optimal_value,
                    "variables": solution,
                    "variable_names": variable_names,
                    "objective_coeffs": obj_coeffs,
                    "objective_constant": obj_constant,
                    "constraints": parsed_constraints,
                    "solver_log": self.solver_log,
                    "log": self.solver_log,
                    "is_maximize": is_maximize,
                    "problem": self.prob,
                }
            else:
                return {
                    "success": False,
                    "status": self._get_status_string(),
                    "solver_log": self.solver_log,
                    "log": self.solver_log,
                    "error": f"Optimization failed: {self._get_status_string()}",
                }

        except Exception as e:
            return {"success": False, "error": str(e)}

    def _solve_with_logging(self):
        """Solve the problem and capture solver output"""
        with tempfile.NamedTemporaryFile(
            mode="w+", delete=False, suffix=".log"
        ) as tmp_log:
            log_path = tmp_log.name

        try:
            self.prob.solve(pulp.PULP_CBC_CMD(msg=True, logPath=log_path))

            # Read the log file
            with open(log_path, "r") as f:
                self.solver_log = f.read()
        finally:
            # Clean up the temporary file
            if os.path.exists(log_path):
                os.remove(log_path)

    def _get_status_string(self) -> str:
        """Convert PuLP status to string"""
        status_map = {
            pulp.LpStatusNotSolved: "not_solved",
            pulp.LpStatusInfeasible: "infeasible",
            pulp.LpStatusUnbounded: "unbounded",
            pulp.LpStatusUndefined: "undefined",
        }
        return status_map.get(self.prob.status, "unknown")
