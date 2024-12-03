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
    # a) Detecção de bordas (Canny)
    edges = cv2.Canny(blurred, 50, 150)

    # b) Análise de textura com Filtros de Gabor
    def apply_gabor_filter(image, ksize=31, sigma=4.0, theta=np.pi/4, lambd=10.0, gamma=0.5, psi=0):
        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
        return cv2.filter2D(image, cv2.CV_8UC3, kernel)

    gabor = apply_gabor_filter(enhanced)
    
    cv2.imshow("Processamento", stackImages(0.8, ([edges], [gabor])))
    cv2.waitKey(0)

    # 4. Pós-processamento
    combined = cv2.addWeighted(edges, 0.5, gabor, 0.5, 0)
    cv2.imshow('Resultado', combined)
    cv2.waitKey(0)