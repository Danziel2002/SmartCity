import cv2
import pytesseract as pt

def getTextFromImage(imageFile):


    image = cv2.imread(imageFile)
    #extract the text from the image and return it
    return pt.image_to_string(image, lang='ron')

