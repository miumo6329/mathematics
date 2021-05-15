import os
import cv2
import numpy as np
from tqdm import tqdm


class Sandpile:
    def __init__(self, model):
        self.model = model
        self.state = np.zeros(model.shape, dtype=np.uint8)
        self.limit = 4  # 積み上げ可能な砂の上限値
        self.step = 1
        self.update_limit = 500000

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        resize = 1  # 動画サイズの倍率
        self.video_size = (int(self.model.shape[1]*resize), int(self.model.shape[0]*resize))
        self.video = cv2.VideoWriter('sandpile.mp4', fourcc, 30.0, self.video_size)

        self.export_counter = 1
        self.progress_bar = tqdm(total=self.update_limit)

    def update(self):
        # 状態を更新
        self.state += self.model
        self.step += 1
        self.progress_bar.update(1)
        # self.record()
        if self.judge_continue() is False:
            return False

        # 上限値を超えるマスがある場合、無くなるまで砂山を崩す
        while np.any(self.state >= self.limit) > 0:
            self.break_sand()
            # self.record()
            # if self.judge_continue() is False:
            #     return False

        return True

    def break_sand(self):
        # 上限値を超えるマスの座標を取得
        break_list = np.where(self.state >= self.limit)
        for i, j in zip(break_list[0], break_list[1]):
            self.state[i][j] -= self.limit
            if not i-1 < 0:
                self.state[i - 1][j] += 1
            if not i+1 >= self.state.shape[0]:
                self.state[i + 1][j] += 1
            if not j-1 < 0:
                self.state[i][j - 1] += 1
            if not j+1 >= self.state.shape[1]:
                self.state[i][j + 1] += 1

    def judge_continue(self):
        # self.step += 1
        # self.progress_bar.update(1)
        # ステップ上限値を超えたとき処理を終了
        if self.step > self.update_limit:
            return False
        # 全てのマスが上限値以上になったとき処理を終了
        if np.sum(self.state < self.limit) == 0:
            print('全てのマスが上限値を超えました。')
            return False
        return True

    def record(self):
        img = self.state * int(255/self.limit)
        img = cv2.applyColorMap(img, cv2.COLORMAP_CIVIDIS)
        img = cv2.resize(img, self.video_size, interpolation=cv2.INTER_AREA)
        self.video.write(img)

    def export_img(self, i):
        img = self.state * int(255/self.limit)
        img = cv2.applyColorMap(img, cv2.COLORMAP_CIVIDIS)
        img = cv2.resize(img, self.video_size, interpolation=cv2.INTER_AREA)
        cv2.imwrite('img/' + str(i) + '.png', img)

    def export_state(self):
        np.savetxt('state/' + str(self.export_counter) + '.csv', self.state, fmt="%.0f", delimiter=',')
        self.export_counter += 1

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        print('finish')


def main():
    # model = np.loadtxt('ulam_spiral.txt', delimiter=',', dtype=np.uint8)
    model = np.zeros((2000, 2000), dtype=np.uint8)
    # for i in range(model.shape[0]):
    #     model[i][0] = 1
    #     model[i][683] = 1
    #     model[i][684] = 1
    #     model[i][1367] = 1

    # model = np.zeros((90, 120), dtype=np.uint8)
    # for i in range(model.shape[0]):
    #     model[i][59] = 1
    #     model[i][60] = 1
    # for j in range(model.shape[1]):
    #     model[44][j] = 1
    #     model[45][j] = 1

    # model = np.zeros((91, 121), dtype=np.uint8)
    # # model[45][60] = 1
    # # model[44][60] = 1
    # # model[46][60] = 1
    # # model[45][59] = 1
    # # model[45][61] = 1
    # for i in range(model.shape[0]):
    #     # model[i][0] = 1
    #     model[i][479] = 1
    #     model[i][480] = 1
    #     # model[i][120] = 1
    # for j in range(model.shape[1]):
    #     # model[0][j] = 1
    #     model[269][j] = 1
    #     model[270][j] = 1
    #     # model[90][j] = 1

    model[1000][1000] = 4

    sandpile = Sandpile(model)

    if not os.path.isdir('img'):
        os.mkdir('img')
    if not os.path.isdir('state'):
        os.mkdir('state')

    i = 1
    n = 1
    while sandpile.update():
        # if i % 5 == 0:
        #     sandpile.export_state()
        if i % 50 == 0:
            sandpile.export_img(n)
            n += 1
        i += 1


if __name__ == '__main__':
    main()
