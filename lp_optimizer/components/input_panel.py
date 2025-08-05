"""Input panel component for LP problems"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify

from ..config import DEFAULT_OBJECTIVE, DEFAULT_CONSTRAINTS
from .nl_input_panel import create_nl_input_panel
from ..utils.logger import get_logger, LPLogger

# Get logger for this module
logger = get_logger("ui.input_panel")


def create_manual_input_tab():
    """Create the manual input form"""
    logger.info("Creating manual input tab")
    
    # Create objective type select
    LPLogger.log_component_creation(logger, "objective-type-select", "objective-type-select")
    objective_select = dmc.Select(
        id="objective-type-select",
        label="Optimization Type",
        value="maximize",
        data=[
            {"label": "Maximize", "value": "maximize"},
            {"label": "Minimize", "value": "minimize"},
        ],
        mb="md",
    )
    
    # Create solver select
    LPLogger.log_component_creation(logger, "solver-select", "solver-select")
    solver_select = dmc.Select(
        id="solver-select",
        label="Solver",
        value="highs",
        data=[
            {"label": "HiGHS (SciPy)", "value": "highs"},
            {"label": "PuLP (CBC)", "value": "pulp"},
        ],
        mb="md",
    )
    
    # Create objective input
    LPLogger.log_component_creation(logger, "objective-input", "objective-input")
    objective_input = dmc.TextInput(
        id="objective-input",
        label="Objective Function",
        placeholder="e.g., Max Z = 40x1 + 30x2",
        value=DEFAULT_OBJECTIVE,
        leftSection=DashIconify(icon="tabler:target"),
        mb="md",
    )
    
    # Create constraints input
    LPLogger.log_component_creation(logger, "constraints-input", "constraints-input")
    constraints_input = dmc.Textarea(
        id="constraints-input",
        label="Constraints (one per line)",
        placeholder="e.g.,\n2x1 + x2 <= 100\nx1 + x2 <= 80\nx1 <= 40\nx1 >= 0\nx2 >= 0",
        value=DEFAULT_CONSTRAINTS,
        minRows=6,
        leftSection=DashIconify(icon="tabler:list-check"),
        mb="md",
    )
    
    # Create solve button
    LPLogger.log_component_creation(logger, "solve-button", "solve-button")
    logger.info("⚠️ Creating SOLVE BUTTON with id='solve-button'")
    solve_button = dmc.Button(
        "Solve Problem",
        id="solve-button",
        leftSection=DashIconify(icon="tabler:calculator"),
        fullWidth=True,
        size="lg",
        variant="gradient",
        gradient={"from": "indigo", "to": "cyan"},
    )
    logger.debug(f"Solve button properties: fullWidth=True, size=lg, variant=gradient")
    
    return dmc.Stack(
        [
            objective_select,
            solver_select,
            objective_input,
            constraints_input,
            solve_button,
        ]
    )


def create_input_panel():
    """Create the problem input panel with tabs"""
    logger.info("="*60)
    logger.info("Creating main input panel with tabs")
    logger.info("="*60)
    
    LPLogger.log_component_creation(logger, "input-mode-tabs", "input-mode-tabs")
    
    return dmc.Paper(
        shadow="sm",
        p="md",
        radius="md",
        children=[
            dmc.Title("Problem Input", order=3, mb="md"),
            # Tabs for manual vs AI input
            dmc.Tabs(
                [
                    dmc.TabsList(
                        [
                            dmc.TabsTab(
                                "Manual Input",
                                value="manual",
                                leftSection=DashIconify(icon="tabler:pencil"),
                            ),
                            dmc.TabsTab(
                                "AI Assistant",
                                value="ai",
                                leftSection=DashIconify(icon="tabler:robot"),
                            ),
                        ]
                    ),
                    dmc.TabsPanel(
                        value="manual",
                        children=create_manual_input_tab(),
                    ),
                    dmc.TabsPanel(
                        value="ai",
                        children=create_nl_input_panel(),
                    ),
                ],
                value="manual",
                id="input-mode-tabs",
            ),
        ],
    )
