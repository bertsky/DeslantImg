import argparse
from time import perf_counter
from typing import List

import cv2
import matplotlib.pyplot as plt
from path import Path

from deslant import deslant


def get_img_files(data_dir: Path) -> List[Path]:
    """Returns all image files contained in a folder."""
    res = []
    for ext in ['*.png', '*.jpg', '*.bmp']:
        res += Path(data_dir).files(ext)
    return res


def parse_args():
    """Parses command line args."""
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=Path('../../data/'))
    parser.add_argument('--optim_algo', choices=['grid', 'powell'], default='grid')
    parser.add_argument('--lower_bound', type=float, default=-2)
    parser.add_argument('--upper_bound', type=float, default=2)
    parser.add_argument('--num_steps', type=float, default=20)
    parser.add_argument('--bg_color', type=int, default=255)

    return parser.parse_args()


def main():
    # parse command line args
    parsed = parse_args()

    # go through list of images
    for fn_img in get_img_files(parsed.data):
        print(f'Processing {fn_img}')
        img = cv2.imread(fn_img, cv2.IMREAD_GRAYSCALE)

        # process image
        t0 = perf_counter()
        res = deslant(img,
                      optim_algo=parsed.optim_algo,
                      lower_bound=parsed.lower_bound,
                      upper_bound=parsed.upper_bound,
                      num_steps=parsed.num_steps,
                      bg_color=parsed.bg_color)
        t1 = perf_counter()

        dt = t1 - t0
        print(f'Runtime {1000 * dt:.1f}ms')

        # show output
        plt.figure(f'Shear value: {res.shear_val:.3f}')

        # show scores for all grid points if optim_algo is 'grid'
        num_rows = 1
        if res.candidates is not None:
            num_rows = 2
            plt.subplot(num_rows, 1, 2)
            shear_vals = [c.shear_val for c in res.candidates]
            score_vals = [c.score for c in res.candidates]
            plt.stem(shear_vals, score_vals)
            plt.title('Score values')

        # show original image
        plt.subplot(num_rows, 2, 1)
        plt.imshow(img, cmap='gray', vmin=0, vmax=255)
        plt.title('Original')

        # and deslanted image
        plt.subplot(num_rows, 2, 2)
        plt.imshow(res.img, cmap='gray', vmin=0, vmax=255)
        plt.title('Deslanted')
        plt.show()


if __name__ == '__main__':
    main()
