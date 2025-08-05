"""Solver log panel component"""

import dash_mantine_components as dmc
from dash_iconify import DashIconify


def create_solver_log_panel():
    """Create the solver log accordion panel"""
    return dmc.Accordion(
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
                                )
                            ],
                        )
                    ),
                ],
            )
        ]
    )
