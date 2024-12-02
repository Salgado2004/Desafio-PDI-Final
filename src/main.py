import cv2

def sobel(img):
    img_gray = img
    grad_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    img_sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return img_sobel

for i in range(6):
    # Ler a imagem
    img = cv2.imread(f"assets/img-{i+1}.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    B, G, R = cv2.split(img)

    # Exibir a imagem
    cv2.imshow("Red", R)
    cv2.imshow("Sobel", sobel(R))
    cv2.waitKey(0)