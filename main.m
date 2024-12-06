%% Préparation du code
clear; close all; clc;

% Variable

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

% Corrélogramme 
y = Mon_correlogramme(nl);
figure; 
hold on;
plot(0:N-1, spectre_puiss);
plot(y);
plot(0:N-1, densite_spect); 
legend("Spectre de puissance", "Corrélogramme", "Densité spectrale de puissance")
title("Corrélogramme");

%% Chargement
clear; close all; clc;
load data_Weierstrass.mat;
load fcno03fz.mat;

% Bruitage du signal de parole 
RSB = 10; % dB
x = fcno03fz.';
N = length(x);
x_bruite = bruite_signal(x, RSB);
fech = 8000;
time = 0:1/fech:(N-1)/fech;

% Bruitage du signal de Weierstrass
cell = data(1, 1);
s_Weierstrass = cell{1}';
Weierstrass_bruite = bruite_signal(s_Weierstrass, RSB);
N_Weierstrass = length(s_Weierstrass);
time_Weierstrass = 0:1/fech:(N_Weierstrass-1)/fech;

% Affichage du signal de parole avec et sans bruit 
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


% Affichage d'un signal de Weierstrass avec et sans bruit 
figure; 
subplot(2, 1, 1);
plot(time_Weierstrass, s_Weierstrass);
title("Représentation temporelle du signal de Weierstrass");
xlabel("Temps en secondes");
subplot(2, 1, 2);
spectrogram(s_Weierstrass,100,80,100,fech,'yaxis');
xlabel("Temps en secondes");
title("Spectrogramme du signal de Weierstrass");

figure; 
subplot(2, 1, 1);
plot(time_Weierstrass, Weierstrass_bruite);
title("Représentation temporelle du signal de Weierstrass bruité");
xlabel("Temps en secondes");
subplot(2, 1, 2);
spectrogram(Weierstrass_bruite,100,80,100,fech,'yaxis');
xlabel("Temps en secondes");
title("Spectrogramme du signal de Weierstrass bruité");

%% DFA
clear; close all; clc;
load data_Weierstrass.mat;
load fcno03fz.mat;

% Variables

cell = data(5, 1);
x = cell{1}';
M = length(x);
M_x = sum(x) / M; % Moyenne empirique 

p = profil_signal(x, M_x);
puissance_residu = [];
abscisse = 10:3000;

for N_DFA = abscisse
    L = floor(M / N_DFA);
    segments = segmentation(p, N_DFA, L);

    tglob = [];
    for i = 1:L
        tglob = cat(2, tglob, tendance(segments(i, :), i));
    end
    
    residu = p(1:length(tglob)) - tglob; 
    puissance_residu = cat(2, puissance_residu, sum(residu.^2)); % Carré de la fonction de fluctuation
end

% Affichage

figure; 
plot(log(abscisse), log(puissance_residu));
title("Log-log de la fonction de fluctuation");
