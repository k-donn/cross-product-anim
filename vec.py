import math

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.axes import Axes
from matplotlib.figure import Figure
from matplotlib.quiver import Quiver

# TODO
# Add graph of cross-product

MAG_1 = 4
MAG_2 = 4
DELTA = math.pi / 64


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

    soa: np.ndarray = np.array([[0, 0, x_1, y_1], [0, 0, x_2, y_2]])
    X, Y, U, V = zip(*soa)

    fig: Figure = plt.figure()
    ax: Axes = fig.add_subplot(111)

    arrows: Quiver = ax.quiver(
        X,
        Y,
        U,
        V,
        angles='xy',
        scale_units='xy',
        scale=1)

    anim = FuncAnimation(
        fig,
        animate,
        frames=64,
        interval=1000/30,
        blit=False,
        repeat=False,
        fargs=(
            arrows,
            thetas))

    ax.set_xlim([-5, 5])
    ax.set_ylim([-5, 5])

    # plt.draw()
    plt.show()


def init_anim_factory(arrows):
    def init_anim():
        return arrows
    return init_anim


def animate(frame, arrows: Quiver, thetas):
    print(f"{frame=}")

    x_1, y_1 = (MAG_1 *
                math.cos(thetas["theta_1"]), MAG_1 *
                math.sin(thetas["theta_1"]))
    x_2, y_2 = (MAG_2 *
                math.cos(thetas["theta_2"]), MAG_2 *
                math.sin(thetas["theta_2"]))

    soa: np.ndarray = np.array([[0, 0, x_1, y_1], [0, 0, x_2, y_2]])
    X, Y, U, V = zip(*soa)

    arrows.set_UVC(U, V)

    thetas["theta_1"] += DELTA
    thetas["theta_2"] -= DELTA



if __name__ == "__main__":
    main()
