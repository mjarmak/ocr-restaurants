#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Tasdik Rahman
# @Date:   2016-03-26
# @Last Modified by:   Tasdik Rahman
# @Last Modified time: 2016-03-29 19:01:05
# @MIT License
# @http://tasdikrahman.me
# @https://github.com/prodicus

"""
Automates the task of uploading a menu image to http://free-ocr.com and get
OCR'd menu text.

References
==========

[1]:  http://stackoverflow.com/a/33691162/3834059
"""

import os
import json

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

PATH = os.path.abspath(os.path.join("."))
MENU_PATH = os.path.join(PATH, "menu_images")
RESULT_PATH = os.path.join(PATH, "menu_text")
URL = "http://www.free-ocr.com/"


def clean_raw_text(raw_text):
    """
    cleans the raw_text of empty strings and integers

    :param raw_text: the text to be cleaned and returned back to
                     make_hotel_file()
    :returns: A iterable list of the menu items

    Example
    =======

    # >>>raw_text

    'SALADS\n\nClassical caesar salad with parmesan shaving: and garlic \
    bread\n\nCandied walnuts, orange segments and mixed greens tossed \
    in\norange sesame dressing\n\nCherry tomatoes, olives and cheese with \
    mixed greens and\nlemon oregano dressing\n\nGrilled aubergine with wild \
    rocket and balsamic vinaigrette\n\nSteamed potato, orange segments, \
    hordboiled egg and\nconfit base with olive oil dressing\n\nYoppings non \
    veg: chickenf‘prawn\n\nSOUPS\n\nWild mushroom creamy soup gamlilied with \
    garlic toast\nCreamed broccoli soup garnished with garlic cheese \
    toast\n\nTraditional Spanish gazpocho, cold tomato soup topped\nwith \
    basil and olive oil\n\nBURGERS: Served With Fries And House Salad\n\nBeef\
    party cooked to perfection topped with sliced cheese,\nsauteed onion,\
    mushrooms, ialapenos and tomatoes\n\nChicken patty topped with sliced \
    cheese, cucumber, onion\nand coiun mayonnaise \
    \n\n300\n\n300\n\n300\n\n350\n\n400\n\n90\n\n200\n200\n\n250\n350\n\n350'

    # >>> filter_cleaned
    ['SALADS', 'Classical caesar salad with parmesan shaving and garlic bread',\
     'Candied walnuts, orange segments and mixed greens tossed in',\
     'orange sesame dressing', 'Cherry tomatoes, olives and cheese with mixed\
      greens and', 'lemon oregano dressing', 'Grilled aubergine with wild \
      rocket and balsamic vinaigrette', 'Steamed potato, orange segments, \
      hordboiled egg and', 'confit base with olive oil dressing', 'Yoppings \
      non veg: chickenf‘prawn', 'SOUPS', 'Wild mushroom creamy soup gamlilied \
      with garlic toast', 'Creamed broccoli soup garnished with garlic cheese\
      toast', 'Traditional Spanish gazpocho, cold tomato soup topped', \
      'with basil and olive oil', 'BURGERS: Served With Fries And House \
      Salad', 'Beef party cooked to perfection topped with sliced cheese,',\
      'sauteed onion, mushrooms, ialapenos and tomatoes', 'Chicken patty \
      topped with sliced cheese, cucumber, onion', 'and coiun mayonnaise']
    """
    # loads the raw_text and cleans the empty strings from the list
    filter_cleaned = [x for x in filter(bool, raw_text.split('\n'))]
    # cleaning the integers in the list
    return [x for x in filter_cleaned if not x.isdigit()]


