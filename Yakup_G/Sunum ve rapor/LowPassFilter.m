clear all

Fs= 100;
T= 1/Fs;
t=0:T:1-T;

s=sin(2*pi*10*t);

noise= 0.5*randn(size(t));
signal= s+noise;


d = designfilt('lowpassfir','FilterOrder',10,'CutoffFrequency',11,'SampleRate',Fs);

fiveOrder= filter(d,signal);


d = designfilt('lowpassfir','L',1,'CutoffFrequency',11,'SampleRate',Fs);

oneOrder= filter(d,signal);

hold on
plot(signal)
plot(oneOrder)
plot(fiveOrder)

xlim([0 40])
legend('normal veri','1.nd low pass filter','5.nd low pass flter')