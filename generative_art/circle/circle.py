import os
import cv2
import numpy as np
import math
import itertools
from tqdm import tqdm


def circle_in_circle(img, center, radius, color, circle_count, depth):
    if depth < 1:
        return
    else:
        depth -= 1

    for c in range(circle_count):
        next_radius = radius // 2
        x = int(center[0] + (next_radius * math.cos(c * math.radians(360 / circle_count))))
        y = int(center[1] + (next_radius * math.sin(c * math.radians(360 / circle_count))))
        cv2.circle(img, (x, y), radius=next_radius, color=color)
        circle_in_circle(img, (x, y), next_radius, color=color, circle_count=circle_count, depth=depth)


def main1():
    img = np.zeros((5000, 5000, 3), dtype=np.uint8)
    init_center = (2500, 2500)
    init_radius = 2400
    color = (255, 255, 255)
    # cv2.circle(img, init_center, radius=init_radius, color=color)
    circle_in_circle(img, init_center, init_radius, color=color, circle_count=18, depth=3)
    cv2.imwrite('circle.png', img)


def torus(img, center, inner_radius, outer_radius, circle_count, color):
    for_center = (outer_radius + inner_radius) // 2
    radius = (outer_radius - inner_radius) // 2

    for c in range(circle_count):
        x = int(center[0] + (for_center * math.cos(c * math.radians(360 / circle_count))))
        y = int(center[1] + (for_center * math.sin(c * math.radians(360 / circle_count))))
        cv2.circle(img, (x, y), radius=radius, color=color)


def main2():
    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    center = (500, 500)
    inner_radius = 200
    outer_radius = 400
    circle_count = 120
    color = (255, 255, 255)

    # torus(img, center, inner_radius, outer_radius, circle_count, color)
    # cv2.imwrite('torus.png', img)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video_size = (1000, 1000)
    video = cv2.VideoWriter('torus.mp4', fourcc, 20.0, video_size)
    for i in reversed(range(0, 350)):
        new_img = img.copy()
        torus(new_img, center, i, outer_radius, circle_count, color)
        video.write(new_img)
    video.release()


def wheels(img, center, radius, angular_velocities, color):
    img = img.copy()
    # fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 20
    # video_size = (1000, 1000)
    # video = cv2.VideoWriter('wheels.mp4', fourcc, fps, video_size)

    cv2.circle(img, center, radius=radius, color=color)
    now_rad = [-90 for r in angular_velocities]
    orbits = []
    for _ in range(150 * fps):
        frame = img.copy()
        next_center = center
        for i, av in enumerate(angular_velocities):
            now_rad[i] += av / fps
            this_radius = radius / (2 ** (i+1))
            x = int(next_center[0] + (this_radius * math.cos(math.radians(now_rad[i]))))
            y = int(next_center[1] + (this_radius * math.sin(math.radians(now_rad[i]))))
            next_center = (x, y)
            # cv2.circle(frame, (x, y), radius=int(this_radius), color=color)
            if i == (len(angular_velocities) - 1):
                orbits.append((x, y))
            # for o in range(len(orbits) - 1):
            #     cv2.line(frame, (orbits[o][0], orbits[o][1]), (orbits[o+1][0], orbits[o+1][1]),
            #              color=(0, 0, 255), thickness=2)
        # video.write(frame)

    # video.release()
    for o in range(len(orbits) - 1):
        cv2.line(img, (orbits[o][0], orbits[o][1]), (orbits[o + 1][0], orbits[o + 1][1]),
                 color=(0, 0, 255), thickness=2)

    # cv2.imwrite('wheels\wheels_' + str(angular_velocities[0]) + '_' +
    #             str(angular_velocities[1]) + '_' +
    #             str(angular_velocities[2]) + '.png', img)
    return img


def main3():
    img = np.zeros((1000, 1000, 3), dtype=np.uint8)
    center = (500, 500)
    radius = 400
    angular_velocities = [60, 180, 150]  # degree/s
    color = (255, 255, 255)

    # wheels(img, center, radius, angular_velocities, color)

    if not os.path.isdir('wheels'):
        os.mkdir('wheels')

    # angulars = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 330, 360]
    # size = sum(1 for _ in itertools.permutations(angulars, 3))
    # progress_bar = tqdm(total=size)
    # for a in itertools.permutations(angulars, 3):
    #     wheels(img, center, radius, a, color)
    #     progress_bar.update(1)

    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    fps = 20
    video_size = (1000, 1000)
    video = cv2.VideoWriter('wheels_orbit.mp4', fourcc, fps, video_size)
    progress_bar = tqdm(total=60)
    for i in np.arange(177, 183, 0.1):
        ret = wheels(img, center, radius, [i, 330, 30], color)
        video.write(ret)
        progress_bar.update(1)
    video.release()


if __name__ == '__main__':
    # main1()
    # main2()
    main3()
