%Define bits
clc;clear all;close all;
%Initializing parallel mode 
% pools = matlabpool('size');
% cpus = feature('numCores');
% 
% if pools ~= (cpus - 1)
%     if pools > 0
%         matlabpool('close');
%     end
%     matlabpool('open', cpus);
% end

tic
N = 10^5; % Simulate N bits each transmission ( one block )
maxNumErrs = 500; % Get at least 100 bit errors ( more is better )
maxNum = 1e7; % 1.e7 OR stop if maxNum bits have been simulated
EbN0 = -1:0.5:7; %Power efficiency range
parfor_progress(length (EbN0))
% ======================================================================= %
% Simulation Chain
% ======================================================================= %
BERcodedE1soft = zeros (1, length(EbN0)); % pre - allocate a vector for the BER results
cmpbits=[0 0 1 1 0 1 1 0];
for m = 1:length (EbN0) % use parfor (’ help parfor ’) to parallelize
    totErr = 0; % running number of errors observed
    num = 0; % running number of bits processed
    c = zeros(1,2*(N+2))'; %Encoded bits
    y = zeros(1,N+2); %Signal with noise
    chat= zeros(1,(N+2)*2); %Received signal after hard decision 
    uhat=zeros(1,(N+2)); %Decoded bits
    currdist=[0 Inf Inf Inf]; %Initializing hamming distance
    states=zeros(4,(N+4)/2); %%Initializing state matrix
    prevdist=zeros(1,8); %Previous hamming distance counter 
    parfor_progress; %Progress bar
    while (( totErr < maxNumErrs ) && ( num < maxNum ))
        % ===================================================================== %
        % Begin processing one block of information
        % ===================================================================== %
        % [SRC] generate N information bits
        uk=[0,0,randi([0 1],1,N),0,0];
        % [ENC] convolutional encoder
        c(1:2:end)=bitxor(bitxor(uk(3:end),uk(2:end-1)),uk(1:end-2));
        c(2:2:end)=bitxor(uk(3:end),uk(1:end-2));
        % [MOD] symbol mapper
        x=((c(1:2:end)*2)-1)+((2*c(2:2:end)*1i)-1i);
        % [CHA] add Gaussian noise
        sigma= sqrt(2*(1./10.^(EbN0(m)./10)));
        n=1/sqrt(2)*sigma*(randn(length(x),1)+1i*randn(length(x),1));        
        y=x+n;      
        for i=1:1:N+2
            %Comparison of hamming distance and received bits
            dh00=(-1-real(y(i)))^2+(-1-imag(y(i)))^2;
            dh11=(1-real(y(i)))^2+(1-imag(y(i)))^2;
            dh01=(-1-real(y(i)))^2+(1-imag(y(i)))^2;
            dh10=(1-real(y(i)))^2+(-1-imag(y(i)))^2;
            %Accumulated hamming distance 
            prevdist(1)=currdist(1)+dh00;
            prevdist(2)=currdist(2)+dh11;            
            prevdist(3)=currdist(3)+dh10;
            prevdist(4)=currdist(4)+dh01;            
            prevdist(5)=currdist(1)+dh11;
            prevdist(6)=currdist(2)+dh00;            
            prevdist(7)=currdist(3)+dh01;
            prevdist(8)=currdist(4)+dh10;
            %Select minimum hamming distance
            if(prevdist(1)>prevdist(2))
                currdist(1)=prevdist(2);
                states(1,i)=2;
            else
                currdist(1)=prevdist(1);
                states(1,i)=1;
            end
            if(prevdist(3)>prevdist(4))
                currdist(2)=prevdist(4);
                states(2,i)=4;
            else
                currdist(2)=prevdist(3);
                states(2,i)=3;
            end
            if(prevdist(5)>prevdist(6))
                currdist(3)=prevdist(6);
                states(3,i)=2;
            else
                currdist(3)=prevdist(5);
                states(3,i)=1;
            end
            if(prevdist(7)>prevdist(8))
                currdist(4)=prevdist(8);
                states(4,i)=4;
            else
                currdist(4)=prevdist(7);
                states(4,i)=3;
            end
        end
        %Find the survivor path
        currentstate=1;
        for kk=N+2:-1:1
            if currentstate==1
                uhat(kk)=0;
                currentstate=states(1,kk);
            elseif currentstate==2
                uhat(kk)=0;
                currentstate=states(2,kk);
            elseif currentstate==3
                uhat(kk)=1;
                currentstate=states(3,kk);
            elseif currentstate==4
                uhat(kk)=1;
                currentstate=states(4,kk);
            end     
        end
        % ===================================================================== %
        % End processing one block of information
        % ===================================================================== %
        %Calculate bit error
        BitErrs=sum(bitxor(uhat(1:end-2),uk(3:end-2)));
        totErr = totErr + BitErrs ;
        num = num + N;
        disp ([ '+++ ',num2str(totErr),'/',num2str(maxNumErrs),' errors . '...
            num2str(num),'/',num2str(maxNum),' bits . Projected error rate = '...
            ,num2str(totErr/num),'%10.1 e. +++']);
    end
    BERcodedE1soft(m) = totErr/num;
end
parfor_progress(0);
disp(['Time: ',num2str(toc/60),'min'])
semilogy(EbN0,BERcodedE1soft,'r-x')
grid on
ylim([1e-5 1])
xlim([-1 10])
ylabel('BER')
xlabel('E_b/N_0[dB]')
legend()
hold on
clearvars -except BERcodedE1soft
save('BERForPlotsE1soft')

% save('BERForPlotsE1')
% ======================================================================= %
% End
% ======================================================================= %