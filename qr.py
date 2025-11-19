# -*- coding: utf-8 -*-
import qrcode
import cv2
import cv2u
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import datetime


# matplotlibでの日本語の文字化け(豆腐)を回避するための設定
plt.rcParams['font.family'] = 'MS Gothic'

date = datetime.date.today()
height, width = 8.27, 11.69

def create_qr():
  # QRコード画像作成
  qr = qrcode.QRCode(border=1)
  qr.add_data("https://google.co.jp/")
  qr.make()

  # 画像として保存
  img = qr.make_image()
  return img
#   img.save("./qr_code.png")

if __name__ == '__main__':
  create_qr()