function splane(z,p)
% Arguments are two vectors: z for zeros, p for poles.  
    plot(real(z), imag(z), 'bo', 'MarkerSize', 12); 
    hold on; 
    plot(real(p), imag(p), 'rx', 'MarkerSize', 12); 

    hival = max(abs(axis)) ; 
    axis([-hival hival -hival hival]) ; 
    plot([0 0], [-hival hival], 'k:') ; 
    plot([-hival hival], [0 0], 'k:') ; 
end 
