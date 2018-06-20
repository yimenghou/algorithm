function [Xhat, psd, const, eyed] = receiver(tout)


tstart = tic;

% Defining Constants

fs = 44100;
fc = 5000;
T = 1/fs;
Bw = 150;
filter_delay = 3;
Bws = 100;
beta = 0.3;
Rs = 2*Bws/(1+beta);
Ts = 1/Rs;
fd = fs/(5*round(Ts/T/5));
Ly = round(fs/fd);                                 
Nfft = 30000;                                      
Nb=128; 

barker = [1 1 1 -1 -1 -1 1 -1 -1 1 -1];             % Barker code for detection



trigb = [1 0 0 1 1 1 0 0 1 1 0 1 0 1 1 1 0 1 1 1];  % Preamble, known to reciever
trigm = (-2*trigb+1);                               % Converting from 0 and 1 to -1 and 1
trigger = [trigm ; trigm];                          % Placing trigger bits in both real and imaginary part
m2 = Nb/2;                      
m=length(trigger)+length(barker)+m2;                % Length of total signal

true = 1;
false = 0;

win_size = 10*round(fs/Rs);                         % Trigger/detection window
sig_size = m*round(fs/Rs);                          % Window to record signal

cont = true;                                        % While loop control


% Filtering barker sequence and putting on carrier frequency

[symbarker,tbark] = rcosflt(barker,fd,fs,'sqrt');       % Putting barker sequence on symbol wave
symbarkeri = symbarker.*sqrt(2).*cos(2*pi*fc.*tbark)';  % Upconverting and creating orthogonal signals
symbarkerq = symbarker.*sqrt(2).*sin(2*pi*fc.*tbark)';

symbarker = symbarkeri+symbarkerq;                      % Total barker, inphase and quad

% Triggering part

while(toc(tstart)< tout && cont == true)
    
    temp = wavrecord(win_size,fs);                      % Record trigger window
    
     
    SIG_Vw = fft(temp,Nfft);                            % FFT of trigger recording
    
    % Computing ratio of recorded trigger around carrier frequency 
    sig = sum(abs(SIG_Vw(round((fc-Bw)/(fs).*Nfft):round((fc+Bw)/(fs).*Nfft))).^2);
    Sigratio = sig./sum(abs(SIG_Vw(1:Nfft/2).^2));
    
    
    if (Sigratio > 0.1)
        
   

        signal = wavrecord(sig_size,fs);                            % Recording data signal
        
        
        cont = false;                                               % Stopping while loop
        
        
        t=([0:length(signal)-1])/fs;                                % Time vector for sine and cosine
        
        Ytot = signal;                                              % Adaption to old code
 
        % Timing synchronization
        
        time_synch = xcorr(Ytot,fliplr(symbarker));                 % Correlate with flipped barker sequence
        [tmp,n_sync] = max(time_synch);                             % Pick out the index of maximum correlation
        trig_delay = n_sync - length(Ytot);                         % Compensating for length increment caused by cross correlation
        
        % Back to base band
        
        yi = Ytot.*sqrt(2).*(cos(2*pi*fc.*t)');                     
        yq = Ytot.*sqrt(2).*(sin(2*pi*fc.*t)');
        
        y = [yi yq];                                                % Stuffing in phase and quadrature parts of signal into the same matrix
        
        [ybis,tbis] = rcosflt(y,fd,fs,'Fs/sqrt');                   % Matched Filtering
        
        
        n_start = (2*filter_delay+length(barker))*Ly+trig_delay;    % Find element corresponding to first data symbol
        Xcorr_samp = round([n_start:Ly:n_start+(m2-1)*Ly]);         % Vector of sampling instants
        sync_samp = round([trig_delay+(2*filter_delay+1)*Ly:Ly:trig_delay+(length(barker)-1+2*filter_delay)*Ly]); % Vector of sampling instants for phase sync
       
       spacer = zeros(size(ybis));                                  % Creating zeros
       ybis = [ybis ; spacer];                                      % Adding the zeros to ybis for the Console does not crash if the index of sampling vector > size(ybis)

        % Sampling recieved signal
        mi = ybis(Xcorr_samp,1);
        mq = ybis(Xcorr_samp,2); 
            
        % Recorded barker sequence
        msync = (ybis(sync_samp,1)+1i*ybis(sync_samp,2));
        
        % Sent barker sequence
        mbarker = barker(2:end)-1i.*barker(2:end);
        
        %Recorded data
        mrec  = (mi + mq.*1i);
        
        dphi = mean(angle(msync([1 2 6 9]))-angle(mbarker([1 2 6 9]))'); % calculating mean angle deviation
        
        mrec = mrec.*exp(1i.*-dphi);                                     % Performing phase compensation
        
        mhati = real(mrec);                             % Creating real and imaginary parts of constellation
        mhatq = imag(mrec);
        
        mhati_norm = mhati/(mean(abs(mhati)));          % Normalizing amplitude of constellation
        mhatq_norm = mhatq/(mean(abs(mhatq)));          
        
        mhat_norm = mhati_norm+1i.*mhatq_norm;          % Putting constellation together in a complex vector
        
        xhat = reshape([mhati < 0  mhatq > 0]',1,Nb);   % Form the bits
         
        %% Generating requested output
        
        % PSD
        [p,f] = pwelch(y,[],[],[],fs,'twosided');
        pdb = 10*log10(p./max(p(1:500)));               % Normalizing and converting to dB
        pdb2=[pdb(end-500:end-1) ; pdb(2:500)];         % Creating centered psd vector
        fneg=-flipud(f(1:500));                         % Creating centered frequency vector
        fsd=[fneg ; f(2:500)];
        
        % Eyevector
        eyevector = ybis(:,1)/mean(abs(ybis(:,1)))-1i.*ybis(:,2)/mean(abs(ybis(:,1))); % Creating normalized vector for use in eye diagram
        eyevector2=((eyevector(n_start:n_start+(m2-1)*Ly)))';

    end
end
if (toc(tstart) < tout)
    Xhat = [xhat]; psd = struct('p',pdb2,'f',fsd);  const=[mhat_norm];  eyed = struct('fsfd',Ly,'r',eyevector2);
else 
    Xhat = []; psd = [];  const=[];  eyed = [];
end

end