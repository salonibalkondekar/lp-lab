"""Main application module for LP optimizer"""

import re
import os
from dash import Dash, callback, Output, Input, State, no_update, dcc, ctx
import dash_mantine_components as dmc
from dash_iconify import DashIconify
from .utils.logger import get_logger, LPLogger

from .components import (
    create_input_panel,
    create_results_panel,
    create_solution_display,
    create_visualization_panel,
    create_solver_log_panel,
    create_formulation_results,
)
from .solvers import PuLPSolver
from .solvers.highs_solver import HiGHSSolver
from .visualization import LPPlotter
from .ai import LPFormulator
from .examples import EXAMPLE_PROBLEMS_LIBRARY

# Get logger for app module
logger = get_logger("app")


def create_app():
    """Create and configure the Dash application"""
    logger.info("Creating Dash application")
    logger.debug("Initializing with Mantine components")
    
    app = Dash(__name__, external_stylesheets=[dmc.styles.ALL], suppress_callback_exceptions=True)
    logger.debug("Dash app instance created with suppress_callback_exceptions=True")

    app.layout = dmc.MantineProvider(
        theme={"colorScheme": "light"},
        children=[
            dmc.Container(
                size="xl",
                py="md",
                children=[
                    # Header
                    dmc.Title(
                        "Linear Programming Optimizer", order=1, ta="center", mb="xl"
                    ),
                    dmc.Text(
                        "Solve linear programming problems with an intuitive interface",
                        size="lg",
                        c="dimmed",
                        ta="center",
                        mb="xl",
                    ),
                    # Main content grid
                    dmc.Grid(
                        children=[
                            # Input Panel
                            dmc.GridCol(
                                span={"base": 12, "sm": 12, "md": 6},
                                children=[create_input_panel()],
                            ),
                            # Results Panel
                            dmc.GridCol(
                                span={"base": 12, "sm": 12, "md": 6},
                                children=[
                                    dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        radius="md",
                                        children=[
                                            dmc.Title("Solution", order=3, mb="md"),
                                            dmc.LoadingOverlay(
                                                visible=False,
                                                id="loading-overlay",
                                            ),
                                            dmc.Container(id="results-container", p=0),
                                        ],
                                    )
                                ],
                            ),
                            # Visualization Panel
                            dmc.GridCol(
                                span=12,
                                children=[
                                    dmc.Paper(
                                        shadow="sm",
                                        p="md",
                                        radius="md",
                                        children=[
                                            dmc.Title("Graphical Solution", order=3, mb="md"),
                                            dcc.Graph(id="feasible-region-plot", config={"displayModeBar": False}),
                                        ],
                                    )
                                ],
                            ),
                            # Solver Log Panel
                            dmc.GridCol(
                                span=12,
                                children=[
                                    dmc.Accordion(
                                        children=[
                                            dmc.AccordionItem(
                                                value="solver-log",
                                                children=[
                                                    dmc.AccordionControl(
                                                        "Solver Log",
                                                        icon=DashIconify(icon="tabler:terminal-2"),
                                                    ),
                                                    dmc.AccordionPanel(
                                                        dmc.ScrollArea(
                                                            h=200,
                                                            children=[
                                                                dmc.Code(
                                                                    id="solver-log-content",
                                                                    block=True,
                                                                    children="",
                                                                )
                                                            ],
                                                        )
                                                    ),
                                                ],
                                            )
                                        ]
                                    )
                                ],
                            ),
                        ]
                    ),
                    # Store for solution data
                    dcc.Store(id="solution-store"),
                    dcc.Store(id="ai-formulation-store"),
                ],
            )
        ],
    )

    # Register callbacks
    logger.info("Registering callbacks...")
    register_callbacks(app)
    logger.info("✅ All callbacks registered successfully")

    return app


