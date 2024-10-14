function y = Mon_Welch(x, NFFT, Fe)
    N_ech = length(x);
    f = -Fe/2:Fe/NFFT:Fe/2-Fe/NFFT;
    th=0.25*(sinc(f/2).*sin(pi*f/2)).^2;
    th((NFFT/2)+1)=th((NFFT/2)+1)+0.25;
    nb_segments = floor(N_ech/NFFT);
    y = zeros(1, NFFT);
    segments = zeros(nb_segments, NFFT);

    for i=0:nb_segments-1
        for j=1:NFFT
            segments(i+1, j) = x(i * NFFT + j);
        end
    end

    for i=1:nb_segments
        y = y + abs(fft(segments(i, :))).^2;
    end
    
    y = y/nb_segments;

    % Affichage de la densité spectrale
    figure; 
    semilogy(f, fftshift(y));
    hold;
    semilogy(f, NFFT*Fe*th);
    grid;
    title("Comparaison densité spectrale (Méthode de Welch/Théorie)");
    xlabel("Fréquence en Hz"); ylabel("Puissance en dB");
    legend('Densité spectrale par Welch',"Densité spectrale théorique");
    ylim([0.000001 25000])
end