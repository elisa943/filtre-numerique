%% Préparation du code
clear; close all; clc;

%% Variable

%Bruit
sigma=3;
N=2^15;
nl = sigma*(randn(1,N));
Nl=xcorr(nl,"biased");
Nl2=xcorr(nl,"unbiased");

corr_biaise=estim(nl,N,"biaise");
corr_nbiaise=estim(nl,N,"non biaise");

corr_biaise=cat(2,flip(corr_biaise),corr_biaise);
corr_nbiaise=cat(2,flip(corr_nbiaise),corr_nbiaise);

figure;
subplot(2,2,1)
scatter(-N:N-1,corr_biaise,"r+")
subtitle("Estimateur biaisé avec notre programme")
ylim([-0.2 0.2])
subplot(2,2,3)
scatter(-N+1:N-1,Nl,"b*")
subtitle("Estimateur biaisé avec xcorr")
ylim([-0.2 0.2])
subplot(2,2,2)
scatter(-N:N-1,corr_nbiaise,"r+")
subtitle("Estimateur non biaisé avec notre programme")
subplot(2,2,4)
scatter(-N+1:N-1,Nl2,"b*")
subtitle("Estimateur non biaisé avec xcorr")

spectre_puiss=(abs(fft(nl)).^2)/N;
densite_spect=(sigma^2)*ones(1,N);
figure
hold on;
plot(0:N-1,spectre_puiss);
plot(0:N-1,densite_spect);


