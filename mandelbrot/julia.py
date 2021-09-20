import numpy as np
import cv2
from numba import jit
from tqdm import tqdm
import time
import multiprocessing
import random
from mpmath import mp

# アスペクト比
# aspect_ratio = 9 / 16
aspect_ratio = 3 / 4
# aspect_ratio = 2 / 3


@jit
def julia(a, b, center, length, resolution, max_itr):
    center = (center[0], -center[1])
    h1 = center[0] - length
    h2 = center[0] + length
    v1 = center[1] - length * aspect_ratio
    v2 = center[1] + length * aspect_ratio

    re_list = np.linspace(h1, h2, resolution)
    im_list = np.linspace(v1, v2, int(resolution * aspect_ratio))

    z = np.empty(shape=(len(im_list), len(re_list)), dtype=np.uint8)

    for i, re in enumerate(re_list):
        for j, im in enumerate(im_list):
            itr = 0
            z0 = complex(re, im)
            c = complex(a, b)
            while np.abs(z0) < np.inf and itr < max_itr:
                z0 = z0 ** 2 + c
                itr += 1

            if itr == max_itr:
                z[j][i] = 0
            else:
                z[j][i] = itr
    z = np.flipud(z)
    return z, a, b


def wrapper_julia(args):
    return julia(*args)


def make_sample_image():
    center = (-0.5, 0.0)
    length = 2.0
    # resolution = 2736
    resolution = 1200
    max_itr = 255
    a = -0.3
    b = -0.63

    z = julia(a, b, center, length, resolution, max_itr)

    colormap_table = [
        ['COLORMAP_AUTUMN', cv2.COLORMAP_AUTUMN],
        ['COLORMAP_BONE', cv2.COLORMAP_BONE],
        ['COLORMAP_JET', cv2.COLORMAP_JET],
        ['COLORMAP_WINTER', cv2.COLORMAP_WINTER],
        ['COLORMAP_RAINBOW', cv2.COLORMAP_RAINBOW],
        ['COLORMAP_OCEAN', cv2.COLORMAP_OCEAN],
        ['COLORMAP_SUMMER', cv2.COLORMAP_SUMMER],
        ['COLORMAP_SPRING', cv2.COLORMAP_SPRING],
        ['COLORMAP_COOL', cv2.COLORMAP_COOL],
        ['COLORMAP_HSV', cv2.COLORMAP_HSV],
        ['COLORMAP_PINK', cv2.COLORMAP_PINK],
        ['COLORMAP_HOT', cv2.COLORMAP_HOT],
        ['COLORMAP_PARULA', cv2.COLORMAP_PARULA],
        ['COLORMAP_MAGMA', cv2.COLORMAP_MAGMA],
        ['COLORMAP_INFERNO', cv2.COLORMAP_INFERNO],
        ['COLORMAP_PLASMA', cv2.COLORMAP_PLASMA],
        ['COLORMAP_VIRIDIS', cv2.COLORMAP_VIRIDIS],
        ['COLORMAP_CIVIDIS', cv2.COLORMAP_CIVIDIS],
        ['COLORMAP_TWILIGHT', cv2.COLORMAP_TWILIGHT],
        ['COLORMAP_TWILIGHT_SHIFTED', cv2.COLORMAP_TWILIGHT_SHIFTED],
        ['COLORMAP_TURBO', cv2.COLORMAP_TURBO],
        ['COLORMAP_DEEPGREEN', cv2.COLORMAP_DEEPGREEN]
    ]

    for colormap in colormap_table:
        a = cv2.applyColorMap(z, colormap[1])
        cv2.imwrite('Colormap/' + colormap[0] + '.png', a)


def closeup_julia():
    # center = (-0.749205, 0.1)
    # length_range = (2.0, 10E-9)
    center = (-0.20415, 0.65252)
    length_range = (2.0, 10E-15)
    resolution = 1280
    max_itr = 1000
    a = -0.3
    b = -0.63

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter('julia.mp4', fourcc, 24.0, (resolution, int(resolution*aspect_ratio)))

    windows = []
    size = length_range[0]
    while size > length_range[1]:
        windows.append(size)
        size *= 0.98

    """
    # シングルver
    progress_bar = tqdm(total=len(windows))
    for w in windows:
        z = mandelbrot(center, w, resolution, max_itr)
        a = cv2.applyColorMap(z, cv2.COLORMAP_PINK)
        video.write(a)
        progress_bar.update(1)
    """

    # マルチプロセスver
    pool = multiprocessing.Pool(4)

    args = []
    for w in windows:
        args.append([a, b, center, w, resolution, max_itr])

    results = []
    with tqdm(total=len(args)) as t:
        for result in pool.imap(wrapper_julia, args):
            results.append(result)
            t.update(1)

    for r in results:
        a = cv2.applyColorMap(r, cv2.COLORMAP_PINK)
        video.write(a)

    video.release()


def move_constant_julia():
    center = (0.0, 0.0)
    length = 2.0
    resolution = 1280
    max_itr = 1000
    constant = [[random.random()/2, random.random()/2],
                [random.random()/2, random.random()/2]]

    movie_time = 10.0  # sec
    fps = 24.0
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter('julia.mp4', fourcc, fps, (resolution, int(resolution*aspect_ratio)))

    a_list = np.linspace(constant[0][0], constant[1][0], int(movie_time * fps))
    b_list = np.linspace(constant[0][1], constant[1][1], int(movie_time * fps))

    pool = multiprocessing.Pool(4)

    args = []
    for a, b in zip(a_list, b_list):
        args.append([a, b, center, length, resolution, max_itr])

    results = []
    with tqdm(total=len(args)) as t:
        for result in pool.imap(wrapper_julia, args):
            results.append(result)
            t.update(1)

    for r in results:
        a = cv2.applyColorMap(r[0], cv2.COLORMAP_PINK)
        cv2.putText(a, 'a= {:+.15f}'.format(r[1]), (0, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        cv2.putText(a, 'b= {:+.15f}'.format(r[2]), (0, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)
        video.write(a)

    video.release()


def calc_julia():
    t0 = time.time()
    # center = (-0.749570065531204200000000001,
    #           0.100515451623784500000000001)
    center = (0.0, 0.0)
    length = 2.0
    # resolution = 2736
    # resolution = 3840
    resolution = 1280
    max_itr = 1000
    a = -0.3
    b = -0.63

    z = julia(a, b, center, length, resolution, max_itr)
    a = cv2.applyColorMap(z, cv2.COLORMAP_PINK)

    print('time:', time.time() - t0)

    cv2.imwrite('julia.png', a)
    cv2.imshow('plot', a)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # make_sample_image()
    # calc_julia()
    # closeup_julia()
    move_constant_julia()
