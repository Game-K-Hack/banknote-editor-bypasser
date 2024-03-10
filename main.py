import cv2
import random
import numpy as np

NUMBER_OF_IMAGE = 15
H = 50
W = 50
SET_PIXEL_OF_KEEP_SIZE = True
IMAGE = "image.jpg"

img = cv2.imread(IMAGE)
imgheight, imgwidth, _= img.shape

images = []

for y in range(0, imgheight, H):
    for x in range(0, imgwidth, W):
        x1 = x+W if x+W < imgwidth else None
        y1 = y+H if y+H < imgheight else None
        images.append({
            "img": img[y:y1, x:x1],
            "pos": (x, y)
        })

limg = len(images)-1
step = limg // NUMBER_OF_IMAGE

# load base image
img_base = cv2.imread(IMAGE)
# mix image list
random.shuffle(images)

index_filename = 1
reste = limg % NUMBER_OF_IMAGE

for i in range(0, limg, step):
    # create transparent image
    height, width, _ = img_base.shape
    new_img = np.zeros((height, width, 4), dtype=np.uint8)

    if SET_PIXEL_OF_KEEP_SIZE:
        new_img[0, 0] = [0, 0, 0, 1]
        new_img[height-1:height, width-1:width] = [0, 0, 0, 1]

    if reste > 0:
        step += 1

    for img in images[i:i+step if i+step < limg else None]:
        x, y = img["pos"]
        image = img["img"]
        y1, x1, _ = image.shape
        new_img[y:y+y1, x:x+x1] = cv2.cvtColor(image, cv2.COLOR_BGR2BGRA)

    cv2.imwrite(f"./output/frame{index_filename}.png", new_img)
    index_filename += 1

    if i+step > limg:
        break