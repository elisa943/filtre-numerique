function t = tendance(segment, i)
    % Droite de régression des moindres carrés
    N_DFA = length(segment); 
    y = segment;
    x = (i-1)*N_DFA + 1 : i*N_DFA; 
    
    B = y.';
    A = zeros(N_DFA, 2);
    A(:, 1) = x;
    A(:, 2) = 1;

    coeff = pinv(A) * B;
    a = coeff(1);
    b = coeff(2);

    t = a * x + b; 
end