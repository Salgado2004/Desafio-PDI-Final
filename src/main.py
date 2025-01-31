import cv2
import numpy as np

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

def apply_sobel(img):
    img_gray = img
    grad_x = cv2.Sobel(img_gray, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(img_gray, cv2.CV_64F, 0, 1, ksize=3)
    abs_grad_x = cv2.convertScaleAbs(grad_x)
    abs_grad_y = cv2.convertScaleAbs(grad_y)
    img_sobel = cv2.addWeighted(abs_grad_x, 0.5, abs_grad_y, 0.5, 0)
    return img_sobel

def apply_gabor_filter(image, ksize=31, sigma=4.0, theta=np.pi/4, lambd=10.0, gamma=0.5, psi=0):
    kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
    return cv2.filter2D(image, cv2.CV_8UC3, kernel)

for i in range(6):
    # 1. Aquisição
    img = cv2.imread(f"assets/img-{i+1}.jpg")
    if img is None:
        raise ValueError("Imagem não encontrada. Verifique o caminho.")
    
    # 2. Pré-processamento
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Equalização adaptativa do histograma para realce
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)

    # Aplicar suavização para reduzir ruídos
    blurred = cv2.GaussianBlur(enhanced, (5, 5), 0)

    cv2.imshow("Pre-processamento", stackImages(0.8, ([img, gray], [enhanced, blurred])))
    cv2.waitKey(0)

    # 3. Processamento
    # a) Detecção de bordas (Sobel + Binary Threshold)
    sobel = apply_sobel(blurred)
    edges = cv2.threshold(sobel, 96, 255, cv2.THRESH_BINARY)[1]

    # b) Análise de textura com Filtros de Gabor
    gabor = apply_gabor_filter(enhanced)

    combined = cv2.addWeighted(edges, 0.5, gabor, 0.5, 0)
    cv2.imshow("Processamento", stackImages(0.8, ([gabor, sobel], [combined, edges])))
    cv2.waitKey(0)

    # 4. Classificação
    dots = 0
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in contours:
        area = cv2.contourArea(c)
        x,y,w,h = cv2.boundingRect(c)
        if area > 5 and area < 100 and y < 204 and x > 50 and x < 400:
            cv2.drawContours(img, c, -1, (0,255,0), 2)
            dots+=1
    
    cv2.imshow("Contornos detectados", img)
    print(dots)
    cv2.waitKey(0)