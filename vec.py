"""
Show an animation of cross products.

usage: python3.8 vec.py

One plot shows the vectors rotating about the origin and displays their cross product.
Adjacent to that, a plot displays the cross product as a function of
theta (absolute value of each vectors' angles above/below the X-axis).

Each of the vectors' magnitudes remain constant and the only transformation is rotation.
"""
import math
from typing import Any, Callable, List, Optional, Tuple, TypedDict

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
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
from matplotlib.ticker import FuncFormatter, MultipleLocator

# TODO
# Add bound checking for GCD
# Refactor out x_1, x_... calculation to function
# Fix formatting for newlines in docstrings
# Extract formatting class to its own file?
# Command line args for vectors' magnitudes?
# Make graph sizing generated?
# Move main() initialization to init_anim()

MAG_1 = 4
MAG_2 = 3


class LineDict(TypedDict):
    """Dictionary with attributes about a plotted line."""

    line: Line2D
    x_data: List[float]
    y_data: List[float]


class MultiplePi:
    r"""
    Handle formatting of numbers as multiples of pi.

    Attributes
    ----------
    denominator : int
        The denominator of the multiples desired.

    base : float, optional
        Number to find multiples of, by default math.pi

    symbol : str, optional
        Symbol to place in string of multiple, by default r"\pi

    """

    def __init__(self, denominator: int, base: float = math.pi,
                 symbol: str = r"\pi"):
        """Initialize self."""
        self.denominator = denominator
        self.base = base
        self.symbol = symbol

    def locator(self) -> MultipleLocator:
        """Return the locator with ticks at multiples of base via denominator.

        Returns
        -------
        MultipleLocator
            The object used to space the ticks
        """
        return MultipleLocator(self.base / self.denominator)

    def formatter(self) -> FuncFormatter:
        """Return the formatter for multiple ticks.

        Returns
        -------
        FuncFormatter
            Used to insert the symbol into the multiples
        """
        return FuncFormatter(self._make_formatter())

    def _make_formatter(self) -> Callable[[float, Any], str]:
        """Return the function used by the FuncFormatter instance.

        Returns
        -------
        Callable[[float, Any], str]
            Accpes a value and a position parameter and transforms them
        """
        def _fmt(theta, _) -> str:
            """Transform the passed value into the proper representation of the multiple.

            Parameters
            ----------
            theta : float
                The angle in radians to be transformed
            _ : int
                Index of the tick on the axis

            Returns
            -------
            str
                The final label to be shown on the axis
            """
            denom = self.denominator
            # Find raw numerator by finding how many (denom)s are in (theta)
            # eg. How many pi/4 are in 1.5pi? (6)
            numer = np.int(np.rint(denom * theta / self.base))

            # Simplify the raw (numer) to lowest eg. 6/4 to 3/2
            com = self._gcd(numer, denom)

            # Simplify by dividing raw (numer) and (denom) by GCD
            (numer, denom) = (int(numer / com), int(denom / com))

            # If an integer of base
            if denom == 1:
                if numer == 0:
                    return r"$0$"

                # When numer simplifies to be +/- 1
                if numer in (-1, 1):
                    return r"${0}{1}$".format(
                        "-" if numer == -1 else "", self.symbol)

                # Just (multiple) * (base)
                return r"${0}{1}$".format(numer, self.symbol)

            # between inetegers of base
            # When numer simplifies to be +/- 1
            if numer in (-1, 1):
                return r"$\frac{{{0}{2}}}{{{1}}}$".format(
                    "-" if numer == -1 else "", denom, self.symbol)

            # Simplified ((numer) * (base))/(denom)
            return r"$\frac{{{0}{2}}}{{{1}}}$".format(
                numer, denom, self.symbol)

        return _fmt

    @staticmethod
    def _gcd(int_1: float, int_2: float) -> float:
        """Return the Greatest Common Divisor of int_1 and int_2.

        AKA, greatest common factor or greatest common measure.

        Parameters
        ----------
        int_1 : float
            First integer
        int_2 : float
            Second integer

        Returns
        -------
        float
            The largest positive integer that divides each of the integers
        """
        while int_2:
            int_1, int_2 = int_2, int_1 % int_2
        return int_1


def setup_plt() -> None:
    """Adjust properties to be rendered on the plot."""
    mpl.rcParams["font.family"] = "Poppins"
    plt.style.use("ggplot")


def format_plt() -> None:
    """Adjust properties of the rendered plot."""
    plt.tight_layout()


def format_plt_1(plt_1: Axes) -> None:
    """Format the vector plot after it has been rendered.

    Parameters
    ----------
    plt_1 : Axes
        The Axes object describing the subplot
    """
    v_patch = Patch(color="r", label=r"$\vec{v}$")
    w_patch = Patch(color="g", label=r"$\vec{w}$")

    plt_1.legend(handles=[v_patch, w_patch])

    x_axis: XAxis = plt_1.get_xaxis()
    y_axis: YAxis = plt_1.get_yaxis()

    y_min_loc: MultipleLocator = MultipleLocator(1)
    y_axis.set_minor_locator(y_min_loc)

    x_min_loc: MultipleLocator = MultipleLocator(1)
    x_axis.set_minor_locator(x_min_loc)

    plt_1.grid(axis="both", which="major", lw=1.5)
    plt_1.grid(axis="both", which="minor", lw=0.5)

    plt_1.set(xlabel="$X$", ylabel="$Y$", title="Vectors plotted on grid")

    plt_1.set_ylim([-5, 5])
    plt_1.set_xlim([-5, 5])


