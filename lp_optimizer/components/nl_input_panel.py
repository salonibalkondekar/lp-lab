"""Natural language input panel component"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from ..config import DEFAULT_PROBLEM_DESCRIPTION
from ..utils.logger import get_logger, LPLogger

# Get logger for this module
logger = get_logger("ui.nl_input_panel")


def create_nl_input_panel():
    """Create the natural language input panel"""
    logger.info("Creating natural language input panel")
    
    # Create problem input textarea
    LPLogger.log_component_creation(logger, "nl-problem-input", "nl-problem-input")
    problem_input = dmc.Textarea(
        id="nl-problem-input",
        label="Problem Description",
        description="Describe what you want to optimize, the constraints, and available resources",
        placeholder="Example: A factory produces two products...",
        value=DEFAULT_PROBLEM_DESCRIPTION,
        minRows=10,
        maxRows=20,
        autosize=True,
    )
    
    # Create example problem selector
    LPLogger.log_component_creation(logger, "example-problem-select", "example-problem-select")
    example_select = dmc.Select(
        id="example-problem-select",
        label="Load Example Problem",
        placeholder="Choose an example...",
        data=[
            {"value": "production", "label": "Production Planning"},
            {"value": "diet", "label": "Diet Problem"},
            {"value": "transportation", "label": "Transportation"},
            {"value": "portfolio", "label": "Portfolio Optimization"},
            {"value": "custom", "label": "Custom Problem"},
        ],
        value="production",
        clearable=False,
        leftSection=DashIconify(icon="tabler:bookmark"),
    )
    
    # Create formulate button
    LPLogger.log_component_creation(logger, "formulate-button", "formulate-button")
    logger.info("⚠️ Creating FORMULATE BUTTON with id='formulate-button'")
    formulate_button = dmc.Button(
        "Formulate with AI",
        id="formulate-button",
        leftSection=DashIconify(icon="tabler:sparkles"),
        fullWidth=True,
        size="lg",
        variant="gradient",
        gradient={"from": "violet", "to": "cyan"},
        loading=False,
    )
    logger.debug(f"Formulate button properties: fullWidth=True, size=lg, variant=gradient")
    
    return dmc.Stack(
        [
            # Description
            dmc.Alert(
                "Describe your optimization problem in plain English. Our AI will convert it to LP format!",
                title="AI-Powered Formulation",
                color="blue",
                icon=DashIconify(icon="tabler:robot"),
            ),
            problem_input,
            example_select,
            formulate_button,
            # Results display (initially hidden)
            dmc.Container(
                id="formulation-results",
                children=[],
                p=0,
            ),
        ],
        gap="md",
    )


def create_formulation_results(formulation_data):
    """Create the formulation results display"""
    logger.info("Creating formulation results display")
    if not formulation_data or not formulation_data.get("success"):
        logger.debug("No successful formulation data to display")
        return []

    # Extract data
    variables = formulation_data.get("variables", [])
    var_desc = formulation_data.get("variable_descriptions", {})
    constraint_desc = formulation_data.get("constraint_descriptions", {})
    explanation = formulation_data.get("explanation", "")
    
    # Log button creation
    logger.info("⚠️ Creating COPY-TO-MANUAL BUTTON with id='copy-to-manual-button'")

    return dmc.Stack(
        [
            dmc.Divider(label="AI Formulation Results", labelPosition="center"),
            # Explanation
            dmc.Alert(
                explanation,
                title="Formulation Explanation",
                color="green",
                icon=DashIconify(icon="tabler:info-circle"),
            ),
            # Variables
            dmc.Paper(
                shadow="xs",
                p="md",
                children=[
                    dmc.Title("Decision Variables", order=5),
                    dmc.List(
                        [
                            dmc.ListItem(f"{var} = {desc}")
                            for var, desc in var_desc.items()
                        ]
                    ),
                ],
            ),
            # Constraints explanation
            dmc.Paper(
                shadow="xs",
                p="md",
                children=[
                    dmc.Title("Constraints Explanation", order=5),
                    dmc.List(
                        [
                            dmc.ListItem(f"{constraint}: {desc}")
                            for constraint, desc in constraint_desc.items()
                        ]
                    ),
                ],
            ),
            # Copy to manual input button
            dmc.Button(
                "Use in Manual Input",
                id="copy-to-manual-button",
                leftSection=DashIconify(icon="tabler:copy"),
                variant="light",
                fullWidth=True,
            ),
        ],
        gap="md",
    )
