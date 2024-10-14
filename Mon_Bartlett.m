function y = Mon_Bartlett(x, K)
    N = length(x);
    M = N/K; 
    sous_segment = zeros(K, M);
    for i=0:K-1
        sous_segment = x(i*K + 1:i*K + M);
        sous_segment(i+1, 1:M) = abs(fft(sous_segment)).^2 / M;
    end
    y = zeros(1, K);
    for i=1:K
        y(i) = mean(sous_segment(:, i));
    end
end