def register_callbacks(app):
    """Register all callbacks for the application"""
    logger.info("Starting callback registration")
    callback_count = 0

    # Callback 1: Main solve problem callback
    LPLogger.log_callback_registration(
        logger, 
        "solve_problem",
        inputs=["solve-button.n_clicks"],
        outputs=[
            "solution-store.data",
            "loading-overlay.visible",
            "objective-input.error",
            "constraints-input.error"
        ],
        states=[
            "objective-input.value",
            "constraints-input.value",
            "objective-type-select.value",
            "solver-select.value"
        ]
    )
    @callback(
        Output("solution-store", "data"),
        Output("loading-overlay", "visible"),
        Output("objective-input", "error"),
        Output("constraints-input", "error"),
        Input("solve-button", "n_clicks"),
        State("objective-input", "value"),
        State("constraints-input", "value"),
        State("objective-type-select", "value"),
        State("solver-select", "value"),
        prevent_initial_call=True,
    )
    def solve_problem(n_clicks, objective, constraints, objective_type, solver_type):
        """Solve the LP problem and update the UI"""
        logger.info(f"🎯 solve_problem callback triggered (n_clicks={n_clicks})")
        logger.debug(f"  Objective: {objective}")
        logger.debug(f"  Constraints: {constraints}")
        logger.debug(f"  Type: {objective_type}, Solver: {solver_type}")
        
        if not n_clicks or not objective or not constraints:
            logger.debug("Missing required inputs, returning no_update")
            return no_update, False, None, None

        try:
            logger.info("Processing LP problem...")
            # Clean objective function string
            clean_objective = re.sub(
                r"^(max(imize)?|min(imize)?)\s*Z\s*=\s*", "", objective, flags=re.IGNORECASE
            ).strip()

            # Reconstruct the objective with the correct prefix
            full_objective = f"{objective_type.capitalize()} Z = {clean_objective}"
            
            # Select solver based on user choice
            is_maximize = objective_type == "maximize"
            logger.info(f"Using {solver_type.upper()} solver (maximize={is_maximize})")
            
            if solver_type == "highs":
                solver = HiGHSSolver()
                solution = solver.solve(clean_objective, constraints, is_maximize)
            else:
                solver = PuLPSolver()
                solution = solver.solve(clean_objective, constraints, is_maximize)
            
            logger.debug(f"Solver returned: success={solution.get('success')}")

            if solution["success"]:
                logger.info("✅ Problem solved successfully")
                logger.debug(f"Optimal value: {solution['objective_value']}")
                
                # Convert numpy types to Python native types for JSON serialization
                import numpy as np
                
                def convert_to_native(obj):
                    """Convert numpy types to native Python types"""
                    if isinstance(obj, dict):
                        return {k: convert_to_native(v) for k, v in obj.items()}
                    elif isinstance(obj, (list, tuple)):
                        return [convert_to_native(item) for item in obj]
                    elif isinstance(obj, (np.integer, np.floating)):
                        return float(obj)
                    elif isinstance(obj, np.ndarray):
                        return obj.tolist()
                    else:
                        return obj
                
                # Prepare solution data for the store (excluding non-serializable objects)
                solution_data = {
                    "success": True,
                    "variables": convert_to_native(solution["variables"]),
                    "objective_value": float(solution["objective_value"]) if hasattr(solution["objective_value"], 'item') else solution["objective_value"],
                    "status": solution["status"],
                    "solution": convert_to_native(solution["variables"]),  # For compatibility
                    "optimal_value": float(solution["objective_value"]) if hasattr(solution["objective_value"], 'item') else solution["objective_value"],  # For compatibility
                    # Don't store the problem object as it's not JSON serializable
                }

                logger.info("Returning successful solution to UI")
                # Store complete solution data including all needed fields
                solution_data["solver_log"] = solution["log"]
                return (
                    solution_data,
                    False,
                    None,
                    None,
                )
            else:
                logger.warning(f"Solver failed: {solution.get('error')}")
                # Store error information in solution data
                error_data = {
                    "success": False,
                    "error": solution["error"],
                    "solver_log": solution.get("log", "")
                }
                return (
                    error_data,
                    False,
                    solution.get("objective_error"),
                    solution.get("constraint_error"),
                )
        except Exception as e:
            logger.error(f"Exception in solve_problem: {e}", exc_info=True)
            error_data = {
                "success": False,
                "error": f"An unexpected error occurred: {e}"
            }
            return (
                error_data,
                False,
                "Check format",
                "Check format",
            )

    # Callback 2: Update results display
    callback_count += 1
    LPLogger.log_callback_registration(
        logger,
        "update_results",
        inputs=["solution-store.data"],
        outputs=["results-container.children"]
    )
    @callback(Output("results-container", "children"), Input("solution-store", "data"))
    def update_results(solution_data):
        """Update results display based on solution data"""
        logger.debug(f"update_results callback triggered with data: {solution_data is not None}")
        
        if not solution_data:
            return no_update
            
        if solution_data.get("success") == False:
            # Display error alert
            return dmc.Alert(
                solution_data.get("error", "Unknown error"),
                title="Solver Error",
                color="red",
                withCloseButton=True
            )
        
        # Display successful solution
        return create_solution_display(solution_data)

    # Callback 3: Update plot
    callback_count += 1
    LPLogger.log_callback_registration(
        logger,
        "update_plot",
        inputs=["solution-store.data"],
        outputs=["feasible-region-plot.figure"]
    )
    @callback(Output("feasible-region-plot", "figure"), Input("solution-store", "data"))
    def update_plot(solution_data):
        """Update visualization based on solution data"""
        logger.debug(f"update_plot callback triggered with data: {solution_data is not None}")
        if not solution_data or solution_data.get("success") == False:
            return LPPlotter._create_empty_plot(
                "Solve a problem to see the visualization"
            )

        # Check if we can visualize (2 variables or less)
        if solution_data.get("variables") and len(solution_data.get("variables", {})) <= 2:
            # For now, just create a simple plot since we can't store the problem object
            import plotly.graph_objects as go
            fig = go.Figure()
            
            # Add the optimal point
            var_names = list(solution_data["variables"].keys())
            if len(var_names) == 2:
                x_val = solution_data["variables"][var_names[0]]
                y_val = solution_data["variables"][var_names[1]]
                
                fig.add_trace(go.Scatter(
                    x=[x_val],
                    y=[y_val],
                    mode='markers',
                    marker=dict(size=12, color='red'),
                    name=f'Optimal Solution ({x_val:.2f}, {y_val:.2f})'
                ))
                
                fig.update_layout(
                    title=f"Optimal Solution: {solution_data['objective_value']:.2f}",
                    xaxis_title=var_names[0],
                    yaxis_title=var_names[1],
                    showlegend=True,
                    height=400
                )
            
            return fig
        else:
            # Create an empty figure for problems with more than 2 variables
            import plotly.graph_objects as go
            fig = go.Figure()
            fig.add_annotation(
                text="Visualization is only available for problems with 2 variables",
                xref="paper", yref="paper",
                x=0.5, y=0.5, showarrow=False,
                font=dict(size=14)
            )
            fig.update_layout(
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                height=400
            )
            return fig

    # Callback 4: Update solver log
    callback_count += 1
    LPLogger.log_callback_registration(
        logger,
        "update_solver_log",
        inputs=["solution-store.data"],
        outputs=["solver-log-content.children"]
    )
    @callback(Output("solver-log-content", "children"), Input("solution-store", "data"))
    def update_solver_log(solution_data):
        """Update solver log display"""
        logger.debug(f"update_solver_log callback triggered with data: {solution_data is not None}")
        if not solution_data:
            return "No solver output yet"

        return solution_data.get("solver_log", "No solver log available")

    # AI-related callbacks
    # Callback 5: Load example problem
    callback_count += 1
    LPLogger.log_callback_registration(
        logger,
        "load_example_problem",
        inputs=["example-problem-select.value"],
        outputs=["nl-problem-input.value"]
    )
    @callback(
        Output("nl-problem-input", "value"), Input("example-problem-select", "value")
    )
    def load_example_problem(example_key):
        """Load example problem description"""
        logger.debug(f"load_example_problem triggered with key: {example_key}")
        if example_key and example_key in EXAMPLE_PROBLEMS_LIBRARY:
            logger.info(f"Loading example problem: {example_key}")
            return EXAMPLE_PROBLEMS_LIBRARY[example_key]["description"]
        return no_update

    # Callback 6: AI formulation
    callback_count += 1
    LPLogger.log_callback_registration(
        logger,
        "formulate_with_ai",
        inputs=["formulate-button.n_clicks"],
        outputs=[
            "formulation-results.children",
            "ai-formulation-store.data",
            "formulate-button.loading"
        ],
        states=["nl-problem-input.value"]
    )
    @callback(
        [
            Output("formulation-results", "children"),
            Output("ai-formulation-store", "data"),
            Output("formulate-button", "loading"),
        ],
        Input("formulate-button", "n_clicks"),
        State("nl-problem-input", "value"),
        prevent_initial_call=True,
    )
    def formulate_with_ai(n_clicks, problem_description):
        """Handle AI formulation button click"""
        logger.info(f"🤖 formulate_with_ai triggered (n_clicks={n_clicks})")
        if not n_clicks or not problem_description:
            logger.debug("Missing inputs for AI formulation")
            return [], None, False

        try:
            logger.info("Starting AI formulation process")
            # Check if API credentials are available
            if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
                error_alert = dmc.Alert(
                    "Please set GEMINI_API_KEY or GOOGLE_API_KEY environment variable to use AI features",
                    title="Configuration Error",
                    color="red",
                )
                return [error_alert], None, False

            # Initialize formulator
            logger.debug("Initializing LPFormulator")
            formulator = LPFormulator()

            # Get formulation
            logger.info("Calling AI formulator...")
            result = formulator.formulate_problem(problem_description)
            logger.debug(f"Formulation result: success={result.get('success')}")

            if result.get("success"):
                # Create results display
                results_display = create_formulation_results(result)
                return results_display, result, False
            else:
                # Show error
                error_alert = dmc.Alert(
                    result.get("error", "Unknown error occurred"),
                    title="Formulation Error",
                    color="red",
                )
                return [error_alert], None, False

        except Exception as e:
            logger.error(f"Exception in formulate_with_ai: {e}", exc_info=True)
            error_alert = dmc.Alert(
                f"Error: {str(e)}",
                title="Unexpected Error",
                color="red",
            )
            return [error_alert], None, False

    # Callback 7: Copy to manual input
    callback_count += 1
    LPLogger.log_callback_registration(
        logger,
        "copy_to_manual_input",
        inputs=["copy-to-manual-button.n_clicks"],
        outputs=[
            "objective-input.value",
            "constraints-input.value",
            "input-mode-tabs.value"
        ],
        states=["ai-formulation-store.data"]
    )
    @callback(
        [
            Output("objective-input", "value", allow_duplicate=True),
            Output("constraints-input", "value"),
            Output("input-mode-tabs", "value"),
        ],
        Input("copy-to-manual-button", "n_clicks"),
        State("ai-formulation-store", "data"),
        prevent_initial_call=True,
    )
    def copy_to_manual_input(n_clicks, formulation_data):
        """Copy AI formulation to manual input fields"""
        logger.info(f"copy_to_manual_input triggered (n_clicks={n_clicks})")
        if not n_clicks or not formulation_data:
            logger.debug("No data to copy")
            return no_update, no_update, no_update

        if formulation_data.get("success"):
            objective = formulation_data.get("objective", "")
            constraints = formulation_data.get("constraints", "")
            logger.info("Copying AI formulation to manual input fields")
            logger.debug(f"Objective: {objective}")
            logger.debug(f"Constraints: {constraints}")

            # Switch to manual tab and populate fields
            return objective, constraints, "manual"

        logger.warning("Formulation data not successful")
        return no_update, no_update, no_update
    
    logger.info(f"✅ Total callbacks registered: {callback_count + 1}")
