"""Results panel component for displaying LP solutions"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_results_panel():
    """Create the results display panel"""
    return dmc.Paper(
        shadow="sm",
        p="md",
        radius="md",
        children=[
            dmc.Title("Solution", order=3, mb="md"),
            dmc.Container(id="results-container", p=0),
        ],
    )


def create_solution_display(solution_data):
    """Create the solution display based on solver results"""
    if not solution_data:
        return dmc.Text("Click 'Solve Problem' to see results", c="dimmed")

    if "error" in solution_data:
        return dmc.Alert(
            title="Error",
            color="red",
            children=solution_data["error"],
            icon=DashIconify(icon="tabler:alert-circle"),
        )

    status = solution_data.get("status", "unknown")

    if status != "optimal":
        status_messages = {
            "infeasible": "The problem is infeasible - no solution exists that satisfies all constraints.",
            "unbounded": "The problem is unbounded - the objective can be improved infinitely.",
            "not_solved": "The problem could not be solved.",
            "undefined": "The problem status is undefined.",
        }
        return dmc.Alert(
            title=f"Status: {status.replace('_', ' ').title()}",
            color="yellow",
            children=status_messages.get(status, "Unknown status"),
            icon=DashIconify(icon="tabler:info-circle"),
        )

    # Display optimal solution
    solution = solution_data["solution"]
    optimal_value = solution_data["optimal_value"]

    # Create solution table
    table_data = [
        {"variable": var, "value": f"{value:.4f}"} for var, value in solution.items()
    ]

    return dmc.Stack(
        [
            dmc.Alert(
                title="Optimal Solution Found!",
                color="green",
                icon=DashIconify(icon="tabler:check"),
                children=f"Optimal objective value: {optimal_value:.4f}",
            ),
            dmc.Title("Variable Values", order=4),
            dmc.Table(
                striped=True,
                highlightOnHover=True,
                withTableBorder=True,
                withColumnBorders=True,
                data={
                    "head": ["Variable", "Value"],
                    "body": [[row["variable"], row["value"]] for row in table_data],
                },
            ),
        ]
    )
