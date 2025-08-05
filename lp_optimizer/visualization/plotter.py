"""Visualization utilities for LP problems"""

import numpy as np
import plotly.graph_objects as go
from typing import Dict

from ..config import (
    PLOT_RESOLUTION,
    DEFAULT_MAX_BOUND,
    OPTIMAL_POINT_COLOR,
    OPTIMAL_POINT_SIZE,
)


class LPPlotter:
    """Create visualizations for linear programming problems"""

    @staticmethod
    def create_feasible_region_plot(result: Dict) -> go.Figure:
        """
        Create visualization for 2-variable LP problems

        Args:
            result: Solution dictionary from solver

        Returns:
            Plotly figure object
        """
        if "error" in result or result.get("status") != "optimal":
            return LPPlotter._create_empty_plot("No optimal solution to visualize")

        variables = result["variables"]
        if len(variables) != 2:
            return LPPlotter._create_empty_plot(
                f"Visualization only available for 2-variable problems (found {len(variables)} variables)"
            )

        fig = go.Figure()

        # Get variable names
        x_var, y_var = variables[0], variables[1]

        # Determine plot bounds
        x_max = (
            max(DEFAULT_MAX_BOUND, result["solution"][x_var] * 1.5)
            if result["solution"][x_var] > 0
            else DEFAULT_MAX_BOUND
        )
        y_max = (
            max(DEFAULT_MAX_BOUND, result["solution"][y_var] * 1.5)
            if result["solution"][y_var] > 0
            else DEFAULT_MAX_BOUND
        )

        x_range = np.linspace(0, x_max, PLOT_RESOLUTION)

        # Plot constraints
        LPPlotter._add_constraints(fig, result, x_var, y_var, x_range, y_max)

        # Add axes
        fig.add_hline(y=0, line_color="black", line_width=2)
        fig.add_vline(x=0, line_color="black", line_width=2)

        # Add optimal point
        LPPlotter._add_optimal_point(fig, result, x_var, y_var)

        # Add objective function direction
        LPPlotter._add_objective_direction(fig, result, x_var, y_var)

        # Update layout
        fig.update_layout(
            title="Feasible Region and Optimal Solution",
            xaxis_title=x_var,
            yaxis_title=y_var,
            xaxis=dict(range=[-0.5, x_max]),
            yaxis=dict(range=[-0.5, y_max]),
            showlegend=True,
            hovermode="closest",
        )

        return fig

    @staticmethod
    def _create_empty_plot(message: str) -> go.Figure:
        """Create empty plot with message"""
        return go.Figure().add_annotation(
            text=message,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )

    @staticmethod
    def _add_constraints(fig, result, x_var, y_var, x_range, y_max):
        """Add constraint lines and feasible regions to the plot"""
        for i, (coeffs, op, rhs) in enumerate(result["constraints"]):
            a = coeffs[x_var]
            b = coeffs[y_var]

            if b != 0:
                # y = (rhs - a*x) / b
                y_line = (rhs - a * x_range) / b

                # Determine feasible side
                if op == "<=":
                    y_fill = np.minimum(y_line, y_max)
                    fillcolor = (
                        f"rgba({50 + i * 30}, {100 + i * 20}, {200 - i * 30}, 0.1)"
                    )
                elif op == ">=":
                    y_fill = np.maximum(y_line, 0)
                    fillcolor = (
                        f"rgba({200 - i * 30}, {100 + i * 20}, {50 + i * 30}, 0.1)"
                    )
                else:  # equality
                    y_fill = y_line
                    fillcolor = f"rgba(150, 150, 150, 0.1)"

                # Add constraint line
                fig.add_trace(
                    go.Scatter(
                        x=x_range,
                        y=y_line,
                        mode="lines",
                        name=f"Constraint {i + 1}",
                        line=dict(width=2),
                    )
                )

                # Add shaded feasible region
                if op != "=":
                    fig.add_trace(
                        go.Scatter(
                            x=np.concatenate([x_range, x_range[::-1]]),
                            y=np.concatenate(
                                [
                                    y_fill,
                                    np.full_like(x_range, 0 if op == "<=" else y_max),
                                ]
                            ),
                            fill="toself",
                            fillcolor=fillcolor,
                            line=dict(width=0),
                            showlegend=False,
                            hoverinfo="skip",
                        )
                    )
            elif a != 0:
                # Vertical line constraint: x = rhs/a
                x_line = rhs / a
                fig.add_vline(
                    x=x_line, line_dash="dash", annotation_text=f"x = {x_line:.2f}"
                )

    @staticmethod
    def _add_optimal_point(fig, result, x_var, y_var):
        """Add the optimal solution point to the plot"""
        fig.add_trace(
            go.Scatter(
                x=[result["solution"][x_var]],
                y=[result["solution"][y_var]],
                mode="markers+text",
                name="Optimal Solution",
                marker=dict(
                    size=OPTIMAL_POINT_SIZE, color=OPTIMAL_POINT_COLOR, symbol="star"
                ),
                text=[
                    f"({result['solution'][x_var]:.2f}, {result['solution'][y_var]:.2f})"
                ],
                textposition="top right",
            )
        )

    @staticmethod
    def _add_objective_direction(fig, result, x_var, y_var):
        """Add arrow showing objective function gradient direction"""
        obj_a = result["objective_coeffs"][x_var]
        obj_b = result["objective_coeffs"][y_var]

        # Normalize gradient
        grad_norm = np.sqrt(obj_a**2 + obj_b**2)
        if grad_norm > 0:
            grad_x = obj_a / grad_norm * 3
            grad_y = obj_b / grad_norm * 3

            # Add gradient arrow
            fig.add_annotation(
                x=result["solution"][x_var] + grad_x,
                y=result["solution"][y_var] + grad_y,
                ax=result["solution"][x_var],
                ay=result["solution"][y_var],
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                showarrow=True,
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=2,
                arrowcolor="darkblue",
                text="Objective Direction"
                if result["is_maximize"]
                else "Negative Obj. Direction",
            )
