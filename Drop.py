try:
    from PIL import Image
except ImportError:
    import Image

import pytesseract
import requests
import numpy as np
import matplotlib.pyplot as plt
import cv2
import random

from os import listdir
from os.path import isfile, join
import os, re

import Card as Card


class Drop:

    @staticmethod
    def download(url):
        filename = "tmp_imgs/main" + str(random.randint(0, 1000)) + ".png"

        while True:
            try:
                with open(filename, "wb") as file:
                    response = requests.get(url)
                    file.write(response.content)
                    break
            except Exception as e:
                print(e)
                print("Errore nel download delle carte, riprovo")
        return filename

    @staticmethod
    def get_card(path, input, n_img):
        img = cv2.imread(input)
        img = cv2.resize(img, (0, 0), interpolation=cv2.INTER_LANCZOS4, fx=2, fy=2)
        crop_img = img[0:0 + 414 * 2, n_img * 278 * 2:n_img * 278 * 2 + 278 * 2]
        crop_img = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
        cv2.imwrite(path, crop_img)

    @staticmethod
    def get_top(input, output):
        img = cv2.imread(input, 0)
        crop_img = img[65 * 2:105 * 2, 45 * 2:230 * 2]
        blur = cv2.GaussianBlur(crop_img, (3, 3), 0)
        # thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_TRIANGLE,3,3)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        invert = 255 - opening
        cv2.imwrite(output, invert)

    @staticmethod
    def get_bottom(input, output):
        img = cv2.imread(input, 0)
        crop_img = img[55 * 2 + 255 * 2:110 * 2 + 255 * 2, 40 * 2:225 * 2]
        blur = cv2.GaussianBlur(crop_img, (3, 3), 0)

        # thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,3,3)
        thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY_INV)[1]

        # Morph open to remove noise and invert image
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        invert = 255 - opening
        cv2.imwrite(output, invert)

    def __init__(self, url):
        print("Drop object creation in progress...")

        fname = Drop.download(url)
        path_to_ocr = "src_to_ocr"

        nonce = str(random.randint(0, 1000))
        card_name = "card{}" + nonce + ".png"
        top_name = "top{}" + nonce + ".png"
        bottom_name = "bottom{}" + nonce + ".png"

        for i in range(0, 3):
            Drop.get_card(card_name.format(i + 1), fname, i)
            Drop.get_card(card_name.format(i + 1), fname, i)
            Drop.get_card(card_name.format(i + 1), fname, i)

        for i in range(0, 3):
            Drop.get_top(card_name.format(i + 1), path_to_ocr + "/" + top_name.format(i + 1))
            Drop.get_bottom(card_name.format(i + 1), path_to_ocr + "/" + bottom_name.format(i + 1))

        self.cards = []
        for i in range(0, 3):
            top = pytesseract.image_to_string(Image.open(path_to_ocr + "/" + top_name.format(i + 1)), lang='eng',
                                              config='--psm 6')
            bottom = pytesseract.image_to_string(Image.open(path_to_ocr + "/" + bottom_name.format(i + 1)), lang='eng',
                                                 config='--psm 6')

            card_top = "".join(re.findall(r"[0-9a-zA-Z?!@:#+-_=\r\n ]+", top)).strip().replace("\n", " ")
            card_bottom = "".join(re.findall(r"[0-9a-zA-Z?!@:#+-_=\r\n ]+", bottom)).strip().replace("\n", " ")

            self.cards.append(Card.Card(card_top, card_bottom))

        print("Constructed drop object...")

        # Rimozione dei file creati
        for i in range(0, 3):
            os.remove(card_name.format(i + 1))
            os.remove(path_to_ocr + "/" + top_name.format(i + 1))
            os.remove(path_to_ocr + "/" + bottom_name.format(i + 1))
        os.remove(fname)

    def isCharacter(self, people):
        for i in range(0, 3):
            if self.cards[i].isCharacter(people):
                return i + 1
        return False

    def isAnime(self, anime):
        for i in range(0, 3):
            if self.cards[i].isAnime(anime):
                return i + 1
        return False

    def get_choice(self):
        with open("keywords/characters", "r") as characters:
            for character in characters.readlines():
                is_c = self.isCharacter(character)
                if is_c:
                    print(f"Found {character.strip()} character in the last drop")
                    return is_c

        with open("keywords/animes", "r") as animes:
            for anime in animes.readlines():
                is_a = self.isAnime(anime)
                if is_a:
                    print(f"Found {anime.strip()} anime in the last drop")
                    return is_a
        return random.choice([1, 2, 3])

    def __str__(self):
        s = []

        for i in range(0, 3):
            s.append(f"Card n°{i + 1}: {self.cards[i]}")
        return "\n".join(s)
