%% Préparation du code
clear; close all; clc;

%% Variable

%Bruit
sigma=3;
N=2^15;
K=2^8;
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

Bartlett=Mon_Bartlett(nl,N/K);
Welch=Mon_Welch(nl,1000,8);
spectre_puiss=(abs(fft(nl)).^2)/N;
densite_spect=(sigma^2)*ones(1,N);
M_sp=mean(spectre_puiss);
Daniell = Mon_Daniell(nl);
figure
hold on;
plot(0:N-1,spectre_puiss)
plot(0:N/K:N-1,Bartlett)
plot(0:N-1,densite_spect)
legend("Spectre de puissance","Densité spectrale de puissance","Périodogramme de Bartlett");
title("Comparaison avec le Périodogramme de Bartlett");

figure; 
hold on;
plot(0:N-1, spectre_puiss);
M_daniell=mean(Daniell/N);
plot(Daniell/N);
plot(0:N-1, densite_spect); 
legend("Densité spectrale de puissance", "Spectre de puissance", "Périodogramme de Daniell");
title("Comparaison avec le Périodogramme de Daniell");

%% Chargement
clear; close all; clc;
load data_Weierstrass.mat;
load fcno03fz.mat;

% Bruitage du signal de parole 
RSB = 5; % dB
x = fcno03fz.';
N = length(x);
x_bruite = bruite_signal(x, RSB);
fech = 8000;
time = 0:1/fech:(N-1)/fech;
% sound(x, fech);
% sound(x_bruite,fech);

figure; 
subplot(2, 1, 1);
plot(time, x);
title("Représentation temporelle du signal de parole");
xlabel("Temps en secondes");
subplot(2, 1, 2);
spectrogram(x,100,80,100,fech,'yaxis');
xlabel("Temps en secondes");
title("Spectrogramme du signal de parole");

figure; 
subplot(2, 1, 1);
plot(time, x_bruite);
title("Représentation temporelle du signal de parole bruité");
xlabel("Temps en secondes");
subplot(2, 1, 2);
spectrogram(x_bruite,100,80,100,fech,'yaxis');
xlabel("Temps en secondes");
title("Spectrogramme du signal de parole bruité");

%% DFA
clear; close all; clc;
load data_Weierstrass.mat;
load fcno03fz.mat;

% Variable
x=fcno03fz.';
M=length(x);
M_x=sum(x)/M;
p=profil_signal(x,M_x);
N_DFA=1000;
L=floor(M/N_DFA);
segments=segmentation(p,N_DFA,L);








