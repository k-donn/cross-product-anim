import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.text import Text
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.quiver import Quiver

# TODO
# Add graph of cross-product
# Fix fargs dummy issue

MAG_1 = 4
MAG_2 = 4


def format_plt():
    plt.style.use("ggplot")


def main():
    thetas = {}
    thetas["theta_1"] = 0
    thetas["theta_2"] = 0

    x_1, y_1 = (MAG_1 *
                math.cos(thetas["theta_1"]), MAG_1 *
                math.sin(thetas["theta_1"]))
    x_2, y_2 = (MAG_2 *
                math.cos(thetas["theta_2"]), MAG_2 *
                math.sin(thetas["theta_2"]))

    # Remeber, U is all of the x-components not the first vector. V for Y
    vecs: np.ndarray = np.array([[0, 0, x_1, y_1], [0, 0, x_2, y_2]])
    X, Y, U, V = zip(*vecs)

    format_plt()

    fig: Figure = plt.figure()
    ax: Axes = fig.add_subplot(111)

    arrows: Quiver = ax.quiver(
        X,
        Y,
        U,
        V,
        angles='xy',
        scale_units='xy',
        scale=1,
        color=("r", "b"))

    info: Text = ax.text(1.9, 3, f"Cross Product: 0")

    anim = FuncAnimation(
        fig,
        animate,
        frames=np.linspace(0, math.pi, 128),
        interval=1000 / 30,
        blit=False,
        repeat=False,
        fargs=(arrows, ax, info))

    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])

    # plt.draw()
    plt.show()


def animate(theta: float, arrows: Quiver, ax: Axes, info: Text):

    x_1, y_1 = (MAG_1 *
                math.cos(theta), MAG_1 *
                math.sin(theta))
    x_2, y_2 = (MAG_2 *
                math.cos(-theta), MAG_2 *
                math.sin(-theta))

    vecs: np.ndarray = np.array([[x_1, y_1], [x_2, y_2]])
    U, V = zip(*vecs)

    cross_prod = np.cross(*vecs)

    info.set_text(f"Cross product: {cross_prod:>6.2f}")

    arrows.set_UVC(U, V)


if __name__ == "__main__":
    main()
