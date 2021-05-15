import time
import cv2
import numpy as np
from numba import jit


@jit
def mandelbrot(center, width, resolution, max_itr):
    re_diff = width / 2
    im_diff = (width / 2) * (resolution[0] / resolution[1])

    im_list = np.linspace(center.imag-im_diff, center.imag+im_diff, resolution[0])
    re_list = np.linspace(center.real-re_diff, center.real+re_diff, resolution[1])

    z = np.empty(shape=resolution, dtype=np.uint8)

    for i, im in enumerate(im_list):  # 垂直方向
        for j, re in enumerate(re_list):  # 水平方向
            zn = complex(0, 0)
            c = complex(re, im)
            value = 0
            for itr in range(max_itr):
                zn = zn ** 2 + c
                if np.abs(zn) > 2.0:
                    value = itr
                    break
            z[i][j] = value
    z = np.flipud(z)
    return z


def main():
    start_time = time.time()

    center = complex(-0.7, 0.0)  # 描画範囲の中心座標
    # center = complex(-0.7495700655312042, 0.1005154516237845)
    width = 4.0  # 描画範囲の横幅
    # width = 10e-13
    resolution = (960, 1280)  # 出力画像の解像度
    max_itr = 5000  # 最大イテレーション数

    z = mandelbrot(center, width, resolution, max_itr)
    img = cv2.applyColorMap(z, cv2.COLORMAP_PINK)

    print('time:', time.time() - start_time)

    cv2.imwrite('mandelbrot.png', img)
    cv2.imshow('mandelbrot', img)
    cv2.waitKey()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
