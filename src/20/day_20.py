from aocd.models import Puzzle
from itertools import product

import numpy as np
import matplotlib.pyplot as plt


def part_a(enh_alg: str, image: np.ndarray):
    image = enhance(enh_alg, image, steps=2)
    # truncate irrelevant border
    image = image[1:-1, 1:-1]
    plt.imshow(image)
    # plt.savefig('part_a.png')
    plt.show()
    return np.count_nonzero(image)


def part_b(enh_alg: str, image: np.ndarray):
    image = enhance(enh_alg, image, steps=50)
    # truncate irrelevant border
    image = image[1:-1, 1:-1]
    plt.imshow(image)
    # plt.savefig('part_b.png')
    plt.show()
    return np.count_nonzero(image)


def enhance(enh_alg: str, image: np.ndarray, steps: int):
    def enhance_pixel(row_: int, col_: int):
        enh_idx = ''.join(image[row_ - 1, col_ - 1:col_ + 2].astype(str)) + \
                  ''.join(image[row_, col_ - 1:col_ + 2].astype(str)) + \
                  ''.join(image[row_ + 1, col_ - 1:col_ + 2].astype(str))
        enh_idx = int(enh_idx, 2)
        return enh_alg[enh_idx] == '#'

    for step in range(steps):
        # transform and expand relevant "infinite" space around image as it flips every iteration
        if step % 2 == 0:
            image = np.pad(image[1:-1, 1:-1], 2, mode='constant', constant_values=0)
        else:
            image = np.pad(image[1:-1, 1:-1], 2, mode='constant', constant_values=1)

        # enhance the image
        enhanced = np.zeros_like(image)
        for row, col in product(range(1, image.shape[0] - 1), range(1, image.shape[1] - 1)):
            enhanced[row, col] = enhance_pixel(row, col)
        image = enhanced

    return image


def load(data: str):
    enh_alg, image = data.split('\n\n')
    image = [list(row) for row in image.split('\n')]
    image = (np.array(image) == '#').astype(np.byte)
    image = np.pad(image, 1, mode='constant')
    return enh_alg, image


puzzle = Puzzle(year=2021, day=20)
ans_a = part_a(*load(puzzle.input_data))
print(ans_a)
# puzzle.answer_a = ans_a  # 5483

ans_b = part_b(*load(puzzle.input_data))
print(ans_b)
# puzzle.answer_b = ans_b  # 18732
