function s=segmentation(p,N_DFA,L)
    s=zeros(L,N_DFA);
    for i=0:L-1
        s(i+1,:)=p(i*N_DFA+1:(i+1)*N_DFA);
    end
end