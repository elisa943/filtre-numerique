function p=profil_signal(x,M_x)
    N=length(x);
    p=zeros(1,N);
    c=x-M_x;
    for i=1:N
        for j=1:i
            p(i)=p(i)+c(j);
        end
    end
end