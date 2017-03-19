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
BERcodedE3soft = zeros (1, length(EbN0)); % pre - allocate a vector for the BER results
cmpbits=[0 0 1 1 0 1 1 0];
CodeGenerator=[str2num(dec2base(bin2dec('10011'),8)) ...
str2num(dec2base(bin2dec('11011'),8))];
ConstraintLength=5;
trellis = poly2trellis(ConstraintLength,CodeGenerator);
for m = 1:length (EbN0) % use parfor (’ help parfor ’) to parallelize
   totErr = 0; % running number of errors observed
    num = 0; % running number of bits processed
    c = zeros(1,2*(N+4))'; %Encoded bits
    y = zeros(1,N+4); %Signal with noise
    chat= zeros(1,(N+4)*2); %Received signal after hard decision 
    uhat=zeros(1,(N+4)); %Decoded bits
    currdist=[0 Inf Inf Inf Inf Inf Inf Inf Inf Inf Inf Inf ...
        Inf Inf Inf Inf]; %Initializing hamming distance
    states=zeros(16,(N+8)/2); %%Initializing state matrix
    prevdist=zeros(1,32); %Previous hamming distance counter 
    parfor_progress; %Progress bar
    while (( totErr < maxNumErrs ) && ( num < maxNum ))
        % ===================================================================== %
        % Begin processing one block of information
        % ===================================================================== %
        % [SRC] generate N information bits
        uk=[randi([0 1],1,N),0,0,0,0];
        % [ENC] convolutional encoder
        c = convenc(uk,trellis);
        % [MOD] symbol mapper
        x=(((c(1:2:end)*2)-1)+((2*c(2:2:end)*1i)-1i))*1/sqrt(2);
        % [CHA] add Gaussian noise
        sigma= sqrt((1/(2*10.^(EbN0(m)./10))));
        n=sigma*(randn(length(x),1)+1i*randn(length(x),1));        
        y=x+n';      
        for i=1:1:N+4
            %Comparison of hamming distance and received bits
            dh00=(-1-real(y(i)))^2+(-1-imag(y(i)))^2;
            dh11=(1-real(y(i)))^2+(1-imag(y(i)))^2;
            dh01=(-1-real(y(i)))^2+(1-imag(y(i)))^2;
            dh10=(1-real(y(i)))^2+(-1-imag(y(i)))^2;
            %Accumulated hamming distance 
            prevdist(1)=currdist(1)+dh00;
            prevdist(2)=currdist(1)+dh11;            
            prevdist(3)=currdist(2)+dh11;
            prevdist(4)=currdist(2)+dh00;            
            prevdist(5)=currdist(3)+dh11;
            prevdist(6)=currdist(3)+dh00;            
            prevdist(7)=currdist(4)+dh00;
            prevdist(8)=currdist(4)+dh11;            
            prevdist(9)=currdist(5)+dh00;
            prevdist(10)=currdist(5)+dh11;            
            prevdist(11)=currdist(6)+dh11;
            prevdist(12)=currdist(6)+dh00;            
            prevdist(13)=currdist(7)+dh11;
            prevdist(14)=currdist(7)+dh00;            
            prevdist(15)=currdist(8)+dh00;
            prevdist(16)=currdist(8)+dh11;
            prevdist(17)=currdist(9)+dh01;
            prevdist(18)=currdist(9)+dh10;            
            prevdist(19)=currdist(10)+dh10;
            prevdist(20)=currdist(10)+dh01;            
            prevdist(21)=currdist(11)+dh10;
            prevdist(22)=currdist(11)+dh01;            
            prevdist(23)=currdist(12)+dh01;
            prevdist(24)=currdist(12)+dh10; 
            prevdist(25)=currdist(13)+dh01;
            prevdist(26)=currdist(13)+dh10;            
            prevdist(27)=currdist(14)+dh10;
            prevdist(28)=currdist(14)+dh01;            
            prevdist(29)=currdist(15)+dh10;
            prevdist(30)=currdist(15)+dh01;            
            prevdist(31)=currdist(16)+dh01;
            prevdist(32)=currdist(16)+dh10;
            %Select minimum hamming distance            
            if(prevdist(1)<=prevdist(3))
                currdist(1)=prevdist(1);
                states(1,i)=1;
            else
                currdist(1)=prevdist(3);
                states(1,i)=2;
             end
            
            if(prevdist(1)>prevdist(3))
                currdist(1)=prevdist(3);
                states(1,i)=2;
            else
                currdist(1)=prevdist(1);
                states(1,i)=1;
            end
            if(prevdist(5)>prevdist(7))
                currdist(2)=prevdist(7);
                states(2,i)=4;
            else
                currdist(2)=prevdist(5);
                states(2,i)=3;
            end
            if(prevdist(9)>prevdist(11))
                currdist(3)=prevdist(11);
                states(3,i)=6;
            else
                currdist(3)=prevdist(9);
                states(3,i)=5;
            end
            if(prevdist(13)>prevdist(15))
                currdist(4)=prevdist(15);
                states(4,i)=8;
            else
                currdist(4)=prevdist(13);
                states(4,i)=7;
            end
             if(prevdist(17)>prevdist(19))
                currdist(5)=prevdist(19);
                states(5,i)=10;
            else
                currdist(5)=prevdist(17);
                states(5,i)=9;
            end
            if(prevdist(21)>prevdist(23))
                currdist(6)=prevdist(23);
                states(6,i)=12;
            else
                currdist(6)=prevdist(21);
                states(6,i)=11;
            end
            if(prevdist(25)>prevdist(27))
                currdist(7)=prevdist(27);
                states(7,i)=14;
            else
                currdist(7)=prevdist(25);
                states(7,i)=13;
            end
            if(prevdist(29)>prevdist(31))
                currdist(8)=prevdist(31);
                states(8,i)=16;
            else
                currdist(8)=prevdist(29);
                states(8,i)=15;
            end
             if(prevdist(2)>prevdist(4))
                currdist(9)=prevdist(4);
                states(9,i)=2;
            else
                currdist(9)=prevdist(2);
                states(9,i)=1;
            end
            if(prevdist(6)>prevdist(8))
                currdist(10)=prevdist(8);
                states(10,i)=4;
            else
                currdist(10)=prevdist(6);
                states(10,i)=3;
            end
            if(prevdist(10)>prevdist(12))
                currdist(11)=prevdist(12);
                states(11,i)=6;
            else
                currdist(11)=prevdist(10);
                states(11,i)=5;
            end
            if(prevdist(14)>prevdist(16))
                currdist(12)=prevdist(16);
                states(12,i)=8;
            else
                currdist(12)=prevdist(14);
                states(12,i)=7;
            end
             if(prevdist(18)>prevdist(20))
                currdist(13)=prevdist(20);
                states(13,i)=10;
            else
                currdist(13)=prevdist(18);
                states(13,i)=9;
            end
            if(prevdist(22)>prevdist(24))
                currdist(14)=prevdist(24);
                states(14,i)=12;
            else
                currdist(14)=prevdist(22);
                states(14,i)=11;
            end
            if(prevdist(26)>prevdist(28))
                currdist(15)=prevdist(28);
                states(15,i)=14;
            else
                currdist(15)=prevdist(26);
                states(15,i)=13;
            end
            if(prevdist(30)>prevdist(32))
                currdist(16)=prevdist(32);
                states(16,i)=16;
            else
                currdist(16)=prevdist(30);
                states(16,i)=15;
            end
        end
        %Find the survivor path
        currentstate=1;
        for kk=N+4:-1:1            
            if currentstate==1
                uhat(kk)=0;
                currentstate=states(1,kk);
            elseif currentstate==2
                uhat(kk)=0;
                currentstate=states(2,kk);
            elseif currentstate==3
                uhat(kk)=0;
                currentstate=states(3,kk);
            elseif currentstate==4
                uhat(kk)=0;
                currentstate=states(4,kk);
            elseif currentstate==5
                uhat(kk)=0;
                currentstate=states(5,kk);
            elseif currentstate==6
                uhat(kk)=0;
                currentstate=states(6,kk);
            elseif currentstate==7
                uhat(kk)=0;
                currentstate=states(7,kk);
            elseif currentstate==8
                uhat(kk)=0;
                currentstate=states(8,kk);
            elseif currentstate==9
                uhat(kk)=1;
                currentstate=states(9,kk);
            elseif currentstate==10
                uhat(kk)=1;
                currentstate=states(10,kk);
            elseif currentstate==11
                uhat(kk)=1;
                currentstate=states(11,kk);
            elseif currentstate==12
                uhat(kk)=1;
                currentstate=states(12,kk);
            elseif currentstate==13
                uhat(kk)=1;
                currentstate=states(13,kk);
            elseif currentstate==14
                uhat(kk)=1;
                currentstate=states(14,kk);
            elseif currentstate==15
                uhat(kk)=1;
                currentstate=states(15,kk);
            elseif currentstate==16
                uhat(kk)=1;
                currentstate=states(16,kk);          
            end
        end
        % ===================================================================== %
        % End processing one block of information
        % ===================================================================== %
        %Calculate bit error
        BitErrs=sum(bitxor(uhat(1:end-4),uk(1:end-4)));
        totErr = totErr + BitErrs ;
        num = num + N;
        disp ([ '+++ ',num2str(totErr),'/',num2str(maxNumErrs),' errors . '...
            num2str(num),'/',num2str(maxNum),' bits . Projected error rate = '...
            ,num2str(totErr/num),'%10.1 e. +++']);
    end
    BERcodedE3soft(m) = totErr/num;
end

parfor_progress(0);
disp(['Time: ',num2str(toc/60),'min'])
semilogy(EbN0,BERcodedE3soft,'r-x')
grid on
ylim([1e-5 1])
xlim([-1 10])
ylabel('BER')
xlabel('E_b/N_0[dB]')
legend()
hold on
clearvars -except BERcodedE3soft
save('BERForPlotsE3soft')
%Asymptotic coding gain
% Rc=1/2;
%dmin=
% Gcasym=10*log(Rc*dmin)
%Reliable communication
% Capacity
% Cd=W*log2(1+P/N0*W)
% Spectral efficiency
% r=Rb/W;
% ======================================================================= %
% End
% ======================================================================= %