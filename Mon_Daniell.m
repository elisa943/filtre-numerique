function y = Mon_Daniell(x)
    N = length(x);
    k = 2;
    y = zeros(1,N);
    for i=1:N
        vecteur_moyenne = 0;
        for j=-k:k
            vecteur_moyenne =  vecteur_moyenne + x(mod(i-1+j, N) + 1);
        end
        y(i) = vecteur_moyenne / (2 * k + 1);
    end    
    y = abs(fft(y)).^2;
end