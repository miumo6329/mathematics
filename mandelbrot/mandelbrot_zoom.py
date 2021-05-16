import cv2
from tqdm import tqdm
import multiprocessing
import mandelbrot


def wrapper_mandelbrot(args):
    return mandelbrot.mandelbrot(*args)


def mandelbrot_zoom():
    # 10E-15あたりが解像度の限界?
    center = complex(-0.20415, 0.65252)
    width_range = (2.0, 10E-9)  # 描画範囲の横幅
    resolution = (960, 1280)  # 出力画像の解像度
    max_itr = 1000

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter('mandelbrot.mp4', fourcc, 24.0, (resolution[1], resolution[0]))

    widths = []
    width = width_range[0]
    while width > width_range[1]:
        widths.append(width)
        width *= 0.98

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
    for w in widths:
        args.append([center, w, resolution, max_itr])

    results = []
    with tqdm(total=len(args)) as t:
        for result in pool.imap(wrapper_mandelbrot, args):
            results.append(result)
            t.update(1)

    for r in results:
        a = cv2.applyColorMap(r, cv2.COLORMAP_PINK)
        video.write(a)

    video.release()


if __name__ == '__main__':
    mandelbrot_zoom()
