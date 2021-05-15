import cv2
import numpy as np
from sympy import sieve


def ulam_spiral(start_num, end_num, prime_color=(0, 0, 0), back_color=(255, 255, 255)):

    # 始点を(0, 0)として、座標のリストを作成する
    pos = [(0, 0)]
    # 螺旋は右に1、上に1、左に2、下に2、右に3、上に3、左に4、下に4…と進む
    count = 1
    while len(pos) < (end_num - start_num):
        for c in range(count):
            pos.append((pos[-1][0] + 1, pos[-1][1]))  # 右に進む
        for c in range(count):
            pos.append((pos[-1][0], pos[-1][1] - 1))  # 上に進む
        for c in range(count+1):
            pos.append((pos[-1][0] - 1, pos[-1][1]))  # 左に進む
        for c in range(count+1):
            pos.append((pos[-1][0], pos[-1][1] + 1))  # 下に進む
        count += 2
    pos = pos[:end_num - start_num]  # 不要な末尾を削除

    # 最小座標を取得し、左上が(0, 0)となるよう補正
    min_x = min([p[0] for p in pos])
    min_y = min([p[1] for p in pos])
    pos = [(p[0]-min_x, p[1]-min_y) for p in pos]

    # 背景画像を作成
    max_x = max([p[0] for p in pos])
    max_y = max([p[1] for p in pos])
    img = np.zeros((max_y+1, max_x+1, 3), np.uint8)
    img[:] = back_color

    # 開始番号から順番に素数判定、素数の場合はposの座標に従い色を変更
    for n, p in zip(range(start_num, end_num), range(len(pos))):
        if n in sieve:
            img[pos[p][1], pos[p][0]] = prime_color

    # 画像出力
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    cv2.imwrite('ulam_spiral' + str(start_num) + '-' + str(end_num) + '.png', img)


def main():
    start_num = 1
    end_num = 50000
    prime_color = (6, 49, 87)
    back_color = (226, 54, 57)
    # ulam_spiral(start_num, end_num)
    ulam_spiral(start_num, end_num, prime_color, back_color)


if __name__ == '__main__':
    main()
