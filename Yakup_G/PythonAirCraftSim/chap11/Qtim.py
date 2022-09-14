
# importing the required libraries
import sys
sys.path.append(r'C:\Users\PC_1589\Desktop\PythonAirCraftSim')
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
import numpy as np
from PyQt5.QtWidgets import QGridLayout
from chap2.mav_viewer import mav_viewer
from message_types.msg_path import msg_path
path = msg_path()

#Aircraft üzerine yapılan dairelerin parametreleri
path.orbit_center = np.array([[0.0, 0.0, 0.0]]).T   # Çizilecek dairelerin merkezi
path.orbit_radius = 50.0                            # Dairenin çapı
path.orbit_direction = 1                            # Daire yönü: (1==clockwise, -1==counter clockwise)

RadtoDeg = 57.29577951308232 

import sys
import numpy as np
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import pyqtgraph.Vector as Vector

class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.mav_view = mav_viewer()
        self.setGeometry(0,0, 1280, 720)    # Ekran boyut ayarları
        self.show()                         # Ekranı gösterme                            
        
        ### Genel parametreler ###
        self.gravity             = 9.81      
        
        ## Düzgitme Algılamak İçin Değişkenleri ##
        
        self.Heading_eski        = 0.0
        self.Heading_Offsett     = 0.044 # Yolda Oluşacak Sapmaları Büyüklüğü Ayarlamaktadır. Heading Ofsetti Değeri Yükseltiğimizde Hassasiyet Azalmaktadır.
        
        ## Daire Çizme Değişkenleri ##
        
        #self.Daire_Offsett       = 0.033 # Daire Ofsett Değeri Arttığında Büyük Ölçekli Daireler Hesaplanamaz
        #self.Daire_kazanci       = 170.0 # Bu Kazanç Gerçek Dünyadaki lat long degerine göre ayarlanacak
        self.Daire_fark          = 0.0
        self.Daire_fark_offsett  = 0.16  #ters orantı yapabilmek için fark ofsetti gerekiyor tekrar ayarlanack
        self.Daire_farkim        = 0.0
        self.Radius_Of_Turn      = 0.0
        self.Radius_Of_Turn_eski = 0.0
        self.Radius_Of_Turn_fark = 0.0
        self.Radius_Of_Turn_Offset = 0.045
        
        ## Yükseklik Algılama Değişkenleri ##
        
        self.h_eski              = 0.0   
        self.h_Ofsett            = 0.06
        
        ## Hareket Algılma Değişkeleri ## 
        
        self.Roll_Maksimum_Aci   = 8        # Roll'deki Açı Farkı Bu Değere Ulastığında Dönüşü Kabul Et
        self.Pitch_Maksimum_Aci  = 4        # Pitch'deki Açı Farkı Bu Değere Ulastığında Dönüşü Kabul Et
        self.Yaw_Maksimum_Aci    = 8        # Yaw'daki Açı Farkı Bu Değere Ulastığında Dönüşü Kabul Et
        self.Hareketsiz_Aci      = 0        # Roll Pitch Yaw Ekseninde Hareketi Algılamak İçin Merkezi 0 Alındı
        
        ## Alçak Geçiren Filtre Değişkenleri ##
        
        self.eskiVeri            = 0        # Eski Veriyi Sakla
        self.h_Lowpass           = 0        # Alçak Geçiren Filtre Çıkışı
        #self.order               = 6        # Alçak Geçiren Derecesi
        self.fs                  = 50.0     # Alçak Geçiren Çalışma Frekansı 
        self.cutoff              = 3.667    # Kesim Frekansı
    
    def UiComponents(self,state):
       
        ## Radyandan Dereceye Geçiş ##
        Heading = state.psi*RadtoDeg      
        Roll    = state.phi*RadtoDeg    
        Pitch   = state.theta*RadtoDeg  
        
        ## Label Tanımlamaları ##
        
        self.label       = QLabel("Phi(Φ):")
        self.labelNumber = QLabel(str(round(Roll,2)))
           
        self.label1       = QLabel("  Theta(θ):")
        self.labelNumber1 = QLabel(str(round(Pitch,2)))
        
        self.label2       = QLabel("  Psi(Ψ):")
        self.labelNumber2 = QLabel(str(round(Heading,2)))
        
        self.label3       = QLabel("  Alpha(α):")
        self.labelNumber3 = QLabel(str(round(state.alpha*RadtoDeg,2)))
        
        self.label4       = QLabel("  Beta(β):")
        self.labelNumber4 = QLabel(str(round(state.beta*RadtoDeg,2)))
        
        self.label5       = QLabel("  h:")
        self.labelNumber5 = QLabel(str(round(state.h,2)))
        
        self.label6       = QLabel("  Rota:")
        
        self.label7       = QLabel("  Daire:")
        
        self.label8       = QLabel("  Altitude:")
        
        self.label9       = QLabel("  Direction:")
        
        self.label10      = QLabel(" Roll:")
        
        self.label11      = QLabel(" Pitch:")
          
        ## Algoritmaların Çağrıldığı Güncelleme Fonksiyonu ##
        
        self.Update_Mod(Heading,state.Vg,state.h,Roll,Pitch,Heading)
        
        ## Layout Oluşturma ve Labelları Ekleme ##
        
        layout = QGridLayout()
        
        layout.addWidget(self.label, 0, 0)           # 0 satır 0. sütüna label oluştur
        layout.addWidget(self.labelNumber, 0, 1)     # 0 satır 1. sütüna label oluştur
        layout.addWidget(self.label1, 1, 0)          # 1 satır 0. sütüna label oluştur
        layout.addWidget(self.labelNumber1, 1, 1)    # 1 satır 1. sütüna label oluştur
        layout.addWidget(self.label2, 2, 0)
        layout.addWidget(self.labelNumber2, 2, 1)
        
        layout.addWidget(self.label3, 3, 0)
        layout.addWidget(self.labelNumber3, 3, 1)
        layout.addWidget(self.label4, 4, 0)
        layout.addWidget(self.labelNumber4, 4, 1)
        layout.addWidget(self.label5, 5, 0)
        layout.addWidget(self.labelNumber5, 5, 1)
        
        layout.addWidget(self.label6, 6, 0)
        layout.addWidget(self.labelNumber6, 6, 1)
        
        layout.addWidget(self.label7, 7, 0)
        layout.addWidget(self.labelNumber7, 7, 1)
        
        layout.addWidget(self.label8, 8, 0)
        layout.addWidget(self.labelNumber8, 8, 1)
        layout.addWidget(self.label9, 9, 0)
        layout.addWidget(self.labelNumber9, 9, 1)
        
        layout.addWidget(self.label10, 10, 0)
        layout.addWidget(self.labelNumber10, 10, 1)
        layout.addWidget(self.label11, 11, 0)
        layout.addWidget(self.labelNumber11, 11, 1)
        
        ## Labelların Renk Ayarları  ##
        
        self.label.setStyleSheet("QLabel { color : white; }")
        self.label1.setStyleSheet("QLabel { color : white; }")
        self.label2.setStyleSheet("QLabel { color : white; }")
        self.label3.setStyleSheet("QLabel { color : white; }")
        self.label4.setStyleSheet("QLabel { color : white; }")
        self.label5.setStyleSheet("QLabel { color : white; }")
        
        self.label8.setStyleSheet("QLabel { color : white; }")
        self.label9.setStyleSheet("QLabel { color : white; }")
        self.label10.setStyleSheet("QLabel { color : white; }")
        self.label11.setStyleSheet("QLabel { color : white; }")
        
        self.labelNumber.setStyleSheet("QLabel { color : white; }")
        self.labelNumber1.setStyleSheet("QLabel { color : white; }")
        self.labelNumber2.setStyleSheet("QLabel { color : white; }")
        self.labelNumber3.setStyleSheet("QLabel { color : white; }")
        self.labelNumber4.setStyleSheet("QLabel { color : white; }")
        self.labelNumber5.setStyleSheet("QLabel { color : white; }")
        self.labelNumber6.setStyleSheet("QLabel { color : white; }")
        self.labelNumber7.setStyleSheet("QLabel { color : white; }")
        self.labelNumber8.setStyleSheet("QLabel { color : white; }")
        self.labelNumber9.setStyleSheet("QLabel { color : white; }")
        self.labelNumber10.setStyleSheet("QLabel { color : white; }")
        self.labelNumber11.setStyleSheet("QLabel { color : white; }")
               
        layout.addWidget(self.mav_view.window, 0, 2, 13, 13)    # 3 Boyutlu Ortamı 0.Satır ve 2.Sütündan 13.Satır ve 13.Sütüna Kadar Doldur
            
        widget = QWidget()                                      
        widget.setLayout(layout)
        widget.setStyleSheet("background-color: black")         # Widget Arkaplan Renk Ayarı 
        self.setCentralWidget(widget)
 
    ## Ekran Güncelleme ##
    def update(self, state):
      
        self.UiComponents(state)
        self.mav_view.update(path,state)
        
    ## Düz_Gitme Algılama Fonksiyonu ##
    def Düz_Gitme(self,Heading):
        
        if self.Heading_Offsett >= abs(Heading - self.Heading_eski):
            self.labelNumber6 = QLabel("Düz Rotada ")
            self.label6.setStyleSheet("QLabel { background-color : lightgreen; color : white; }");
        else:
            self.labelNumber6 = QLabel("Düz Rotadan Çıktı")
            self.label6.setStyleSheet("QLabel { background-color : red; color : white; }");
            
    ## Daire Çizme Algılama Fonksiyonu ##
    
    def Daire_Cizme(self,Heading,TAS,Roll): 
        
        #self.Daire_fark = abs(Heading - self.Heading_eski)
        #self.Daire_farkim = self.Daire_fark_offsett - self.Daire_fark
        self.Radius_Of_Turn = (TAS**2) / (self.gravity / np.tan(np.radians(Roll)))
        
        if self.Radius_Of_Turn_Offset >= self.Radius_Of_Turn:
            self.labelNumber7 = QLabel("Daire Çizmiyor")
            self.label7.setStyleSheet("QLabel { background-color : lightgreen; color : white; }")
        else:
            radius=str(round((self.Radius_Of_Turn),2))
            stringyaz = "Radius " + radius  
            self.labelNumber7 = QLabel(stringyaz)
            self.label7.setStyleSheet("QLabel { background-color : red; color : white; }")
            
    ## İrtifa Kontrol Algılama Fonksiyonu ##
    def Irtifa_kontrol(self,h):
        
        self.h_Lowpass = self.LowPassFilter(h) 
        
        if abs(self.h_Lowpass-self.h_eski)>self.h_Ofsett:
            
            if(self.h_Lowpass>self.h_eski):
                self.labelNumber8 = QLabel("İrtifa Kazanıyor ")
                self.label8.setStyleSheet("QLabel { background-color : red; color : white; }")
            else:
                self.labelNumber8 = QLabel("İrtifa Kaybediyor ") 
                self.label8.setStyleSheet("QLabel { background-color : red; color : white; }")
        else:
            self.labelNumber8 = QLabel(" İrtifada Sabit")
            
    ## Yön Takip Algılama Fonksiyonu ##
    def Yön_Takip(self,Heading):
        
        if Heading<= 22.5 and Heading>= -22.5:  
            
            stringyaz1 = "N  "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
            
        elif Heading<= 67.5 and Heading>= 22.5:
            
            stringyaz1 = "NW "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
            
        elif Heading<= 112.5 and Heading>= 67.5:
           
            stringyaz1 = "W "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
            
        elif Heading<= 157.5 and Heading>= 112.5:
            
            stringyaz1 = "SW "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
        elif Heading<=-157.5 or Heading>= 157.5:
            
            stringyaz1 = "S "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
        elif Heading>=-67.5 and Heading<=-22.5:
            
            stringyaz1 = "NE "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
        elif Heading>= -112.5 and Heading<= -67.5:
            
            stringyaz1 = "E "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
        elif Heading>= -157.5 and Heading<= -112.5:
        
            stringyaz1 = "SE "+ str(round((Heading),2))+" açışı ile ilerliyor"
            self.labelNumber9 = QLabel(stringyaz1)
        else:
            self.labelNumber9 = QLabel("Böyle bir heading açısı olamaz kontrol edin!!")
            
    ## Hareket Kontrol Algılama Fonksiyonu ##
    def Hareket_Kontrol(self,Roll,Pitch,Yaw):
        
        if abs(Roll - self.Hareketsiz_Aci)>self.Roll_Maksimum_Aci:
            if Roll > self.Hareketsiz_Aci:
                stringyaz2 = "Sağa "+str(round(Roll,2)) + " Açı yapıyor "
                self.labelNumber10 = QLabel(stringyaz2)
            else:  
                stringyaz2 = "Sola "+str(round(Roll,2)) + " Açı yapıyor  "
                self.labelNumber10 = QLabel(stringyaz2)
        else:
            self.labelNumber10 = QLabel("Roll'de hareket yapmıyor     ")
            
        if abs(Pitch - self.Hareketsiz_Aci)>self.Pitch_Maksimum_Aci:
            if Pitch > self.Hareketsiz_Aci:
              
                stringyaz3 = "Yukarı "+str(round(Pitch,2)) + " Açı yapıyor"
                self.labelNumber11 = QLabel(stringyaz3)
            else:
                
                stringyaz3 = "Aşağı "+str(round(Pitch,2)) + " Açı yapıyor"
                self.labelNumber11 = QLabel(stringyaz3)
        else:
            self.labelNumber11 = QLabel("Pitch'de hareket yapmıyor   ")
            
    ## Oluşturulan Algoritmalırın Güncelleme Fonksiyonu ##
    def Update_Mod(self,Heading,TAS,h,Roll,Pitch,Yaw):

        self.Düz_Gitme(Heading)

        self.Daire_Cizme(Heading,TAS,Roll)

        self.Irtifa_kontrol(h)

        self.Yön_Takip(Heading)
  
        self.Hareket_Kontrol(Roll,Pitch,Yaw)

        ## Önceki Değerleri Daha Sonra Kullanmak İçin Kayıt Et ##
        self.Radius_Of_Turn_eski=self.Radius_Of_Turn 
        self.Heading_eski       = Heading
        self.h_eski             = self.h_Lowpass
        
    ## Alçak geçiren filtre ##
    def LowPassFilter(self,data):
        self.eskiVeri = data*0.1 + self.eskiVeri*0.9
        return self.eskiVeri   
