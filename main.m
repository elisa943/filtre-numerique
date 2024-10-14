%% Préparation du code
clear; close all; clc;

%% Chargement
load data_Weierstrass.mat;
load fcno03fz.mat;

%% Bruitage du signal de parole 
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
spectrogram(x);
title("Spectrogramme du signal de parole");

figure; 
subplot(2, 1, 1);
plot(time, x_bruite);
title("Représentation temporelle du signal de parole bruité");
xlabel("Temps en secondes");
subplot(2, 1, 2);
spectrogram(x_bruite);
title("Spectrogramme du signal de parole bruité");


