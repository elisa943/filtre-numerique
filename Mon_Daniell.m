function y = Mon_Daniell(x)
    k = 2;
    y = abs(fft(x)).^2;
    N = length(y);
    for i=1:N
        vecteur_moyenne = 0;
        for j=-k:k
            vecteur_moyenne =  vecteur_moyenne + y(mod(i-1+j, N) + 1);
        end
        y(i) = vecteur_moyenne / (2* k + 1);
    end    
    
end