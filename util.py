import urllib.request ,time
from PIL import Image 
from selenium.webdriver.common.by import By
import vk_captchasolver as vc
# Retrieving the resource located at the URL 
# and storing it in the file name a.png 
def download_image(url):
    urllib.request.urlretrieve(url, "demo.jpeg") 
    
    # Opening the image and displaying it (to confirm its presence) 
    img = Image.open(r"demo.jpeg") 
    img.show()

from PIL import Image, ImageFilter, ImageChops
from pytesseract import image_to_string
import cv2
import numpy,pytesseract
# pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'


def preprocess_image_using_pil(image_path):
    # unblur, sharpen filters
    img = Image.open(image_path)
    img = img.convert("RGBA")

    pixdata = img.load()

    # Make the letters bolder for easier recognition
    
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][0] < 90:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][1] < 136:
                pixdata[x, y] = (0, 0, 0, 255)

    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixdata[x, y][2] > 0:
                pixdata[x, y] = (255, 255, 255, 255)

    # And sharpen it
    img.filter(ImageFilter.SHARPEN)
    img.save("input-black.gif")

    #   Make the image bigger (needed for OCR)
    basewidth = 1000  # in pixels
    im_orig = Image.open('input-black.gif')
    wpercent = (basewidth/float(im_orig.size[0]))
    hsize = int((float(im_orig.size[1])*float(wpercent)))
    big = img.resize((basewidth, hsize), Image.ANTIALIAS)

    # tesseract-ocr only works with TIF so save the bigger image in that format
    ext = ".tif"
    tif_file = "input-NEAREST.tif"
    big.save(tif_file)
    
    return tif_file


def get_captcha_text_from_captcha_image(captcha_path):
    # Preprocess the image befor OCR
    tif_file = preprocess_image_using_opencv(captcha_path)
    # Perform OCR using tesseract-ocr library
    image = Image.open(tif_file)
    ocr_text = image_to_string(image, config="--psm 6")
    alphanumeric_text = ''.join(e for e in ocr_text)

    return alphanumeric_text

def binarize_image_using_pil(captcha_path, binary_image_path='input-black-n-white.gif'):
    im = Image.open(captcha_path).convert('L')
 
    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if im.getpixel((i,j)) > 127:
                im.putpixel((i,j), 255)
            else:
                im.putpixel((i,j), 0)

    im.save(binary_image_path)
    return binary_image_path


def binarize_image_using_opencv(captcha_path, binary_image_path='input-black-n-white.jpg'):
    img = cv2.imread(captcha_path)
    im_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # although thresh is used below, gonna pick something suitable
    im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]
    cv2.imwrite(binary_image_path, im_bw)
    return binary_image_path


def preprocess_image_using_opencv(captcha_path):
    bin_image_path = binarize_image_using_opencv(captcha_path)

    im_bin = Image.open(bin_image_path)
    
    basewidth = 340  # in pixels
    wpercent = (basewidth/float(im_bin.size[0]))
    hsize = int((float(im_bin.size[1])*float(wpercent)))
    big = im_bin.resize((basewidth, hsize), Image.NEAREST)
    
    # tesseract-ocr only works with TIF so save the bigger image in that format
    ext = ".tif"
    tif_file = "input-NEAREST.tif"
    big.save(tif_file)

    return tif_file


def take_screen_shot(driver):
    driver.save_screenshot("screenshot.png")

    # Get the size and location of the element you want to clip
    element = driver.find_element(By.XPATH,'//*[@id="captcha_image"]')
    element_location = element.location
    element_size = element.size

    # Coordinates of the element
    left = element_location['x']
    top = element_location['y']
    right = element_location['x'] + element_size['width']
    bottom = element_location['y'] + element_size['height']

    # Open the screenshot
    screenshot = Image.open("screenshot.png")

    # Crop the screenshot to the specified coordinates
    clipped_image = screenshot.crop((left, top, right, bottom))

    # Save the clipped image
    clipped_image.save("clipped_image.png")
    return 'clipped_image.png'


def resolve_captcha(driver):
    image_pth = take_screen_shot(driver=driver)
    text = img2text(image_pth)
    # print(f'>>>image_url {image_pth}<<<')
    # text = vc.solve(image_pth)
    # print('>>>>>>>>>>>>',text,"<<<<<<<<<<<<<<<<<<")
    captcha_input_box = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[2]/div/form/div/input')  # captcha input
    print(f'<<<<<<<<{text}>>>>>>>>>>>>>>>>>>')
    captcha_input_box.clear()
    captcha_input_box.send_keys(text)

def click_search(driver):
    search_button = driver.find_element(By.XPATH, '/html/body/div[1]/div/main/div[2]/div/form/button[1]')  # invalid captcha input
    search_button.click()
    time.sleep(2)

def img2text(URL):
    '''
        take that image and return 
        its content
    '''
    img = cv2.imread(URL)
    im = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    config = ('-l eng --oem 1 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzQWERTYUIOPASDFGHJKLZXCVBNM --psm 6')
    text = pytesseract.image_to_string(im, config=config)
    text2 = text.rstrip('\n')
    print(text2)
    return (text2)