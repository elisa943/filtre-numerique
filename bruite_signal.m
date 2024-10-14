function y = bruite_signal(x, RSB)
    N = length(x);
    P_s = sum(x .* x) / N;
    P_b = P_s/ exp(RSB/10);

    b = sqrt(P_b) * rand(1, N);
    y = x + b;
end