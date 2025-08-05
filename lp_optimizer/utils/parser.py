"""Parser utilities for LP problems"""

import re
from typing import List, Tuple, Dict


def parse_objective(objective_str: str) -> Tuple[Dict[str, float], List[str], float]:
    """
    Parse objective function string like 'Max Z = 3x1 + 2x2 - 5'

    Args:
        objective_str: String representation of objective function

    Returns:
        Tuple of (coefficients dict, variables list, constant term)
    """
    # Remove 'Max' or 'Min' prefix and 'Z =' part
    clean_str = re.sub(
        r"^(Max|Min)\s+Z\s*=\s*", "", objective_str.strip(), flags=re.IGNORECASE
    )

    # Extract variables and coefficients
    terms = re.findall(r"([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)", clean_str)

    coefficients = {}
    variables = []

    for coef, var in terms:
        coef = coef.replace(" ", "")
        if coef in ["", "+"]:
            coef = "1"
        elif coef == "-":
            coef = "-1"
        coefficients[var] = float(coef)
        if var not in variables:
            variables.append(var)
    
    # Extract constant term (numbers without variables)
    # Remove all terms with variables from the string
    remaining = clean_str
    for term in re.findall(r"[+-]?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\w*", clean_str):
        remaining = remaining.replace(term, "", 1)
    
    # Clean up and find remaining constant
    remaining = remaining.strip()
    constant = 0.0
    
    if remaining:
        # Look for standalone numbers (positive or negative)
        const_match = re.search(r"[+-]?\s*\d+\.?\d*", remaining)
        if const_match:
            const_str = const_match.group().replace(" ", "")
            constant = float(const_str)

    return coefficients, variables, constant


def parse_constraint(
    constraint_str: str, variables: List[str]
) -> Tuple[Dict[str, float], str, float]:
    """
    Parse constraint string like '2x1 + x2 <= 8' or 'x2 >= 3x1'
    
    Handles variables on both sides of the constraint by moving all
    variables to the left side and constants to the right.

    Args:
        constraint_str: String representation of constraint
        variables: List of variable names

    Returns:
        Tuple of (coefficients dict, operator, rhs value)
    """
    # Split by inequality/equality
    match = re.match(r"(.+?)\s*(<=|>=|=)\s*(.+)", constraint_str)
    if not match:
        raise ValueError(f"Invalid constraint format: {constraint_str}")

    lhs, operator, rhs = match.groups()

    # Parse left-hand side
    lhs_terms = re.findall(r"([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)", lhs)
    
    coefficients = {var: 0.0 for var in variables}
    
    # Add LHS variable terms
    for coef, var in lhs_terms:
        coef = coef.replace(" ", "")
        if coef in ["", "+"]:
            coef = "1"
        elif coef == "-":
            coef = "-1"
        if var in variables:
            coefficients[var] = float(coef)
    
    # Parse right-hand side for both variables and constants
    rhs_terms = re.findall(r"([+-]?\s*\d*\.?\d*)\s*\*?\s*([a-zA-Z]\w*)", rhs)
    rhs_constant = 0.0
    
    # Process RHS variable terms (subtract from LHS)
    for coef, var in rhs_terms:
        coef = coef.replace(" ", "")
        if coef in ["", "+"]:
            coef = "1"
        elif coef == "-":
            coef = "-1"
        if var in variables:
            # Move variable to left side (subtract from existing coefficient)
            coefficients[var] -= float(coef)
    
    # Extract constant term from RHS
    # Remove all variable terms from RHS to find the constant
    rhs_remaining = rhs.strip()
    for term in re.findall(r"[+-]?\s*\d*\.?\d*\s*\*?\s*[a-zA-Z]\w*", rhs):
        rhs_remaining = rhs_remaining.replace(term, "", 1)
    
    # Clean up and find remaining constant
    rhs_remaining = rhs_remaining.strip()
    
    # If there's a standalone number, use it as the constant
    if rhs_remaining:
        # Try to parse as a number
        try:
            rhs_constant = float(rhs_remaining)
        except ValueError:
            # If it's not a valid number, check for patterns like "+5" or "-3"
            const_match = re.search(r"[+-]?\s*\d+\.?\d*", rhs_remaining)
            if const_match:
                rhs_constant = float(const_match.group().replace(" ", ""))
    else:
        # If no constant found and only variables, RHS constant is 0
        # (This handles cases like "x2 >= 3x1" which becomes "x2 - 3x1 >= 0")
        rhs_constant = 0.0

    return coefficients, operator, rhs_constant
