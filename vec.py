import math
from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.axis import XAxis, YAxis
from matplotlib.figure import Figure
from matplotlib.quiver import Quiver
from matplotlib.text import Text
from matplotlib.ticker import MultipleLocator

# TODO
# Add graph of cross-product as a function of theta
# Make graph sizing generated?

MAG_1 = 4
MAG_2 = 3


def format_plt():
    plt.style.use("ggplot")


def format_plt_1(plt_1: Axes):
    x_axis: XAxis = plt_1.get_xaxis()
    y_axis: YAxis = plt_1.get_yaxis()

    y_min_loc: MultipleLocator = MultipleLocator(1)
    y_axis.set_minor_locator(y_min_loc)

    x_min_loc: MultipleLocator = MultipleLocator(1)
    x_axis.set_minor_locator(x_min_loc)

    plt_1.grid(axis="y", which="major", lw=1.5)
    plt_1.grid(axis="y", which="minor", lw=0.5)

    plt_1.grid(axis="x", which="major", lw=1.5)
    plt_1.grid(axis="x", which="minor", lw=0.5)

    plt_1.set_xlabel("X")
    plt_1.set_ylabel("Y")

    plt_1.set_ylim([-5, 5])
    plt_1.set_xlim([-5, 5])

    plt_1.set_title("Vectors plotted on grid.")


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
        color=("r", "b"))

    info: Text = axes.text(1.9, 3, f"Cross Product: 0")

    return (arrows, info)


def main():

    format_plt()

    fig: Figure = plt.figure()
    plt_1: Axes = fig.add_subplot(111)

    format_plt_1(plt_1)

    (arrows, info) = plot_quiver(plt_1)

    anim = FuncAnimation(
        fig,
        animate,
        frames=np.linspace(0, math.pi, 128),
        interval=1000 / 30,
        blit=False,
        repeat=False,
        fargs=(arrows, plt_1, info))

    # plt.draw()
    plt.show()


def update_plt_1(plt_1: Axes, arrows: Quiver, info: Text, theta: float):
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


def animate(theta: float, arrows: Quiver, plt_1: Axes, info: Text):
    update_plt_1(plt_1, arrows, info, theta)


if __name__ == "__main__":
    main()
