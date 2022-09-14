
import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
''' 
bu kütüphane 2. derece alçak geçiren filtre için oluşturulmuştur.
kütüphane 2 temel fonksiyon içermektedir bunlar CoefficientCalculator ve Butterworth fonksiyonlarıdır
CoefficientCalculator fonksiyonun A ve B için coefficient değerleri üretir bu fonksiyonun bir kere çalışması yeterlidir
buradaki CutOffFrekansHZ değeri filtrelemek istenen frekans değerini temsil etmektedir filtrelenecek frekansı buraya girmelisiniz
OrneklemeFrekansHZ değişkeni ise çalışan döngünüzün çalışma frekansını girmeniz içindir örneğin döngünüz bütün fonksiyonları 500 hz
de bir yeniliyorsanız burası 500 olmalıdır. CoefficientCalculator ile A ve B nin coefficientları hesaplandıktan sonra 
Butterworth fonksiyonunda FilterData değeri filtrelemek istediğiniz veriyi girmeniz içindir. filtrelenen veri çıktısı butterworth out olarak çıkmaktadır.

buraki kütüphane henüz bitmemiştir. uygulama üzerine çalışılacaktır.
 
'''

class AlcakgecirenFiltre():
    def __init__(self):
		self.A_LP = np.array([0.0,0.0,0.0])   
		self.B_LP = np.array([0.0,0.0,0.0])   
    	self.ButterworthIn = np.array([0.0,0.0,0.0,0.0])
		self.ButterworthOut=0.0
		self.GenelFrekans=0.0
     
	def CoefficientCalculator(self,CutOffFrekansHZ,OrneklemeFrekansHZ):

		self.GenelFrekans = CutOffFrekansHZ / OrneklemeFrekansHZ
		ita = 1/np.tan(np.pi * self.GenelFrekans)
		q = np.sqrt(2)
		B_Coefficient0 = 1 / (1 + q*ita + ita*ita)
		B_Coefficient1 = 2*B_Coefficient0
		B_Coefficient2 = B_Coefficient0
		A_Coefficient0 = 1;											
		A_Coefficient1 = -2 * (ita * ita - 1.0) * B_Coefficient0
		A_Coefficient2 = (1.0 - q*ita + ita * ita) * B_Coefficient0
		A_LP = np.array([A_Coefficient0, A_Coefficient1,A_Coefficient2])

	def Butterworth(self,FilterData):

		self.ButterworthOut = (self.B_LP[0])*FilterData+(self.B_LP[1])*self.ButterworthIn[0]+(self.B_LP[2])*self.ButterworthIn[1]-(self.A_LP[1])*self.ButterworthIn[2]-(self.A_LP[2])*self.ButterworthIn[3]
		self.ButterworthIn[1] = self.ButterworthIn[0]
		self.ButterworthIn[0] = FilterData
		self.ButterworthIn[3] = self.ButterworthIn[2]
		self.ButterworthIn[2] = self.ButterworthOut
		return self.ButterworthOut
