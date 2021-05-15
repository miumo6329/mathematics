import cv2
import numpy as np


class Sandpile:
    def __init__(self, model):
        self.model = model
        self.state = np.zeros(model.shape, dtype=np.uint8)
        self.limit = 4  # 積み上げ可能な砂の上限値
        self.step = 1
        self.step_limit = 20000

        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        resize = 3  # 動画サイズの倍率
        self.video_size = (int(self.model.shape[1]*resize), int(self.model.shape[0]*resize))
        self.video = cv2.VideoWriter('sandpile.mp4', fourcc, 30.0, self.video_size)

    def update(self):
        # 状態を更新
        self.state += self.model
        self.record()
        if self.judge_continue() is False:
            return False

        # 上限値を超えるマスがある場合、無くなるまで砂山を崩す
        while np.any(self.state >= self.limit) > 0:
            self.break_sand()
            self.record()
            if self.judge_continue() is False:
                return False

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
        self.step += 1
        # ステップ上限値を超えたとき処理を終了
        if self.step > self.step_limit:
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

    def __del__(self):
        self.video.release()
        cv2.destroyAllWindows()
        print('finish')


def main():
    # model = np.loadtxt('model.txt', delimiter=',', dtype=np.uint8)
    model = np.zeros((200, 200), dtype=np.uint8)
    model[100][100] = 1
    model[110][110] = 1
    model[90][110] = 1
    model[90][90] = 1
    model[110][90] = 1
    sandpile = Sandpile(model)

    while sandpile.update():
        pass


if __name__ == '__main__':
    main()
