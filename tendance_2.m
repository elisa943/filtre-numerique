function t = tendance_2(segment, i)
    % Moindres carrés : approximation avec un polynôme du second degré
    % https://lucidar.me/fr/mathematics/least-square-approximation-with-a-second-degree-polynomial/
    N_DFA = length(segment); 
    y = segment;
    x = i*N_DFA + 1 : (i+1)*N_DFA; 
    
    B = y.';
    A = zeros(N_DFA, 3);
    A(:, 1) = x .* x;
    A(:, 2) = x;
    A(:, 3) = 1;

    coeff = pinv(A) * B;
    a = coeff(1);
    b = coeff(2);
    c = coeff(3);
    
    t = a * x .* x + b * x + c; 
end