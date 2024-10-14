function y = Mon_Bartlett(x, K)
    N = length(x);
    M = N/K; 
    sous_segments = zeros(K, M);
    for i=0:K-1
        segment = x(i*K + 1:i*K + M);
        sous_segments(i+1, 1:M) = abs(fft(segment)).^2 / M;
    end
    y = zeros(1, K);
    for i=1:K
        y(i) = mean(sous_segments(:, i));
    end
end