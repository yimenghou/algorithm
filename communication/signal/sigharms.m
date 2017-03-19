function sigharms(specarray, fullcycles, param)
%HARMS HARMS(SPECARRAY, FULLCYCLES, PARAMARRAY)
%   SPECARRAY is a spectrum array
%   FULLCYCLES is the number of full cycles to assume 
%   PARAMARRAY is an array of parameter values to use for the X axis 

% # of spectrum components 
speccomps = size(specarray, 1)  ;

% # of harmonics to plot 
harmcount = 10; 
% pick out indices of harmonics ...
ixarray = (1 == mod((1:speccomps),fullcycles)) ; 
% ... but not DC ...
ixarray(1) = 0;
% ... and only harmcount of them 
ixarray(harmcount*fullcycles+2:end) = 0; 

figure; 

set(gcf, ...
   'DefaultAxesColorOrder', [1 0 0 ; 0 1 0 ; 0 0 1; 0 0 0], ...
   'DefaultAxesLineStyleOrder', '-d|-+|-x|-o') ;

semilogx(param, ...
         10 * log10(specarray(ixarray, :))) ; 
     
legendarray = {} ;
for i = 1:harmcount 
  legendarray = [ legendarray , { ['tone ' int2str(i)] } ] ; 
end 

legend(legendarray) ; 

title(['Harmonics for ' inputname(1) ]) ; 

end

