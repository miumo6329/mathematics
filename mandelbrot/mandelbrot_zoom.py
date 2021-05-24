import cv2
from tqdm import tqdm
import multiprocessing
import mandelbrot


def wrapper_mandelbrot(args):
    return mandelbrot.mandelbrot(*args)


def mandelbrot_zoom():
    center = complex(-0.20415, 0.65252)
    width_range = (2.0, 10E-9)  # 描画範囲の横幅
    resolution = (960, 1280)  # 出力画像の解像度
    max_itr = 1000  # 最大イテレーション数

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter('mandelbrot.mp4', fourcc, 30.0, (resolution[1], resolution[0]))

    # 描画範囲の横幅を段階的に小さくして引数のlistを作成
    args = []
    width = width_range[0]
    while width > width_range[1]:
        args.append([center, width, resolution, max_itr])
        width *= 0.99

    # マルチプロセスで処理
    pool = multiprocessing.Pool(6)
    results = []
    with tqdm(total=len(args)) as t:
        for result in pool.imap(wrapper_mandelbrot, args):
            results.append(result)
            t.update(1)

    # 動画作成
    for r in results:
        a = cv2.applyColorMap(r, cv2.COLORMAP_PINK)
        video.write(a)
    video.release()


if __name__ == '__main__':
    mandelbrot_zoom()
