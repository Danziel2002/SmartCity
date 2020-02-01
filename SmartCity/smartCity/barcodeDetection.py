# import the necessary packages
from pyzbar import pyzbar
import cv2

# construct the argument parser and parse the arguments
def  readBarcode(imageFile):
    image = cv2.imread(imageFile)
    text = 'foo'

    # find the barcodes in the image and decode each of the barcodes
    barcodes = pyzbar.decode(image)
    # loop over the detected barcodes
    for barcode in barcodes:
        (x, y, w, h) = barcode.rect
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(image, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0, 0, 255), 2)
        return barcodeData
