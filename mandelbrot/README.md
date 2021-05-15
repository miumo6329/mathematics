# はじめに
散々いろいろな方が記事にしているので、何番煎じか分かりませんがマンデルブロ集合の画像、拡大動画を作ってみました。

マンデルブロ集合が描くオシャレな幾何学模様をデスクトップにしたり、[こんな感じのyoutube動画](https://www.youtube.com/watch?v=pCpLWbHVNhk)を作ってみたりしたい、というのがモチベーションです。

# マンデルブロ集合とは


# 実装① 画像生成

```Python
import time
import cv2
import numpy as np
from numba import jit


@jit
def mandelbrot(center, width, resolution, max_itr):
    re_diff = width / 2
    im_diff = (width / 2) * (resolution[0] / resolution[1])
resolution[1])

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
    width = 4.0  # 描画範囲の横幅
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


```
# 実装② 動画生成
実装①に以下の関数を追加し、mp4動画を作成しました。

# まとめ

# 参考ページ
- <https://watlab-blog.com/2020/05/23/mandelbrot-set/>
- <https://qiita.com/namahoge/items/c390e79693605234212b>
- <http://www.math.titech.ac.jp/~kawahira/courses/mandel.pdf>
