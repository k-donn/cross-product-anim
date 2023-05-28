"""
Show an animation of vector cross products.

usage: python3.8 vec.py [-h] mag1 mag2

One plot shows the vectors rotating about the origin and displays their cross product.
Adjacent to that, a plot displays the cross product as a function of
theta (absolute value of each vectors' angles above/below the X-axis).

Each of the vectors' magnitudes remain constant and the only transformation is rotation.

positional arguments:
  mag1        Magnitude of vector 1
  mag2        Magnitude of vector 2

optional arguments:
  -h, --help  show this help message and exit

"""
from argparse import ArgumentParser
import math
from typing import Any, Callable, List, Optional, Tuple, TypedDict

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplot_fmt_pi.ticker import MultiplePi
from matplotlib.animation import FuncAnimation
from matplotlib.artist import Artist
from matplotlib.axes import Axes
from matplotlib.axis import XAxis, YAxis
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
from matplotlib.quiver import Quiver
from matplotlib.text import Text
from matplotlib.ticker import MultipleLocator

# TODO
# Command line args for vectors' magnitudes?
# Make graph sizing generated?
# Move main() initialization to init_anim()


# The components of a vector
Vector = Tuple[float, float]
# Two vectors together
VectorPair = Tuple[Vector, Vector]


class LineDict(TypedDict):
    """Dictionary with attributes about a plotted line."""

    line: Line2D
    x_data: List[float]
    y_data: List[float]


def calc_vector_comps(theta_1: float, theta_2: float,
                      mag1: float, mag2: float) -> VectorPair:
    """Calculate the components of two vectors with constant magnitude.

    Parameters
    ----------
    theta_1 : `float`
        The first angle
    theta_2 : `float`
        The second angle

    Returns
    -------
    `VectorPair`
        The components of the vectors
    """
    x_1, y_1 = (mag1 *
                math.cos(theta_1), mag1 *
                math.sin(theta_1))
    x_2, y_2 = (mag2 *
                math.cos(theta_2), mag2 *
                math.sin(theta_2))

    return ((x_1, y_1), (x_2, y_2))


def setup_plt() -> None:
    """Adjust properties to be rendered on the plot."""
    mpl.rcParams["font.family"] = "Poppins"
    plt.style.use("ggplot")


def format_plt() -> None:
    """Adjust properties of the rendered plot."""
    plt.tight_layout()


def format_plt_1(plt_1: Axes, mag1: float, mag2: float) -> None:
    """Format the vector plot after it has been rendered.

    Parameters
    ----------
    plt_1 : `Axes`
        The Axes object describing the subplot
    """
    v_patch = Patch(color="r", label=r"$\vec{v}$")
    w_patch = Patch(color="g", label=r"$\vec{w}$")

    plt_1.legend(handles=[v_patch, w_patch])

    x_axis: XAxis = plt_1.get_xaxis()
    y_axis: YAxis = plt_1.get_yaxis()

    # y_min_loc: MultipleLocator = MultipleLocator(1)
    # y_axis.set_minor_locator(y_min_loc)

    # x_min_loc: MultipleLocator = MultipleLocator(1)
    # x_axis.set_minor_locator(x_min_loc)

    plt_1.grid(axis="both", which="major", lw=1.5)
    plt_1.grid(axis="both", which="minor", lw=0.5)

    plt_1.set(xlabel="$X$", ylabel="$Y$", title="Vectors plotted on grid")

    plt_1.set_xlim([-max(mag1, mag2) - 1, max(mag1, mag2) + 1])
    plt_1.set_ylim([-max(mag1, mag2) - 1, max(mag1, mag2) + 1])


def format_plt_2(plt_2: Axes, mag1: float, mag2: float) -> None:
    """Format the cross product plot after it has been rendered.

    Parameters
    ----------
    plt_2 : `Axes`
        The Axes object describing the subplot
    """
    x_axis: XAxis = plt_2.get_xaxis()
    plt_2.set(
        xlabel=r"$\theta$ (radians)",
        ylabel="Cross Product",
        title="Cross Product Theta Relationship")

    maj_manager = MultiplePi(denominator=4)
    min_manager = MultiplePi(denominator=12)

    x_axis.set_major_locator(maj_manager.locator())
    x_axis.set_major_formatter(maj_manager.formatter())

    x_axis.set_minor_locator(min_manager.locator())

    ((x_1, y_1), (x_2, y_2)) = calc_vector_comps(
        math.pi / 4, -math.pi / 4, mag1, mag2)
    vecs: np.ndarray = np.array([[x_1, y_1], [x_2, y_2]])

    # gets maximum cross product to know hot to set axes
    bound = abs(np.cross(*vecs))
    bound = bound + bound / 10
    plt_2.set_ylim([-bound, bound])
    plt_2.set_xlim([- math.pi / 8, math.pi + (math.pi / 8)])


def plot_quiver(axes: Axes, mag1: float, mag2: float) -> Tuple[Quiver, Text]:
    """Plot the vector arrows on the plot.

    Parameters
    ----------
    axes : `Axes`
        The object describing the subplot

    Returns
    -------
    `Tuple[Quiver, Text]`
        The quiver objects as well as the cross product text
    """
    ((x_1, y_1), (x_2, y_2)) = calc_vector_comps(0, 0, mag1, mag2)

    vecs: np.ndarray = np.array([[0, 0, x_1, y_1], [0, 0, x_2, y_2]])
    x_origins, y_origins, x_comps, y_comps = zip(*vecs)

    arrows: Quiver = axes.quiver(
        x_origins,
        y_origins,
        x_comps,
        y_comps,
        angles='xy',
        scale_units='xy',
        scale=1,
        color=("r", "g"))

    info: Text = axes.text(0.1, 0.9, f"Cross Product: 0", transform=axes.transAxes)

    return (arrows, info)


