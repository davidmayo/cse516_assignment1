import math
import sys
from typing import Iterable, List, Tuple, Union

try:
    import matplotlib.pyplot as plt
    _matplotlib_available = True
except ImportError:
    _matplotlib_available = False


def throughput(n: int, p: float) -> float:
    """Calculate the total throughput of an ALOHA network with `n` stations,
    each of which have a `p` probability of transmitting a frame during the
    frame transmission time"""
    try:
        return n * p * (1.0 - p) ** (2 * (n - 1))
    except ZeroDivisionError:
        return float("nan")

# This is basically a clone of numpy.linspace, but I don't want a dependence on
# numpy
def linspace(
    low: float,
    high: float,
    count: int
) -> List[float]:
    step_size = (high - low) / (count - 1)
    return [
        low + t * step_size
        for t
        in range(count)
    ]

def throughput_vectorized(
    n: int,
    xs: Iterable[float]
) -> List[Tuple[float, float]]:
    """Vectorized version of `throughput()`"""
    return [
        (x, throughput(p=x, n=n))
        for x
        in xs
    ]

def find_max(points: List[Tuple[float, float]]) -> Tuple[float, float]:
    """Get the (x, y) point with the largest 'y' value."""
    return sorted([
        point
        for point
        in points
        if not math.isnan(point[1])
    ], key=lambda tup: tup[1])[-1]

# [0.000, 1.000] in steps of 0.0001
xs = linspace(0.0, 1.0, count=10001)

# Specific points the assignment asks for
specific_xs = [
    0.01,
    0.05,
    0.10,
    0.15,
    0.20,
    0.25,
    0.30,
    0.35,
    0.40,
    0.45,
    0.50,
    0.55,
    0.60,
    0.65,
    0.70,
    0.75,
]

def split(
    points: List[Tuple[float, float]]
) -> Tuple[List[float], List[float]]:
    """Split a list of point tuples `[(x, y)]` into a tuple of lists of Xs
    and Ys `([xs], [ys])` (This is needed for matplotlib plotting)"""
    xs = [
        x
        for x,y
        in points
    ]
    ys = [
        y
        for x,y
        in points
    ]
    return (xs, ys)

# Create list of matplotlib Axes, if possible
if _matplotlib_available:
    fig, axes = plt.subplots(
        3,
        2,
        constrained_layout=True
    )
    fig.suptitle(
        f"ALOHA network throughputs",
        weight="bold",
    )
    fig.set_size_inches(7.5, 10.5)
    fig.set_dpi(300)
    print(axes)
    ax1: plt.Axes = axes[0][0]
    ax2: plt.Axes = axes[0][1]
    ax3: plt.Axes = axes[1][0]
    ax4: plt.Axes = axes[1][1]
    ax5: plt.Axes = axes[2][0]
    ax6: plt.Axes = axes[2][1]
    ax6.remove()
else:
    ax1 = None
    ax2 = None
    ax3 = None
    ax4 = None
    ax5 = None
axes = [ax1, ax2, ax3, ax4, ax5]

def analyze_n(n: int, ax: Union[plt.Axes, None] = None) -> None:
    """Do analysis of ALOHA network of size `n`, plotting to Axes `ax`, if
    possible."""
    print()
    print(f"----- Analyzing network of size {n} -----")
    points = throughput_vectorized(n=n, xs=xs)
    specific_points = throughput_vectorized(n=n, xs=specific_xs)
    max_p, max_throughput = find_max(points)
    max_p_specific, max_throughput_specific = find_max(specific_points)
    print(f"Max throughput is p={max_p:.4f}, throughput={max_throughput:.4f}")
    print(
        f"Max throughput (of given p values to analyze) is f"
        + "p={max_p_specific:.4f}, throughput={max_throughput_specific:.4f}"
    )
    pass

    if ax:
        ax: plt.Axes

        # Plot the line and the specific points asked for
        ax.plot(*split(points), color="blue")
        ax.scatter(*split(specific_points), color="blue")

        # Plot the max point, and horizontal/vertical lines to it.
        ax.scatter(
            max_p,
            max_throughput,
            color="red",
            label=f"Maximum:\np={max_p:.4f}\nS={max_throughput:.4f}"
        )
        ax.vlines(max_p, 0, max_throughput, color="red")
        ax.hlines(max_throughput, 0, max_p, color="red")
        ax.set_title(f"Network size {n=}")
        ax.set_xbound(0, 1)
        ax.set_xlabel(f"p = P(station has frame)")
        ax.set_ybound(0, 1)
        ax.set_ylabel(f"S = Network throughput")
        ax.legend()
        # plt()
        pass

for index, n in enumerate(range(1, 5+1)):
    analyze_n(n=n, ax=axes[index])

if _matplotlib_available:
    plt.savefig(f"plots.png", bbox_inches="tight")
    # plt.show()
else:
    print(f"ERROR! matplotlib not available. Plots will not be displayed.")
    print(f"matplotlib can be installed with:")
    print()
    print(f"{sys.executable} -m pip install matplotlib")
    print()
    print(f"Program will exit.")
