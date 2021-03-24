# USAGE
# python compare.py

from skimage.metrics import structural_similarity
import argparse
import imutils
import cv2
import pytesseract
import os
import itertools
from PIL import Image
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def compare__(filenameRef, filenameToTest):
    imageref = cv2.imread(filenameRef)
    imageToTest = cv2.imread(filenameToTest)

    filename = os.path.splitext(os.path.basename(filenameToTest))[0]
    TAGED_TEXT = 'C:/Users/cyrin/OneDrive/Bureau/IC2/py/Screenshot/result_img/'+filename
    # TAGED_TEXT = os.path.splitext(filenameToTest)[0]
    print(TAGED_TEXT)
    # convert the images to grayscale
    grayref = cv2.cvtColor(imageref, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageToTest, cv2.COLOR_BGR2GRAY)

    # compute the Structural Similarity Index (SSIM) between the two
    # images, ensuring that the difference image is returned
    (score, diff) = structural_similarity(grayref, grayB, full=True)
    diff = (diff * 255).astype("uint8")
    print("SSIM: {}".format(score))

    # threshold the difference image, followed by finding contours to
    # obtain the regions of the two input images that differ
    thresh = cv2.threshold(diff, 0, 255,
                           cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    coordinations = {}
    coordinations['coordination'] = []
    # loop over the contours
    Words = {}
    Words['words'] = []
    boxes = pytesseract.image_to_data(imageToTest)
    issue = "%s \n" % os.path.basename(filenameToTest)
    issue += "SSIM: {} \n".format(score)
    count = 0
    i = 0
    for c in cnts:
        # compute the bounding box of the contour and then draw the
        # bounding box on both input images to represent where the two
        # images differ
        (x, y, w, h) = cv2.boundingRect(c)
        index_pos = None
        cv2.rectangle(imageToTest, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(imageToTest, str(i), (x + w - 25, y + h - 25),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (50, 50, 255), 2)
        cropped = imageref[y:y + h, x:x + w]
        text = pytesseract.image_to_string(cropped)
        count = len(cnts)

        coordinations['coordination'].append({
            "nummber": i,
            "text": text,
            "left": x,
            "top": y,
            "width": w,
            "height": h,
        })
        i = i+1

    if (count != 0):
        for coordination in coordinations['coordination']:
            issue += "Problemnummer: %s \n%s  \nKoordinationen:\nleft: %s \ntop: %s \nwidth: %s \nheight: %s  \n" % (
                coordination['nummber'], coordination['text'], coordination['left'], coordination['top'], coordination['width'], coordination['height'])
        with open(TAGED_TEXT+"_result.txt", "w") as text_file:
            text_file.write(issue)
    else:
        with open(TAGED_TEXT+"_result.txt", "w") as text_file:
            text_file.write("%s \nes gibt keinen fehler" %
                            os.path.basename(filenameToTest))

    # show the output images
    cv2.imwrite(TAGED_TEXT+"_result.png", imageToTest)
    print("done")
    cv2.waitKey(0)


srcDir = 'C:/Users/cyrin/OneDrive/Bureau/IC2/py/Screenshot/test_img'
files = os.listdir(srcDir)
images = []
for file in files:
    if file.endswith('.png') or file.endswith('.PNG') or file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.jepg') or file.endswith('.JEPG'):
        images.append(file)

imagesref = []
srcDirRef = 'C:/Users/cyrin/OneDrive/Bureau/IC2/py/Screenshot/ref_img'
filesref = os.listdir(srcDirRef)
for file in filesref:
    if file.endswith('.png') or file.endswith('.PNG') or file.endswith('.jpg') or file.endswith('.JPG') or file.endswith('.jepg') or file.endswith('.JEPG'):
        imagesref.append(file)


def compare__img():

    for a in images:
        for b in imagesref:
            imagename1 = (a.split("_")[-1]).split(".")[0]
            imagename2 = (b.split("_")[-1]).split(".")[0]
            if imagename1 == imagename2:
                image1 = Image.open(srcDir + '/' + a)
                image2 = Image.open(srcDirRef + '/' + b)
                if image1.size[1] > image2.size[1]:
                    diff = image1.size[1]-image2.size[1]
                    newimage = Image.new(
                        'RGB', (image2.size[0], diff), '#ffffff')
                    newimage.save(srcDirRef + '/a.png')
                    im1 = cv2.imread(srcDirRef + '/a.png')
                    im2 = cv2.imread(srcDirRef + '/' + b)
                    im_v = cv2.vconcat([im2, im1])
                    cv2.imwrite(srcDirRef + '/' + b, im_v)
                    os.remove(srcDirRef + '/a.png')
                elif image1.size[1] < image2.size[1]:
                    diff = image2.size[1]-image1.size[1]
                    newimage = Image.new(
                        'RGB', (image1.size[0], diff), '#ffffff')
                    newimage.save(srcDir + '/a.png')
                    im1 = cv2.imread(srcDir + '/a.png')
                    im2 = cv2.imread(srcDir + '/' + a)
                    im_v = cv2.vconcat([im2, im1])
                    cv2.imwrite(srcDir + '/' + a, im_v)
                    os.remove(srcDir + '/a.png')

                compare__(srcDirRef + '/' + b, srcDir + '/' + a)
                print("=========================================")


compare__img()