def plot_cross_prod_line(plt_2: Axes) -> Line2D:
    """Plot the cross product value as a function of theta.

    Parameters
    ----------
    plt_2 : `Axes`
        The Axes object describing the graph

    Returns
    -------
    `Line2D`
        The object describing the plotted line
    """
    artists: List[Any] = plt_2.plot(
        [],
        [],
        lw=2,
        color="#0055ffff",
        label="cross v. theta")

    line: Line2D = artists[0]

    return line


def init_anim_factory(arrows: Quiver, info: Text,
                      line: Line2D) -> Callable[..., List[Artist]]:
    """Return a function that has all of the initially plotted artists on the subplots.

    The blitting algorithm needs these artists for its optimizations.
    This function could probably contain what is currently in main().

    Parameters
    ----------
    arrows : `Quiver`
        The vector arrows

    info : `Text`
        The text stating the cross product

    line : `Line2D`
        Line plotting cross product

    Returns
    -------
    `Callable[..., List[Artist]]`
        The function called by FuncAnimation
    """
    return lambda: [arrows, info, line]


def update_plt_1(arrows: Quiver,
                 info: Text, theta: float, mag1: float, mag2: float) -> float:
    """Update the vector plot with new angles and re-calculate cross product.

    Parameters
    ----------
    arrows : `Quiver`
        The vector arrows

    info : `Text`
        The text stating the cross product

    theta : `float`
        The angle above and below the x-axis for each vector

    Returns
    -------
    `float`
        The cross product at this angle
    """
    ((x_1, y_1), (x_2, y_2)) = calc_vector_comps(theta, -theta, mag1, mag2)
    vecs: np.ndarray = np.array([[x_1, y_1], [x_2, y_2]])
    x_comps, y_comps = zip(*vecs)

    cross_prod = np.cross(*vecs)

    info.set_text(f"Cross product: {cross_prod:>6.2f}")

    arrows.set_UVC(x_comps, y_comps)

    return cross_prod


def update_plt_2(line_dict: LineDict, theta: float,
                 cross_prod: float) -> Line2D:
    """Update the line plotting cross product as a function of theta.

    Parameters
    ----------
    line_dict : `LineDict`
        Has the line object and associated x and y data

    theta : `float`
        The angle above and below the x-axis for each vector

    cross_prod : `float`
        The calculated cross product

    Returns
    -------
    `Line2D`
        The actual line object
    """
    line_dict["x_data"].append(theta)
    line_dict["y_data"].append(cross_prod)

    line_dict["line"].set_data(line_dict["x_data"], line_dict["y_data"])

    return line_dict["line"]


def animate(theta: float, arrows: Quiver, info: Text,
            line_dict: LineDict, mag1: float, mag2: float) -> List[Artist]:
    """Update all plots with new data.

    Parameters
    ----------
    theta : `float`
        The angle above and below the x-axis for each vector

    arrows : `Quiver`
        The vector arrows

    info : `Text`
        The text stating the cross product

    line_dict : `LineDict`
        Has the line object and associated x and y data

    Returns
    -------
    `List[Artist]`
        The updated artists
    """
    cross_prod = update_plt_1(arrows, info, theta, mag1, mag2)

    update_plt_2(line_dict, theta, cross_prod)

    return [arrows, info, line_dict["line"]]


def main() -> None:
    """Run all executable code."""
    parser = ArgumentParser(
        prog="python3.8 vec.py",
        description="Show an animation of vector cross products.",
    )
    parser.add_argument("mag1", type=float, help="Magnitude of vector 1")
    parser.add_argument("mag2", type=float, help="Magnitude of vector 2")

    args = parser.parse_args()

    setup_plt()

    fig: Figure = plt.figure(figsize=(9, 4.5), dpi=140)
    plt_1: Axes = fig.add_subplot(121)
    plt_2: Axes = fig.add_subplot(122)

    format_plt_1(plt_1, args.mag1, args.mag2)
    format_plt_2(plt_2, args.mag1, args.mag2)

    (arrows, info) = plot_quiver(plt_1, args.mag1, args.mag2)
    line = plot_cross_prod_line(plt_2)

    # Include line_dict and info under plt_x in future
    # plt_dict = {"plt_1": plt_1, "plt_2": plt_2}

    line_dict: LineDict = {"line": line, "x_data": [], "y_data": []}

    format_plt()

    anim = FuncAnimation(  # pylint: disable=unused-variable
        fig,
        animate,
        init_func=init_anim_factory(arrows, info, line),
        fargs=(arrows, info, line_dict, args.mag1, args.mag2),
        frames=np.linspace(0, math.pi, 128),
        interval=1000 / 30,
        repeat=False)

    fig_manager: Optional[FigureManagerQT] = plt.get_current_fig_manager()
    if fig_manager is not None:
        fig_manager.set_window_title("Cross Product Animation")

    plt.draw()
    plt.show()


if __name__ == "__main__":
    main()
