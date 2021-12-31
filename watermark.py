import cv2 as cv
import os
import tkinter
from tkinter import filedialog

current_dir = os.getcwd()


def browse_multiple_images():
    root = tkinter.Tk()
    root.withdraw()

    images_paths = filedialog.askopenfilenames(initialdir=current_dir + 'lib',
                                               title='Please select images')
    return images_paths


def browse_image():
    root = tkinter.Tk()
    root.withdraw()

    images_path = filedialog.askopenfilename(initialdir=current_dir + 'lib',
                                             title='Please select a watermark')
    return images_path


def select_img_options():
    select_options = int(input("Choose : \n 1- browse image or multiple images \n 2- enter image path \n "))
    if select_options == 1:
        return browse_multiple_images()
    elif select_options == 2:
        return str(input("enter image path : \n"))
    else:
        return browse_multiple_images()


def select_watermark_options():
    select_options = int(input("Choose watermark type : \n 1- image \n 2- text \n"))
    if select_options == 1:
        return browse_image()
    elif select_options == 2:
        return str(input("enter watermark context : \n"))
    else:
        return browse_multiple_images()


def resize(scale, img):
    scale_percent = scale
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    resized = cv.resize(img, dim, interpolation=cv.INTER_AREA)
    return resized


def calcCoordinates(img, watermark_img):
    h_img, w_img, _ = img.shape
    h_logo, w_logo, _ = watermark_img.shape

    center_y = int(h_img / 2)
    center_x = int(w_img / 2)
    top_y = center_y - int(h_logo / 2)
    left_x = center_x - int(w_logo / 2)
    bottom_y = top_y + h_logo
    right_x = left_x + w_logo

    return [top_y, bottom_y, left_x, right_x]


def get_removed_place(watermark_pos, original_img):
    removed_space = original_img[watermark_pos[0]: watermark_pos[1], watermark_pos[2]: watermark_pos[3]]
    return removed_space


def place_watermark(watermark_pos, watermark_img, original_img):
    removed = get_removed_place(watermark_pos, original_img)
    result = cv.addWeighted(removed, 1, watermark_img, 0.8, 0)

    original_img[watermark_pos[0]: watermark_pos[1], watermark_pos[2]: watermark_pos[3]] = result
    return original_img


def place_text_watermark(img, watermark_text, pos):
    font = cv.FONT_HERSHEY_SIMPLEX

    fontScale = 1
    color = (255, 255, 255)
    thickness = 2

    cv.putText(img, watermark_text, pos, font, fontScale, color, thickness, cv.LINE_AA)

    opacity = 40/100
    overlay = img.copy()
    output = img.copy()

    cv.addWeighted(overlay, opacity, output, 1 - opacity, 0, output)
    return output


def calcTextWatermarkPos(text, img):
    font = cv.FONT_HERSHEY_SIMPLEX

    textsize, _ = cv.getTextSize(text, font, 1, 2)
    textX = (img.shape[1] - textsize[0]) / 2
    textY = (img.shape[0] + textsize[1]) / 2
    pos = (int(textX), int(textY))
    return pos


if __name__ == '__main__':

    images_path = select_img_options()
    watermark_type = select_watermark_options()

    for img_path in images_path:

        img = cv.imread(img_path)
        img = resize(50, img)
        filename = os.path.basename(img_path)

        if os.path.exists(watermark_type):

            watermark_img = cv.imread(watermark_type)
            watermark_img = resize(10, watermark_img)

            watermark_pos = calcCoordinates(img, watermark_img)
            image_after_watermark = place_watermark(watermark_pos, watermark_img, img)

            cv.imwrite(current_dir + '\lib\watermarked_image_' + filename, img)

        else:
            watermark_text = watermark_type

            pos = calcTextWatermarkPos(watermark_text, img)
            output = place_text_watermark(img, watermark_text, pos)
            cv.imwrite(current_dir + '\lib\watermarked_text_' + filename, output)

    cv.waitKey(0)