def format_plt_2(plt_2: Axes) -> None:
    """Format the cross product plot after it has been rendered.

    Parameters
    ----------
    plt_2 : Axes
        The Axes object describing the subplot
    """
    x_axis: XAxis = plt_2.get_xaxis()
    plt_2.set(
        xlabel=r"$\theta$ (radians)",
        ylabel="Cross Product",
        title="Cross Product Theta Relationship")

    pi_formatter: MultiplePi = MultiplePi(4)

    x_axis.set_major_locator(pi_formatter.locator())
    x_axis.set_major_formatter(pi_formatter.formatter())

    x_min_loc: MultipleLocator = MultipleLocator(math.pi / 12)
    x_axis.set_minor_locator(x_min_loc)

    plt_2.set_ylim([-17, 17])
    plt_2.set_xlim([- math.pi / 8, math.pi + (math.pi / 8)])


def plot_quiver(axes: Axes) -> Tuple[Quiver, Text]:
    """Plot the vector arrows on the plot.

    Parameters
    ----------
    axes : Axes
        The object describing the subplot

    Returns
    -------
    Tuple[Quiver, Text]
        The quiver objects as well as the cross product text
    """
    x_1, y_1 = (MAG_1 *
                math.cos(0), MAG_1 *
                math.sin(0))
    x_2, y_2 = (MAG_2 *
                math.cos(0), MAG_2 *
                math.sin(0))

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

    info: Text = axes.text(-4, 4, f"Cross Product: 0")

    return (arrows, info)


def plot_cross_prod_line(plt_2: Axes) -> Line2D:
    """Plot the cross product value as a function of theta.

    Parameters
    ----------
    plt_2 : Axes
        The Axes object describing the graph

    Returns
    -------
    Line2D
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
    arrows : Quiver
        The vector arrows
    info : Text
        The text stating the cross product
    line : Line2D
        Line plotting cross product

    Returns
    -------
    Callable
        The function called by FuncAnimation
    """
    return lambda: [arrows, info, line]


def update_plt_1(arrows: Quiver,
                 info: Text, theta: float) -> float:
    """Update the vector plot with new angles and re-calculate cross product.

    Parameters
    ----------
    arrows : Quiver
        The vector arrows
    info : Text
        The text stating the cross product
    theta : float
        The angle above and below the x-axis for each vector

    Returns
    -------
    float
        The cross product at this angle
    """
    x_1, y_1 = (MAG_1 *
                math.cos(theta), MAG_1 *
                math.sin(theta))
    x_2, y_2 = (MAG_2 *
                math.cos(-theta), MAG_2 *
                math.sin(-theta))

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
    line_dict : LineDict
        Has the line object and associated x and y data
    theta : float
        The angle above and below the x-axis for each vector
    cross_prod : float
        The calculated cross product

    Returns
    -------
    Line2D
        The actual line object
    """
    line_dict["x_data"].append(theta)
    line_dict["y_data"].append(cross_prod)

    line_dict["line"].set_data(line_dict["x_data"], line_dict["y_data"])

    return line_dict["line"]


def animate(theta: float, arrows: Quiver, info: Text,
            line_dict: LineDict) -> List[Artist]:
    """Update all plots with new data.

    Parameters
    ----------
    theta : float
        The angle above and below the x-axis for each vector
    arrows : Quiver
        The vector arrows
    info : Text
        The text stating the cross product
    line_dict : LineDict
        Has the line object and associated x and y data

    Returns
    -------
    List[Artist]
        The updated artists
    """
    cross_prod = update_plt_1(arrows, info, theta)

    update_plt_2(line_dict, theta, cross_prod)

    return [arrows, info, line_dict["line"]]


def main() -> None:
    """Run all executable code."""
    setup_plt()

    fig: Figure = plt.figure(figsize=(9, 4.5), dpi=140)
    plt_1: Axes = fig.add_subplot(121)
    plt_2: Axes = fig.add_subplot(122)

    format_plt_1(plt_1)
    format_plt_2(plt_2)

    (arrows, info) = plot_quiver(plt_1)
    line = plot_cross_prod_line(plt_2)

    # Include line_dict and info under plt_x in future
    # plt_dict = {"plt_1": plt_1, "plt_2": plt_2}

    line_dict: LineDict = {"line": line, "x_data": [], "y_data": []}

    format_plt()

    anim = FuncAnimation(  # pylint: disable=unused-variable
        fig,
        animate,
        init_func=init_anim_factory(arrows, info, line),
        fargs=(arrows, info, line_dict),
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
