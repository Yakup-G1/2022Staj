import sys


sys.path.append(r'C:\Users\PC_1589\Desktop\PythonAirCraftSim')
import numpy as np

from chap7.mav_dynamics import mav_dynamics
import parameters.simulation_parameters as SIM
from scipy.signal import butter, lfilter, freqz

class Mod_Anlayici:
    def __init__(self):
        
        self.gravity             = 9.81
        #düzgitme değişkenleri
        self.Heading_eski        = 0.0
        self.Heading_Offsett     = 0.044 #heading ofsetti değeri yükseltiğimizde hassasiyet azalmaktadır
        self.Gps_N_eski          = 0.0
        self.Gps_E_eski          = 0.0
        #daire çizme değişkenleri
        self.Daire_Offsett       = 0.033 #daire ofsett değeri arttığında büyük ölçekli daireler hesaplanamaz
        self.Daire_kazanci       = 170.0 # bu kazanç gerçek dünyadaki lat long degerine göre ayarlanacak
        self.Daire_fark          = 0.0
        self.Daire_fark_offsett  = 0.16  #ters orantı yapabilmek için fark ofsetti gerekiyor tekrar ayarlanack
        self.Daire_farkim        = 0.0
        self.Radius_Of_Turn      = 0.0
        self.Radius_Of_Turn_eski = 0.0
        self.Radius_Of_Turn_Offset = 0.1
        #yükseklik algılama değişkenleri
        self.h_eski              = 0.0   
        self.h_Ofsett            = 0.06
        #hareket algılma değişkeleri
        self.Roll_Maksimum_Aci   = 6
        self.Pitch_Maksimum_Aci  = 3
        self.Yaw_Maksimum_Aci    = 8
        self.Hareketsiz_Aci      = 0 # hareketin olmadığı bu parametreye göre ayarlanmalı
        #LowPassFilter
        self.eskiVeri            = 0
        self.h_Lowpass           = 0
        self.order = 6
        self.fs = 50.0       
        self.cutoff = 3.667 
        mav = mav_dynamics(SIM.ts_simulation)

    def Düz_Gitme(self,Heading):
        
        if self.Heading_Offsett >= abs(Heading - self.Heading_eski):
            print("Düz Rotada İlerliyor")
        else:
            print("Düz Rotadan Çıktı")
         
    def Daire_Cizme(self,Heading,TAS,Roll):# buranın ayarlanması için uçağın max yapabileceği headingi yere göre hızı ve lat long verilereni göre birim dönüşüm gerekli
        
        self.Daire_fark = abs(Heading - self.Heading_eski)
        self.Daire_farkim = self.Daire_fark_offsett - self.Daire_fark
        self.Radius_Of_Turn = (TAS**2) / (self.gravity / np.tan(np.radians(Roll)))
        #self.Radius_Of_Turn_fark = abs(self.Radius_Of_Turn-self.Radius_Of_Turn_eski)
        
        #if self.Daire_Offsett >= self.Daire_fark:
        #    print("Daire Çizmiyor")
        #else:
        #    print(round((self.Daire_farkim*TAS*self.Daire_kazanci),2)," boyutlarında daire çiziyor") 
        #
        if self.Radius_Of_Turn_Offset >= self.Radius_Of_Turn:
            print("Daire Çizmiyor")
        else:
            print("radius:",round((self.Radius_Of_Turn),2)," boyutlarında daire çiziyor") 
           
    def Irtifa_kontrol(self,h):
        
        self.h_Lowpass = self.LowPassFilter(h) #kendi bildiğim birinci derece
        
        if abs(self.h_Lowpass-self.h_eski)>self.h_Ofsett:
            
            if(self.h_Lowpass>self.h_eski):
                print("İrtifa Kazanıyor")
                
            else:
                print("İrtifa Kaybediyor")  
                   
        else:
            print("Sabit İrtifada Devam Ediyor")
            
    def Yön_Takip(self,Heading):
        if Heading<= 22.5 and Heading>= -22.5:  
            print("Kuzeye",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading<= 67.5 and Heading>= 22.5:
            print("KuzeyDoğuya",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading<= 112.5 and Heading>= 67.5:
            print("Doğuya",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading<= 157.5 and Heading>= 112.5:
            print("GüneyDoğuya",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading<=-157.5 or Heading>= 157.5:
            print("Güneye",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading>=-67.5 and Heading<=-22.5:
            print("KuzeyBatıya",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading>= -112.5 and Heading<= -67.5:
            print("Batıya",round((Heading),2),"derece açı ile ilerliyor")
            
        elif Heading>= -157.5 and Heading<= -112.5:
            print("GüneyBatıya",round((Heading),2),"derece açı ile ilerliyor")
            
        else:
            print("Böyle bir heading açısı olamaz kontrol edin!!")
               
    
    def Hareket_Kontrol(self,Roll,Pitch,Yaw):
        if abs(Roll - self.Hareketsiz_Aci)>self.Roll_Maksimum_Aci:
            if Roll > self.Hareketsiz_Aci:
                print("Sağa doğru",round(Roll,2),"Açısı ile yan yatıyor");
            else:
                print("Sola doğru",round(Roll,2),"Açısı ile yan yatıyor");
        else:
            print("Roll'de hareket yapmıyor")
            
        if abs(Pitch - self.Hareketsiz_Aci)>self.Pitch_Maksimum_Aci:
            if Pitch > self.Hareketsiz_Aci:
                print("Yukarı Doğru",round(Pitch,2),"Açısı ile ilerliyor");
            else:
                print("Aşağı Doğru",round(Pitch,2),"Açısı ile ilerliyor");
        else:
            print("Pitch'de hareket yapmıyor")
            
        '''if abs(Yaw - self.Hareketsiz_Aci)>self.Yaw_Maksimum_Aci:
            if Yaw < self.Hareketsiz_Aci:
                print("Sağa doğru",round(Yaw,2),"Açısı ile dönüyor");
            else:
                print("Sola doğru",round(Yaw,2),"Açısı ile dönüyor");
        else:
            print("Yaw'de hareket yapmıyor")'''
    
    def LowPassFilter(self,data):
        
        self.eskiVeri = data*0.1 + self.eskiVeri*0.9
        return self.eskiVeri
        
    def Update_Mod(self,Heading,TAS,h,Roll,Pitch,Yaw):

        self.Düz_Gitme(Heading)
        print("  ")
        self.Daire_Cizme(Heading,TAS,Roll)
        print("  ")
        self.Irtifa_kontrol(h)
        print("  ")
        self.Yön_Takip(Heading)
        print("  ")
        self.Hareket_Kontrol(Roll,Pitch,Yaw)
        print(" ")
        
        self.Radius_Of_Turn_eski=self.Radius_Of_Turn
        self.Heading_eski       = Heading
        self.h_eski             = self.h_Lowpass
        
         
