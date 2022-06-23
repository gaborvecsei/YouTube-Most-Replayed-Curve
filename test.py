import argparse

import matplotlib.pyplot as plt

import get_curve


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="URL of the Youtube video")
    parser.add_argument("--wait-time",
                        "-t",
                        required=False,
                        type=int,
                        default=20,
                        help="How much seconds to wait for the curve element to load")
    parser.add_argument("--chromedriver-path",
                        required=False,
                        default="chromedriver",
                        help="Path to the chromedriver executeable")
    return parser.parse_args()


def show_the_curve(url: str, wait_time: int, chromedriver_path: str = "chromedriver") -> None:
    most_replayed_retriever = get_curve.MostReplayedCurve(chromedriver_path)
    curve = most_replayed_retriever.get_curve(url, wait_time)
    most_replayed_retriever.close()

    x = curve[:, 0]
    y = curve[:, 1]

    plt.figure(figsize=(20, 4))
    plt.title(f"We have {len(x)} points for {url}")
    plt.scatter(x, y, c="r", alpha=0.5)
    plt.plot(x, y)
    plt.show()


if __name__ == "__main__":
    args = get_args()
    show_the_curve(url=args.url, wait_time=args.wait_time, chromedriver_path=args.chromedriver_path)
