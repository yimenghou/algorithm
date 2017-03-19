function transmitter(packet)

%% Defining constansts

bits = packet;      % Interprate input
fs = 44100; 
fc = 5000;
T = 1/fs;
Bws = 100;
beta = 0.3;
Rs = 2*Bws/(1+beta);
Ts = 1/Rs;


barker = [1 1 1 -1 -1 -1 1 -1 -1 1 -1];                     % Creating barker sequence
b = buffer(bits,2);                                         % Splitting the input and placing even index bits in first row and odd bits in second row 

trigb=[1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0 1 1 0 0];    % Arbitrary sequence used for triggering
trigm = (-2*trigb+1);                                       % Converting 0 and 1 to -1 and 1
trigger = [trigm ; trigm];                                  % Placing trigger sequence in both "real" and "imaginary" column
m2 = (-2*b+1);                                              % Converting information bits from 0 and 1 to -1 and 1

preamble = [barker ; barker];                               % Placing barker in both "real" and "imaginary" column
m  = [trigger preamble  m2];                                % Concatenating preamble and message matrixes
fd = fs/(5*round(Ts/T/5));                                  % Calculating input sampling frequency

num = rcosine(fd,fs,'sqrt',beta);                           % Creating filter characteristics
[st,t2] = rcosflt(m',fd,fs,'filter',num);                   % Perform filtering

c = [sqrt(2).*cos(2*pi*fc.*t2)' sqrt(2).*sin(2*pi*fc.*t2)'];% Up conversion vector
S = st.*c;                                                  % Up conversion

Stot = S(:,1)-S(:,2);                                       % Signal to send

wavplay(Stot,fs)                                            % Sending signal

end