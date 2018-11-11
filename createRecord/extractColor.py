import cv2

#imgとマスクの上下限を受け取ってマスクで抜き取った色のgrayスケールを返す
def extractColor(img,lC,uC):
    # 2hsv
    hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # make mask
    img_mask = cv2.inRange(hsv_img, lC, uC)
    # extract from mask
    img_color = cv2.bitwise_and(img, img, mask=img_mask)
    # 2gray
    gray = cv2.cvtColor(img_color, cv2.COLOR_BGR2GRAY)
    # binarization
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    return gray