function a = pente(x, y)
    N = length(y);

    B = y.';
    A = zeros(N, 2);
    A(:, 1) = x;
    A(:, 2) = 1;

    coeff = pinv(A) * B;
    a = coeff(1);
end