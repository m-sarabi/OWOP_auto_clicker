import random

from PIL import Image, ImageGrab
import numpy as np
import pyautogui
import keyboard
import easygui
import letters
# import random
import mouse
import time
import math
import os

zoom_level_widths = [40, 20, 10]  # other zoom levels are bad
zoom = zoom_level_widths[int(input('Zoom level(0, 1, 2): '))]  # reading grid pixels from input zoom level
pyautogui.PAUSE = 0.035  # pause between pyautogui actions
MAX_DIST = 15  # how far is too far (it is about 19 pixels but less is better for high pings)
click_pause = 0.038


# stop if q is pressed
def stop():
    if keyboard.is_pressed('q'):
        return True
    return False


# distance between two points
def point_dist(p1, p2):
    if len(p1) != 2 or len(p2) != 2:
        raise ValueError('points should have only x and y values')
    return round(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2), 3)


def path_length(points_list):
    dist = 0
    for i in range(len(points_list) - 1):
        dist += point_dist(points_list[i + 1], points_list[i])
    return dist


def repeating_nn(points_list: list, timeout=5, min_repeat=2):
    # print('sorting pixels for each color')
    # sort pixels by distance for each color
    all_nn = []
    tic = time.time()
    indexes = list(range(len(points_list)))
    random.shuffle(indexes)
    repeats = 0
    for point_i in indexes:
        repeats += 1
        r_list = points_list.copy()
        sorted_list = [r_list[point_i]]
        del r_list[point_i]
        while len(r_list) > 0:
            distance_list = [point_dist(sorted_list[-1], _) for _ in r_list]
            sorted_list.append([x for _, x in sorted(zip(distance_list, r_list))][0])
            r_list.remove(sorted_list[-1])
        all_nn.append(sorted_list)
        if (time.time() - tic) > timeout and repeats >= min_repeat:
            break
    all_nn_dist = [path_length(i) for i in all_nn]
    return [x for _, x in sorted(zip(all_nn_dist, all_nn))][0]


# def sort_by_distance(image_dict):
#     print('sorting pixels for each color')
#     # sort pixels by distance for each color
#     for i in image_dict:
#         sorted_list = [image_dict[i][0]]
#         del image_dict[i][0]
#         while len(image_dict[i]) > 0:
#             distance_list = [point_dist(sorted_list[-1], _) for _ in image_dict[i]]
#             sorted_list.append([x for _, x in sorted(zip(distance_list, image_dict[i]))][0])
#             image_dict[i].remove(sorted_list[-1])
#         image_dict[i] = sorted_list
#     return image_dict


def paste_image(ignore_color=(255, 255, 255), image=None, text=False):
    # reading the image from file if not provided
    if image is None:
        while True:
            img_src = input('[f]: from file\n[c] from clipboard\n')
            match img_src:
                case 'f':
                    image = Image.open(
                        easygui.fileopenbox(msg='Select Image to Draw', default=os.path.expanduser("~/Desktop/"),
                                            filetypes=["*.png", "*.bmp", "*.jpg", "Image files"])).convert('RGB')
                    break
                case 'c':
                    image = ImageGrab.grabclipboard().convert('RGB')
                    break
                case _:
                    print('get gud!')
    width, height = image.size
    image_dict = {}
    print('separating each color into a dictionary')
    for h in range(height):
        for w in range(width):
            color = image.getpixel((w, h))
            if color in image_dict:
                image_dict[color].append((w, h))
            else:
                image_dict[color] = [(w, h)]
    if ignore_color:
        for i in image_dict.keys():
            if i == ignore_color:
                del image_dict[i]
                break
    # image_dict = sort_by_distance(image_dict)
    if text:
        painter(image_dict, width, height, 10, 100)
    else:
        painter(image_dict, width, height, 5, 3)
    return image_dict, width, height


# main function for drawing an image
def painter(image_dict, width, height, sort_time, sort_repeat):
    last_color = []
    print('press "Ctrl + V" to start!')
    keyboard.wait('ctrl+v')
    x0, y0 = pyautogui.position()
    # y0 = y0 - (height - 1) * zoom  # from bottom left
    # x0, y0 = [x0 - (width - 1) * zoom, y0 - (height - 1) * zoom]  # convert to top left corner
    start_im = pyautogui.screenshot(region=(x0 - zoom / 2, y0 - zoom / 2,
                                            x0 + (width - 0.5) * zoom, y0 + (height - 0.5) * zoom))
    start_status = []
    for i in range(width):
        start_status.append([])
        for j in range(height):
            start_status[i].append(start_im.getpixel(((i + 0.5) * zoom, (j + 0.5) * zoom)))
    x_y_last = (0, 0)
    time.sleep(0.25)
    color_changed = False
    for i in image_dict:
        click_count = 0
        c = 0
        while c < len(image_dict[i]):
            if start_status[image_dict[i][c][0]][image_dict[i][c][1]] == i:
                image_dict[i].remove(image_dict[i][c])
                continue
            c += 1
        if len(image_dict[i]) == 0:
            continue
        image_dict[i] = repeating_nn(image_dict[i], timeout=sort_time, min_repeat=sort_repeat)
        for j in image_dict[i]:
            if stop():
                return
            x_y = (j[0] * zoom + x0, j[1] * zoom + y0)
            # if start_status[j[0]][j[1]] == i:
            #     continue
            if not color_changed:
                color_changed = True
                if last_color != [i[0], i[1], i[2]]:
                    pyautogui.press('f')
                    time.sleep(0.1)
                    pyautogui.write(f'{i[0]},{i[1]},{i[2]}')
                    last_color = [i[0], i[1], i[2]]
                    time.sleep(0.1)
                    pyautogui.press('return')
            if math.sqrt((x_y[0] - x_y_last[0]) ** 2 + (x_y[1] - x_y_last[1]) ** 2) > zoom * MAX_DIST:
                time.sleep(0.15)
                mouse.move(x_y[0], x_y[1])
                time.sleep(0.15)
            mouse.move(x_y[0], x_y[1])
            mouse.click()
            click_count += 1
            if click_count <= 50:
                time.sleep(click_pause/2)
            else:
                time.sleep(click_pause)
            x_y_last = x_y
        if color_changed:
            time.sleep(0.15)
        color_changed = False


def text_to_image(text, text_color, background_color):
    image_list = []
    for i in range(8):
        image_list.append([])
    for i in range(len(image_list)):
        for char_index in range(len(text)):
            if text[char_index] in letters.LettersDict.keys():
                image_list[i].extend(letters.LettersDict[text[char_index]][i])
                if char_index < len(text) - 1:
                    image_list[i].append(0)
    for i in range(len(image_list)):
        for j in range(len(image_list[i])):
            if image_list[i][j] == 1:
                image_list[i][j] = text_color
            else:
                image_list[i][j] = background_color
    image_array = np.asarray(image_list, dtype=np.uint8)
    return Image.fromarray(image_array).convert('RGB')


def write_text(color=(0, 0, 0), background=(255, 255, 255)):
    while True:
        text = input('Enter the text:')
        text_image = text_to_image(text, color, background)
        paste_image(image=text_image, text=True)
