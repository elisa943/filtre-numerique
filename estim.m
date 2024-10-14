function corr=estim(x,N,biai)
    corr=zeros(1,N);
    for m=1:N
        for j=1:N-m-1
            if j+m<=N
                corr(m)=corr(m)+x(j+m)*x(j);
            else
                corr(m)=corr(m);
            end
        end
        if biai=="non biaise"
            corr(m)=corr(m)/(N-m);
        elseif biai=="biaise"
            corr(m)=corr(m)/N;
        end
    end
end