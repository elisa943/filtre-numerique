function t=tendance(segment)
    N=length(segment);
    x=0:N-1;
    b1=x.'\segment.';
    t=b1*x;
end