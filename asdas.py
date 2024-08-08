import cv2
from pyzbar.pyzbar import decode
import datetime
import time
import xlsxwriter
tarih = datetime.datetime.now()
tarih_str = tarih.strftime("%Y-%m-%d")
dosya_ad = f"mesai_takip_{tarih_str}.txt"

f = open(dosya_ad, "r")
datas = []
for i in f:
    print(i)
    datas.append(i)
print(datas)
