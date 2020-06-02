from PIL import ImageGrab
import numpy as np
import keyboard
import cv2
import time

bbox = (10, 50, 800, 600)  # (x, y, width, height)

keys = ['w', 'a', 'd', 's']
vertices = np.array([[0, 600], [0, 200], [800, 200], [800, 600]])

low = np.array([26, 31, 114])       # lowest hsv value of road
high = np.array([100, 40, 148])     # highest hsv value of road

kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))

def key_press(i):
    keyboard.press(keys[0])
    if i > 50:
        keyboard.release(keys[0])

def forward():
    keyboard.press(keys[0])
    keyboard.release(keys[1])
    keyboard.release(keys[2])

def left():
    keyboard.press(keys[1])
    keyboard.release(keys[0])
    keyboard.release(keys[2])

def right():
    keyboard.press(keys[2])
    keyboard.release(keys[1])
    keyboard.release(keys[0])

def release_all_keys():
    keyboard.release(keys[2])
    keyboard.release(keys[1])
    keyboard.release(keys[0])

def drive(cent_x, cent_y):

    if cent_x != -1:

        if 800/2 - 30 <= cent_x <= 800/2 + 30:
            print('Forward')
            forward()

        elif cent_x < 800/2 - 30:
            print('Left')
            forward()
            left()

        elif cent_x > 800/2 + 30:
            print('Right')
            forward()
            right()

        else:
            print('All keys released!')
            release_all_keys()

def draw_contours(detected_contours, original_image):

    for c in detected_contours:
        if len(c) > 500:

            cv2.polylines(original_image, [c], True, (0, 255, 0))
            M = cv2.moments(c)

            if M["m00"] != 0:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.line(img, (cX - 10, cY), (cX + 10, cY), (0, 255, 0), 5)
                cv2.line(img, (cX, cY - 10), (cX, cY + 10), (0, 255, 0), 5)

                return cX, cY

            else:
                return -1, -1


def contour_detection(original_image):
    processed_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2HSV)
    contour = cv2.inRange(processed_image, low, high)       # returns contour of road based on colour in hsv
    processed_contour = cv2.morphologyEx(contour, cv2.MORPH_CLOSE, kernel)
    im, detected_contours, heir = cv2.findContours(processed_contour, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    try:
        cent_x, cent_y = draw_contours(detected_contours, original_image)
        drive(cent_x, cent_y)
    except:
        pass
    return original_image

for i in reversed(range(1, 10)):
    time.sleep(0.5)
    print(i, end = ' ')

# last = time.time()

i = 0

while True:

    img = np.array(ImageGrab.grab(bbox=bbox))
    cv2.imshow("test", contour_detection(img))
    # print('Time taken : {}'.format(time.time() - last))
    # last = time.time()
    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        cv2.destroyAllWindows()
        break
