"""Visualization panel component for LP problems"""

import dash_mantine_components as dmc
from dash import dcc


def create_visualization_panel():
    """Create the graphical solution panel"""
    return dmc.Paper(
        shadow="sm",
        p="md",
        radius="md",
        children=[
            dmc.Title("Graphical Solution", order=3, mb="md"),
            dcc.Graph(
                id="feasible-region-plot",
                config={
                    "displayModeBar": True,
                    "toImageButtonOptions": {
                        "format": "svg",
                        "filename": "lp_solution",
                    },
                },
            ),
        ],
    )
