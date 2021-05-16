import os
import cv2
import mandelbrot


def make_sample_image():
    center = complex(-0.7, 0.0)
    length = 4.0
    resolution = (960, 1280)
    max_itr = 255

    z = mandelbrot.mandelbrot(center, length, resolution, max_itr)

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

    if not os.path.isdir('colormap'):
        os.mkdir('colormap')

    for colormap in colormap_table:
        a = cv2.applyColorMap(z, colormap[1])
        cv2.imwrite('colormap/' + colormap[0] + '.png', a)


if __name__ == '__main__':
    make_sample_image()