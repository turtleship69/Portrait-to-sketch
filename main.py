import cv2
filename = 'nell.jpg'

def sketcher(input):
    img = cv2.imread(filename)
    gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) 
    inverted_gray_image = 255 - gray_image
    cv2.destroyAllWindows()
    blurred_img = cv2.GaussianBlur(inverted_gray_image, (21,21),0) 
    inverted_blurred_img = 255 - blurred_img
    pencil_sketch_IMG = cv2.divide(gray_image, inverted_blurred_img, scale = 256.0)
    return pencil_sketch_IMG

    
#Show the original image
#cv2.imshow('Original Image', cv2.imread("nell.jpg"))
#Show the new image pencil sketch

sketch = sketcher("nell.jpg")
#cv2.imshow('Pencil Sketch', sketch)
#cv2.waitKey(0)
cv2.imwrite('sketch 2.png', sketch)
#Display the window infinitely until any keypress