def get_raw_ocr_text(menu):
    return 'SALADS\n\nClassical caesar salad with parmesan shaving: and garlic \
    bread\n\nCandied walnuts, orange segments and mixed greens tossed \
    in\norange sesame dressing\n\nCherry tomatoes, olives and cheese with \
    mixed greens and\nlemon oregano dressing\n\nGrilled aubergine with wild \
    rocket and balsamic vinaigrette\n\nSteamed potato, orange segments, \
    hordboiled egg and\nconfit base with olive oil dressing\n\nYoppings non \
    veg: chickenf‘prawn\n\nSOUPS\n\nWild mushroom creamy soup gamlilied with \
    garlic toast\nCreamed broccoli soup garnished with garlic cheese \
    toast\n\nTraditional Spanish gazpocho, cold tomato soup topped\nwith \
    basil and olive oil\n\nBURGERS: Served With Fries And House Salad\n\nBeef\
    party cooked to perfection topped with sliced cheese,\nsauteed onion,\
    mushrooms, ialapenos and tomatoes\n\nChicken patty topped with sliced \
    cheese, cucumber, onion\nand coiun mayonnaise \
    \n\n300\n\n300\n\n300\n\n350\n\n400\n\n90\n\n200\n200\n\n250\n350\n\n350'


def make_hotel_file(hotel, menu_list):
    """
    Will create the hotel directory inside the 'RESULT_PATH' and store the
    OCR'd text inside it.

    :param hotel: the name of the hotel for which the list of images is to
                  be uploaded
    :param menu_list: the menu images for the hotel with absolute paths to it
    """
    hotel_menu_path = os.path.join(RESULT_PATH, hotel)
    hotel_file_name = "{0}.txt".format(hotel_menu_path)
    cleaned_menu = []  # stores all the ocr'd menu of the hotel

    # create the directory, if it does not exists for storing the ocrd menus
    with open(hotel_file_name, 'w') as f:
        for menu in menu_list:
            # use tesseract
            raw_text = get_raw_ocr_text(menu)
            if raw_text:
                # clean this raw text and append to the menu content
                cleaned_menu.extend(clean_raw_text(raw_text))
            else:
                continue

        # converting the list to JSON format for easy readability
        json_dict = {
            "menu_items": cleaned_menu,
            "restaurant_name": hotel
        }

        # writing this JSON to the hotel_file
        json.dump(json_dict, f, sort_keys=True, indent=4, ensure_ascii=False)


def get_image_list(hotel, menus):
    """
    Gets the image list (full path) for each hotel and returns that list

    Example
    =======

    For a file

    menu_images
        │   ├── 3-kings-kafe-kitchen-marathahalli-listing
        │   ├── 3-kings-kafe-kitchen-marathahalli-listing_0.jpg

    Returns something like
    ======================

    /home/tasdik/Documents/github/foodoh/ocrd_menus/menu_images/ \
    3-kings-kafe-kitchen-marathahalli-listing/ \
    3-kings-kafe-kitchen-marathahalli-listing_3.jpg'

    :param hotel: the name of the hotel for which the list of images is to
                  be uploaded
    :param menus: returns the list of images with its absolute path in the
                  file system
    :returns: the menu_list with it's absolute path for that particular hotel

    """
    menu_list = [menu for menu in map(lambda x: os.path.join(
        MENU_PATH, hotel, x), menus)]
    return menu_list


def run_ocr():
    for hotel in os.listdir(MENU_PATH):
        # return the list of menus in the hotel dir
        # each hotel typically has 4 menus in it
        # scraped from BURPP

        # skipping the hotel if it has already been processed
        hotel_menu = os.path.join(RESULT_PATH, hotel)
        hotel_menu += '.txt'
        if os.path.exists(hotel_menu):
            continue

        else:
            menu_list = get_image_list(
                hotel, os.listdir(os.path.join(MENU_PATH, hotel)))
            """
            feed this list to a helper function which makes the hotel dir and
            calls selenium
            """
            make_hotel_file(hotel, menu_list)

def run():
    cleaned_menu = []  # stores all the ocr'd menu of the hotel
    menu = 'test_menu'

    output_file = 'output.txt'

    with open(output_file, 'w') as f:

        # use tesseract
        raw_text = get_raw_ocr_text(menu)
        if raw_text:
            # clean this raw text and append to the menu content
            cleaned_menu.extend(clean_raw_text(raw_text))
        else:
            print('nope')

        # converting the list to JSON format for easy readability
        json_dict = {
            "menu_items": cleaned_menu,
            "restaurant_name": menu
        }

        # writing this JSON to the hotel_file
        json.dump(json_dict, f, sort_keys=True, indent=4, ensure_ascii=False)

run()
