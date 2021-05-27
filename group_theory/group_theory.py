import math
import itertools
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def calc_group(base_group):
    group = base_group
    is_continue = True
    while is_continue and len(group) < 1000:
        is_continue = False
        for a, b in itertools.combinations_with_replacement(group, 2):
            c = np.dot(a, b)
            if True not in [np.allclose(c, g) for g in group]:
                group.append(c)
                is_continue = True
    return group


def reflect_group(group, vector):
    reflected = [np.dot(g, vector) for g in group]

    x = [r.flatten()[0] for r in reflected]
    y = [r.flatten()[1] for r in reflected]
    z = [r.flatten()[2] for r in reflected]

    fig = plt.figure()
    ax = Axes3D(fig)

    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")

    ax.plot(x, y, z, marker="o", linestyle='None')
    plt.show()


def main():
    # s0 = np.array([[math.sqrt(2), -1], [1, math.sqrt(2)]])
    # s1 = np.array([[math.sqrt(2), 1], [-1, math.sqrt(2)]])
    # s0 = np.array([[1, 0], [-1, 1]])
    # s1 = np.array([[1, -1], [0, 1]])

    s0 = np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]])
    s1 = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, -1]])
    base_group = [s0, s1]

    group = calc_group(base_group)
    print('位数：', len(group))

    # 列ベクトル作成
    vector = np.array([1, 1, 0])
    vector = np.reshape(vector, (-1, 1))

    # 射影プロット
    reflect_group(group, vector)


if __name__ == '__main__':
    main()

