from PIL import Image
import pyautogui
import keyboard
# import random
import mouse
import time
import math

zoom_level_widths = [40, 20, 10]  # other zoom levels are bad
zoom = zoom_level_widths[int(input('Zoom level(0, 1, 2): '))]  # reading grid pixels from input zoom level
pyautogui.PAUSE = 0.035  # pause between pyautogui actions
MAX_DIST = 15  # how far is too far (it is about 19 pixels but less is better for high pings)


# distance between two points
def point_dist(p1, p2):
    if len(p1) != 2 or len(p2) != 2:
        raise ValueError('points should have only x and y values')
    return round(math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2), 3)


# stop if q is pressed
def stop():
    if keyboard.is_pressed('q'):
        return True
    return False


# main function for drawing an image
def painter():
    ignore_color = (255, 255, 255)  # color to ignore in the image
    # reading the image file
    file_name = input('Enter Image name with extension: ')
    file = Image.open('C:/Users/msara/Desktop/To Draw/' + file_name)
    file = file.convert('RGB')
    width, height = file.size
    color_dict = {}
    print('separating each color into a dictionary')
    for h in range(height):
        for w in range(width):
            color = file.getpixel((w, h))
            if color in color_dict:
                color_dict[color].append((w, h))
            else:
                color_dict[color] = [(w, h)]
    for i in color_dict.keys():
        if i == ignore_color:
            del color_dict[i]
            break

    print('sorting pixels for each color')
    # sort pixels by distance for each color
    for i in color_dict:
        sorted_list = [color_dict[i][0]]
        del color_dict[i][0]
        while len(color_dict[i]) > 0:
            distance_list = [point_dist(sorted_list[-1], _) for _ in color_dict[i]]
            sorted_list.append([x for _, x in sorted(zip(distance_list, color_dict[i]))][0])
            color_dict[i].remove(sorted_list[-1])
        color_dict[i] = sorted_list
    last_color = []

    while True:
        print('press "Ctrl + V" to start!')
        keyboard.wait('ctrl+v')
        x0, y0 = pyautogui.position()  # bottom right corner of the canvas
        # y0 = y0 - (height - 1) * zoom  # from bottom left
        x0, y0 = [x0 - (width - 1) * zoom, y0 - (height - 1) * zoom]  # convert to top left corner
        start_im = pyautogui.screenshot(region=(x0 - zoom / 2, y0 - zoom / 2,
                                                x0 + (width - 0.5) * zoom, y0 + (height - 0.5) * zoom))
        start_status = []
        for i in range(width):
            start_status.append([])
            for j in range(height):
                start_status[i].append(start_im.getpixel(((i + 0.5) * zoom, (j + 0.5) * zoom)))
        x_y_last = (0, 0)
        time.sleep(0.25)
        keyboard.press('esc')
        time.sleep(0.25)
        color_changed = False
        for i in color_dict:
            for j in color_dict[i]:
                if stop():
                    return
                x_y = (j[0] * zoom + x0, j[1] * zoom + y0)
                if start_status[j[0]][j[1]] == i:
                    continue
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
                time.sleep(0.038)
                x_y_last = x_y
            if color_changed:
                time.sleep(0.15)
            color_changed = False
