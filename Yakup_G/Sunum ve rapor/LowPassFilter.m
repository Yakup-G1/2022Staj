clear all

counter=0;
counter2=0
Fs= 1000;
T= 1/Fs;
t=0:T:1-T;
eski_veri=0;
s=0:T:1-T;
mylowpass=0:T:1-T;

for t=0.0:T:1-T;
     
    counter2=counter2+1;
    s(counter2) = sin(2*pi*50*t);
    
    if counter2==0
        eski_veri=0;
    end

    a=0.1;
    eski_veri= eski_veri*(1-a)+a*s(counter2);
    mylowpass(counter2) = eski_veri;
    
end
d = designfilt('lowpassfir','FilterOrder',1,'CutoffFrequency',1,'SampleRate',Fs);

oneOrder= filter(d,s);


d = designfilt('lowpassfir','FilterOrder',5,'CutoffFrequency',11,'SampleRate',Fs);

fiveOrder= filter(d,s);


hold on
plot(s)
plot(mylowpass)
plot(oneOrder)
plot(fiveOrder)

xlim([0 100])
legend('normal veri','1.nd low pass filter','matlab_lowpass','5.derece')