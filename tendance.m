function t = tendance(segment, i)
    % Droite de régression des moindres carrés
    % https://www.nagwa.com/fr/explainers/246195683207/#:~:text=La%20droite%20de%20r%C3%A9gression%20des,s'ajuste%20le%20mieux%20ici.
    N_DFA = length(segment); 
    y = segment;
    x = i*N_DFA + 1 : (i+1)*N_DFA; 
    
    b = (sum(y .* x) - (sum(x) * sum(y))/N_DFA) / (sum(x .* x) - sum(x)^2 / N_DFA);
    a = sum(y)/N_DFA - b * sum(x) / N_DFA;

    t = a * x + b; 
end