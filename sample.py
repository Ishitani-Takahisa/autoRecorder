import cv2
from matplotlib import pyplot as plt

# 定数定義
ORG_WINDOW_NAME = "org"
GRAY_WINDOW_NAME = "gray"
CANNY_WINDOW_NAME = "canny"

ORG_FILE_NAME = "org.jpg"
GRAY_FILE_NAME = "gray.png"
CANNY_FILE_NAME = "canny.png"

# 元の画像を読み込む
# org_img = cv2.imread("./sample125689x.png", cv2.IMREAD_UNCHANGED)
# グレースケールに変換
gray = cv2.imread("./sample125689x.png", cv2.IMREAD_GRAYSCALE)
# エッジ抽出
canny_img = cv2.Canny(gray, 100, 200)
# _, contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


plt.imshow(canny_img)
plt.show()