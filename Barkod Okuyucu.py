import cv2
from pyzbar.pyzbar import decode
import datetime
import time
import xlsxwriter
kamera = cv2.VideoCapture(0)
current_kod = 0


kod = -1

def unique(list1):
 

    list_set = set(list1)

    unique_list = (list(list_set))
    aaa = []
    for x in unique_list:
        print(x)
        aaa.append(x)
        #return x
    return aaa
while True:
    
    ret, resim = kamera.read()
    time.sleep(0.1)

    kodlar = decode(resim)

    if len(kodlar) > 0:
        if (current_kod != kod):
            # ilk karekodu al
            kod = kodlar[0][0].decode('utf-8') #stringe çevir
            print('Sicil Numaranız:', kod)
            current_kod = kod

            # tarih bilgisini al
            tarih = datetime.datetime.now()
            tarih_str = tarih.strftime("%Y-%m-%d")
            # dosya adını oluştur
            dosya_ad = f"mesai_takip_{tarih_str}.txt"



            # sicil numarası ve zamanı dosyaya yazdır
            from datetime import datetime

            # get current datetime
            dt = datetime.now()
            #print('Datetime is:', dt)

            # get weekday name
            #print('day Name:', dt.strftime('%A'))
            daystr = dt.strftime('%A')
            


            with open(dosya_ad, "a") as f:
                f.write(f"{daystr} _ {kod} _ {tarih.strftime('%H:%M:%S')}\n")
           
            #buradan sonra python işlemleri yapılacak

            import os

            tarih = datetime.now()
            tarih_str = tarih.strftime("%Y-%m-%d")
            dosya_ad = f"mesai_takip_{tarih_str}.txt"

            f = open(dosya_ad, "r")
            datas = []
            sicil = []
            for i in f:
                #print(i)
                try:
                    datas.append(i)
                    spltt = i.split("_")
                    parca = spltt[1]
                    sicil.append(parca)
                except:
                    print(1)

            u_sicil = unique(sicil)
            print("uniq: ",u_sicil)
            for u_sic in u_sicil:
                #print(u_sicil)
                search_data = []
                for data in datas:
                    parcalar = data.split("_")
                    scl = parcalar[1]
                    gun = parcalar[0]
                    saat = parcalar[2]
                    scl = parcalar[1]
                    if(scl == u_sic):
                        search_data.append(gun)
                        search_data.append(scl)
                        search_data.append(saat)
                saat1 = search_data[2]
                parcalan = saat1.split("\n")
                saat1 = parcalan[0]
                parca = saat1.split(" ")
                saat1 = parca[1]


                try:
                    saat2 = search_data[5]
                    parcalan = saat2.split("\n")
                    saat2 = parcalan[0]
                    parca = saat2.split(" ")
                    saat2 = parca[1]
                    saat1 =datetime.strptime(saat1, '%H:%M:%S')
                    saat2 =datetime.strptime(saat2, '%H:%M:%S')
                    harcanan_zaman = saat2-saat1
                    hours = harcanan_zaman.seconds / 3600
                    veri = str(search_data[0]).strip()+"_"+str(search_data[1]).strip()+"_"+str(search_data[2]).strip()+"_"+ str(search_data[5]).strip() + "_" + str(hours).strip() + '\n'
                except Exception as e:
                    print(e)
                    veri = str(search_data[0]).strip()+"_"+str(search_data[1]).strip()+"_"+str(search_data[2]).strip()+str("_---_---").strip()+'\n'
                
                with open("yedek.txt", "a") as f:
                    f.write(veri)
                f.close()
                

            #buradan sonra excel işlemleri

            f = open("yedek.txt", "r")
            guns = []
            persons = []
            strt_times = []
            stp_tmes =[]
            past_tmes = []
            for i in f:
                print(i)
                try:
                    splttt = i.split("_")
                    day = splttt[0]
                    guns.append(day)

                    persnn = splttt[1]
                    persons.append(persnn)

                    startt_time = splttt[2]
                    strt_times.append(startt_time)

                    stop_time = splttt[3]
                    stp_tmes.append(stop_time)

                    past_time = splttt[4]
                    past_tmes.append(past_time)

                except Exception as e:
                    print(e)
            f.close()

            #
            os.remove('yedek.txt')


            workbook = xlsxwriter.Workbook(f"mesai_takip_{tarih_str}.xlsx")
            worksheet = workbook.add_worksheet()
            row = 0
            gunnnn = 0
            calisan = 1
            baslangic =2
            bitis = 3
            gecensure = 4

            for j in range(len(stp_tmes)):
                g = guns[j]
                person = persons[j]
                strt_time = strt_times[j]
                stp_tme = stp_tmes[j]
                past_tme = past_tmes[j]

                worksheet.write(row, gunnnn, g)
                worksheet.write(row, calisan, person)
                worksheet.write(row, baslangic, strt_time)
                worksheet.write(row, bitis, stp_tme)
                worksheet.write(row, gecensure, past_tme)
                row = row +1
                print("yazildi")
            workbook.close()


    cv2.imshow('Kamera', resim)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

kamera.release()
cv2.destroyAllWindows()
