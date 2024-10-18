function y = Mon_correlogramme(x)
    % https://stm.cairn.info/signaux-et-systemes--9782746248595-page-315?lang=fr 
    y = xcorr(x, "biased");    

    % Fenêtrage 
    N = length(y);
    y = y(ceil(N/4):floor(3*N/4));
    y = abs(fft(y));
end