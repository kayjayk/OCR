#!/usr/bin/env python
# coding: utf-8

# In[1]:


from PIL import Image
from pytesseract import image_to_string
import argparse
import cv2
import os
import fitz
import matplotlib.pyplot as plt
import matplotlib.image as mpimg


class TesseractApplication:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_dir, self.file_name = os.path.split(file_path)
        self.file_name_wo_ext = self.file_name.split('.pdf')[0]

    def convert_pdf_to_png(self, png_save_dir):
        
        doc = fitz.open(self.file_path)
        output_png_list = list()

        for i in range(doc.pageCount):
            page = doc.loadPage(i) #number of page
            pix = page.getPixmap()
            output_png = os.path.join(png_save_dir, self.file_name_wo_ext) + '_{}.png'.format(i)
            output_png_list.append(output_png)
            pix.writePNG(output_png)
            # plt.rcParams["figure.figsize"] = (30,15)
            # img = mpimg.imread(output)

            ## img 확인하고 싶다면
            # plt.imshow(img)
            # plt.show()
        self.output_png_list = output_png_list
        
    def convert_png_to_txt(self, txt_save_dir, lang):
        
        text_of_all = list()
        for output in self.output_png_list:
            text_of_a_page = image_to_string(output, lang=lang) 
            # ex. ('kor'), ('kor+eng') if want to do both kor and eng, e.g 'kor+eng'
            text_of_all.append(text_of_a_page)
            
        text = ''.join(text_of_all)
        with open(os.path.join(txt_save_dir, self.file_name_wo_ext) + '.txt', "w") as f:
            f.write(text)