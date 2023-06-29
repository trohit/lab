#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# importing the qrcode library
import qrcode
import os
import sys
from qrcode.image.styles import colormasks, moduledrawers

# colors
# https://sites.google.com/view/paztronomer/blog/basic/python-colors

url = 'http://google.com/'

def qr_create(url:str, fg = "black", bg = "white"):
    tmp_qr_file = "tmp_qr.jpg"
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    # generating a QR code using the make() function
    print(f"generating a QR code using fg:{fg} bg:{bg} url:{url}")
    qr_img = qr.make_image(fill_color = fg, back_color = bg)
    # saving the image file
    qr_img.save(tmp_qr_file)
    return tmp_qr_file

# main
if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
    qr_create(url)
