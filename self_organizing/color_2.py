import numpy as np
import cv2
from tqdm import tqdm
from numba import jit

MAX_ROW = 100
MAX_COL = 100


def show_img(state):
    img = cv2.cvtColor(state, cv2.COLOR_BGR2RGB)
    cv2.imshow('img', cv2.resize(img, (400, 400), interpolation=cv2.INTER_AREA))
    cv2.waitKey()
    cv2.destroyAllWindows()


@jit
def attack(state):
    new_state = state.copy()
    for i, state_row in enumerate(state):
        for j, color in enumerate(state_row):
            new_r = state[i, (j-1) % MAX_COL][0]
            new_g = state[(i-1) % MAX_ROW, j][1]
            new_b = state[(i+1) % MAX_ROW, j][2]
            new_state[i][j] = [new_r, new_g, new_b]
            # diff_list = [[(i-1) % MAX_ROW, (j-1) % MAX_COL], [i, (j-1) % MAX_COL], [(i+1) % MAX_ROW, (j-1) % MAX_COL],
            #              [(i-1) % MAX_ROW, j], [(i+1) % MAX_ROW, j],
            #              [(i-1) % MAX_ROW, (j+1) % MAX_COL], [i, (j+1) % MAX_COL], [(i+1) % MAX_ROW, (j+1) % MAX_COL]]
            # for [diff_row, diff_col] in diff_list:
            #     for rgb in range(3):
            #         if int(color[rgb]) - int(new_state[diff_row][diff_col][(rgb+1) % 3]) > 20.0:
            #             new_state[diff_row][diff_col][rgb] = min(255, new_state[diff_row][diff_col][rgb] + 20)
            #             new_state[diff_row][diff_col][(rgb + 1) % 3] = max(0, new_state[diff_row][diff_col][(rgb + 1) % 3] - 20)
            # max_in_rgb = []
            # for rgb in range(3):
            #     value = max([state[d_row][d_col][rgb] for [d_row, d_col] in diff_list])
            #     max_in_rgb.append(value)
            # # print(max_in_rgb)
            # spread_color = max_in_rgb.index(max(max_in_rgb))
            #
            # if new_state[i][j][(spread_color + 1) % 3] - 10 > 0:
            #     color_1_diff = 10
            # else:
            #     color_1_diff = new_state[i][j][(spread_color+1) % 3]
            #
            # if new_state[i][j][(spread_color + 2) % 3] - 10 > 0:
            #     color_2_diff = 10
            # else:
            #     color_2_diff = new_state[i][j][(spread_color+2) % 3]
            #
            # new_state[i][j][spread_color] += (color_1_diff + color_2_diff)
            # new_state[i][j][(spread_color+1) % 3] -= color_1_diff
            # new_state[i][j][(spread_color+2) % 3] -= color_2_diff

    return new_state


def main():
    # state = np.zeros([MAX_ROW, MAX_COL, 3], dtype=np.uint8)
    state = np.random.randint(0, 255, [MAX_ROW, MAX_COL, 3], dtype=np.uint8)

    # RGBの合計値が255以下になるよう補正
    for i, state_row in enumerate(state):
        for j, color in enumerate(state_row):
            # print(color)
            state[i][j] = np.uint8((color / sum(color)) * 256)
            # print(color, sum(color))

    # state[10, 10] = [255, 0, 0]
    # state[70, 30] = [0, 255, 0]
    # state[40, 80] = [0, 0, 255]

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_size = (400, 400)
    video = cv2.VideoWriter('color_war_2.mp4', fourcc, 20.0, video_size)

    img = cv2.cvtColor(state, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, video_size, interpolation=cv2.INTER_AREA)
    video.write(img)

    steps = 500
    progress_bar = tqdm(total=steps)
    for i in range(steps):
        state = attack(state)
        img = cv2.cvtColor(state, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, video_size, interpolation=cv2.INTER_AREA)
        video.write(img)
        progress_bar.update(1)

    video.release()

    # img = cv2.cvtColor(state, cv2.COLOR_BGR2RGB)
    # cv2.imshow('img', cv2.resize(img, (100, 100), interpolation=cv2.INTER_AREA))
    # cv2.waitKey()
    # cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
