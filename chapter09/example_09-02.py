#!/usr/bin/env python3"
# File Name: 未命名.py
# Author: wkangk
# Mail: wangkangchn@163.com
# Created Time: 2020-01-04 19:38:19 中国标准时间
#
"""
        学习opencv3 Example 9-2 python版
    控制鼠标在屏幕上绘制矩形框
"""
import cv2 as cv
import numpy as np

box = np.float32([-1.0, -1.0, .0, .0])  # 欲绘制的矩形框参数 (x, y, w, h)
drawing_box = False

def wh_to_lr(box):
    """ 将(x, y, w, h)转为左上右下(lx, ly, rx, ry)表示 """
    lx, ly, rx, ry = *box[:2], box[0] + box[2], box[1] + box[3]
    # 宽度小于0
    if box[2] < 0:
        lx = box[0] + box[2]
        rx = box[0]
    # 高度小于0
    if box[3] < 0:
        ly = box[1] + box[3]
        ry = box[1]
    return ((lx, ly), (rx, ry))

def draw_box(img, box):
    """ 将矩形框绘制到图像上 """
    print('draw_box: ', box)
    cv.rectangle(img, *wh_to_lr(box), color=(0, 255, 0))

## 按下左键开始绘制box, 送开键添加box到当前图像上
## 按下左键并拖动时调整box大小
def my_mouse_callback(event, x, y, flags, param):
    """
        回调函数参数列表必须这样写 !!!
    event:      事件
    x, y:       事件发生时鼠标所在的位置
    flags:      特殊键控制标志, (shift, ctrl, alt, ...)
    param:      用户需要传递的特殊参数(以元组的方式传递)
    """
    global box, drawing_box
    image = param
    # 处理鼠标事件
    if event == cv.EVENT_MOUSEMOVE:     # 鼠标移动, 移动时不画, 只记录位置, 当鼠标弹起时才进行绘制
        print('鼠标移动: ', x, y)
        if drawing_box:
            # 计算当前位置与起始位置的偏移量(默认向右移动鼠标)
            box[2] = x - box[0]     # width
            box[3] = y - box[1]     # height

    elif event == cv.EVENT_LBUTTONDOWN: # 左键按下, 开始绘制
        drawing_box = True
        box[:] = [x, y, 0, 0]   # 记录初始位置
        print('左键按下: ', box)

    elif event == cv.EVENT_LBUTTONUP:   # 左键弹起, 结束绘制
        print('左键弹起: ', box)
        drawing_box = False
        draw_box(image, box)


def _main(args):
    global box, drawing_box
    image = np.zeros((600, 600, 3), np.uint8)
    window_name = "Box Example"
    cv.namedWindow(window_name)

    # 注册鼠标的回调函数
    cv.setMouseCallback(window_name, my_mouse_callback, image)

    while True:
        # ~ print('循环') # 真的是线程
        temp = image.copy() # 在这次的绘制过程中, 不再绘制对image的修改
        if drawing_box:
            draw_box(temp, box)
        cv.imshow("Box Example", temp)
        if cv.waitKey(1) == 27:
            break
    cv.destroyAllWindows()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(_main(sys.argv))
