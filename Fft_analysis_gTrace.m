close all
% L=L_exp;
L=L-mean(L);
figure(1); plot(L)

%% FFT analysis
L_zm = L-mean(L);
Y = fft(L_zm);
tL = length(L_zm/2);
A2 = abs(Y/tL);% amplitude
P2 = A2.^2;% power
A1 = A2(1:tL/2+1);
P1 = P2(1:tL/2+1);
P1(2:end-1) = 2*P1(2:end-1);

Fs = 1200;
f = Fs*(0:(tL/2))/tL;
figure(2); plot(f, A1) 
title("Single-Sided Amplitude Spectrum of X(t)")
xlabel("f (per generation)")
ylabel("|P1(f)|")

background = mean(P1(end-1000:end));
power_sum = cumsum(P1(2:end)-background);
power_sum_norm = power_sum./max(power_sum);

figure(3); plot(f(2:end), power_sum_norm)
xline(10);
yline(0.95)
xline(44);
yline(0.99)
xlabel("f (per generation)")
ylabel("cum-power(f)")

%% reconstructing the signal
close all
rec_L  = ifft(Y);
l_recL= lowpass(rec_L,0.1,Fs);
h_recL= highpass(rec_L,44,Fs);

b_recL= bandpass(rec_L,[1 2],Fs);
figure(4); plot(rec_L,'+k'); hold on
plot(l_recL,'r')
plot(h_recL,'m')
plot(b_recL,'b')
%% lowpass
figure()
lowpass(L_zm,44,Fs, "ImpulseResponse","iir")
%% bandpass
bandpass(L_zm,[1 2],Fs)
%% highpass
highpass(L_zm,44,Fs, "ImpulseResponse","iir")