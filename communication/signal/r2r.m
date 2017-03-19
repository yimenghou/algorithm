function [out] = r2r(n, varargin)
% this function generates a level lookup table for an n-bit R2R ladder, 
% using 1-ohm resistors with a standard deviation of sigma; 
% the 2r resistors consist of two series-conencted 1-ohm resistors, 
% each with a std dev of sigma, so the total std dev of a 2r
% resistor is sqrt(2) sigma 

if (nargin == 1) 
    sigma = 0; 
elseif (nargin == 2) 
    sigma = varargin{1}; 
else 
    error('too many arguments'); 
end

% calculate bit weights f(i), where i is the bit number.
% starting from the least significant bit, 
% iterate over the nodes in the ladder; 
% in each branching point, 
% compute the currentsgoing to all the lesser bits 
% and the current going into this bit 

% need to initialize f
f(1) = 0; 

% "lesser" is the combined resistance of the branches of the lesser
% significant bits; start with only one resistance 
lesser = 2 + sigma * (randn + randn) ; 

for i = 1:n 
  % resistor for this bit branch 
  this2r = 2 + (sigma) * (randn + randn) ; 
  % split current beween lesser bits and this branch 
  f = f * (this2r / (this2r + lesser)) ; 
  f(i) = lesser / (this2r + lesser) ; 
  % compute new value for lesser 
  lesser = (1 + (sigma) * randn) + 1 / ((1 / this2r) + (1 / lesser)) ; 
end

% now, populate the output table
% create a temporary table dval containing the digital values
dval = (1:2^n) - 1 ; 
out = zeros(size(dval)); 

% add bit current value at those positions where bit would be set 
for i = 1:n 
  tmp = mod(dval, 2) ; 
  out = out + tmp * f(i) ; 
  dval = (dval - tmp) / 2 ; 
end 

% stretch final values across the range -1:1  
out = out + linspace(-1-out(1), 1-out(end), length(out)) ;
