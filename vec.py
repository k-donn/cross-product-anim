import math
from typing import Callable, List, Optional, Tuple, TypedDict

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
# Types
# Docstrings
# Extract formatting thing to it's own file?
# Make graph sizing generated?

MAG_1 = 4
MAG_2 = 3


class LineDict(TypedDict):
    line: Line2D
    x_data: List[float]
    y_data: List[float]


def format_pi(denominator, base=math.pi, symbol=r"\pi"):
    def _gcd(int_1, int_2):
        while int_2:
            int_1, int_2 = int_2, int_1 % int_2
        return int_1

    def _fmt(theta, _):
        denom = denominator
        # Find raw numerator by finding how many (denom)s are in (theta)
        # eg. How many pi/4 are in 1.5pi? (6)
        numer = np.int(np.rint(denom * theta / base))

        # Simplify the raw (numer) to lowest eg. 6/4 to 3/2
        com = _gcd(numer, denom)

        # Simplify by dividing raw (numer) and (denom) by GCD
        (numer, denom) = (int(numer / com), int(denom / com))

        # If a multiple of base
        if denom == 1:
            if numer == 0:
                return r"$0$"

            if numer == 1:
                return r"${0}$".format(symbol)

            if numer == -1:
                return r"$-{0}$".format(symbol)

            # Just (multiple) * (base)
            return r"${0}{1}$".format(numer, symbol)
        # between multiples of base
        else:
            # Less than one-whole integer multiple
            if numer == 1:
                return r"$\frac{{{1}}}{{{0}}}$".format(denom, symbol)

            if numer == -1:
                return r"$\frac{{-{1}}}{{{0}}}$".format(denom, symbol)

            # Simplified ((numer)(base))/(denom)
            return r"$\frac{{{0}{2}}}{{{1}}}$".format(numer, denom, symbol)

    return _fmt


class Multiple(object):
    def __init__(self, denominator, base=math.pi, symbol=r"\pi"):
        self.denominator = denominator
        self.base = base
        self.symbol = symbol

    def locator(self):
        return MultipleLocator(self.base / self.denominator)

    def formatter(self):
        return FuncFormatter(
            format_pi(self.denominator, self.base, self.symbol))


def setup_plt():
    plt.style.use("ggplot")


def format_plt():
    plt.tight_layout()


def format_plt_1(plt_1: Axes):
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


def format_plt_2(plt_2: Axes):
    x_axis: XAxis = plt_2.get_xaxis()
    plt_2.set(
        xlabel=r"$\theta$ (radians)",
        ylabel="Cross Product",
        title="Cross Product Theta Relationship")

    pi_formatter: Multiple = Multiple(4)

    x_axis.set_major_locator(pi_formatter.locator())
    x_axis.set_major_formatter(pi_formatter.formatter())

    x_min_loc: MultipleLocator = MultipleLocator(math.pi / 12)
    x_axis.set_minor_locator(x_min_loc)

    plt_2.set_ylim([-17, 17])
    plt_2.set_xlim([- math.pi / 8, math.pi + (math.pi / 8)])


def plot_quiver(axes: Axes) -> Tuple[Quiver, Text]:
    x_1, y_1 = (MAG_1 *
                math.cos(0), MAG_1 *
                math.sin(0))
    x_2, y_2 = (MAG_2 *
                math.cos(0), MAG_2 *
                math.sin(0))

    # Remeber, U is all of the x-components not the first vector. V for Y
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


def plot_cross_prod_line(axes: Axes) -> Line2D:
    line: Line2D = plt.plot(
        [],
        [],
        lw=2,
        color="#0055ffff",
        label="cross v. theta")[0]

    return line


def main():

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

    anim = FuncAnimation(
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


def init_anim_factory(arrows: Quiver, info: Text, line: Line2D) -> Callable:
    def init_anim() -> List[Artist]:
        return [arrows, info, line]
    return init_anim


def update_plt_1(arrows: Quiver,
                 info: Text, theta: float) -> float:
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


def update_plt_2(line_dict: LineDict, theta, cross_prod):
    line_dict["x_data"].append(theta)
    line_dict["y_data"].append(cross_prod)

    line_dict["line"].set_data(line_dict["x_data"], line_dict["y_data"])

    return line_dict["line"]


def animate(theta: float, arrows: Quiver, info: Text, line_dict: LineDict):
    cross_prod = update_plt_1(arrows, info, theta)

    update_plt_2(line_dict, theta, cross_prod)

    return [arrows, info, line_dict["line"]]


if __name__ == "__main__":
    main()
