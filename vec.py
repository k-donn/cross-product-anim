import math
from typing import Callable, List, TypedDict, Optional, Tuple
from matplotlib.artist import Artist

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.axis import XAxis, YAxis
from matplotlib.backends.backend_qt5 import FigureManagerQT
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.quiver import Quiver
from matplotlib.text import Text
from matplotlib.ticker import FuncFormatter, MultipleLocator

# TODO
# Add latex to cross-prod x-axis
# Make graph sizing generated?

MAG_1 = 4
MAG_2 = 3


class LineDict(TypedDict):
    line: Line2D
    x_data: List[float]
    y_data: List[float]


def format_pi(denominator):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    def _fmt(theta, _):
        den = denominator
        num = np.int(np.rint(den * theta / np.pi))
        com = gcd(num, den)
        num, den = (int(num / com), int(den / com))
        if den == 1:
            if num == 0:
                return 0

            if num == 1:
                return "\u03C0"

            if num == -1:
                return "-\u03C0"

            return f"{num}\u03C0"
        else:
            if num == 1:
                return f"\u03C0/{den}"

            if num == -1:
                return f"-\u03C0/{den}"

            return f"{num}\u03C0/{den}"

    return _fmt


def setup_plt():
    plt.style.use("ggplot")


def format_plt():
    plt.tight_layout()


def format_plt_1(plt_1: Axes):
    x_axis: XAxis = plt_1.get_xaxis()
    y_axis: YAxis = plt_1.get_yaxis()

    y_min_loc: MultipleLocator = MultipleLocator(1)
    y_axis.set_minor_locator(y_min_loc)

    x_min_loc: MultipleLocator = MultipleLocator(1)
    x_axis.set_minor_locator(x_min_loc)

    plt_1.grid(axis="both", which="major", lw=1.5)
    plt_1.grid(axis="both", which="minor", lw=0.5)

    plt_1.set(xlabel="X", ylabel="Y", title="Vectors plotted on grid")

    plt_1.set_ylim([-5, 5])
    plt_1.set_xlim([-5, 5])


def format_plt_2(plt_2: Axes):
    x_axis: XAxis = plt_2.get_xaxis()
    plt_2.set(
        xlabel=r"Theta (radians)",
        ylabel="Cross Product",
        title="Cross Product Theta Relationship")

    x_maj_loc: MultipleLocator = MultipleLocator(math.pi / 4)
    x_axis.set_major_locator(x_maj_loc)

    x_min_loc: MultipleLocator = MultipleLocator(math.pi / 12)
    x_axis.set_minor_locator(x_min_loc)

    x_formatter: FuncFormatter = FuncFormatter(format_pi(4))
    x_axis.set_major_formatter(x_formatter)

    plt_2.set_ylim([-17, 17])
    plt_2.set_xlim([-math.pi / 8, math.pi + (math.pi / 8)])


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

    info: Text = axes.text(0, 4, f"Cross Product: 0")

    return (arrows, info)


def plot_cross_prod_line(axes: Axes) -> Line2D:
    line: Line2D = plt.plot([], [], "-", lw=2, color="b")[0]

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
