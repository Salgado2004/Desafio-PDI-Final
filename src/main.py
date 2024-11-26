import cv2

for i in range(6):
    # Ler a imagem
    img = cv2.imread(f"assets/img-{i+1}.jpg")
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    B, G, R = cv2.split(img)

    # Exibir a imagem
    cv2.imshow("Normal", img)
    cv2.imshow("Cinza", gray)
    cv2.imshow("Red", R)
    cv2.waitKey(0)