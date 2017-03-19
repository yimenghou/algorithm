clear all;clc; close all
% % 
% fs=8000;
p=10;
% X= wavrecord(p*fs,fs,1);
% wavwrite(X,'mysentence.wav');
[X, FS]=audioread('mysentence.wav'); % read voice
figure; plot(X);
% title('natural speech sentence');
% xlabel('time sample');
% ylabel('magnitude');
% print('sentence','-dpng', '-r300');
% wavplay(X);


num = 20*0.001*8000; % sample number in each block
block = length(X)/num; %block number
xbar = reshape(X,[],block); % buffer 
[A ,E] = lpc(xbar,p); % lpc parameter estimate

e= [];
e1 = filter(A(1,:),1,X(1:num)); % the first block do the normal filtering
for i=2:block                   % other blocks filter them consider the last 10 samples of the previous block
    e(i,:) =  filter(A(i,:),1,X(1+(i-1)*num-10:i*num));
end
e =e(:,11:end);
e(1,:)= e1;   % put the first and others together
e=e';
ef = reshape(e,1,[]);

dsamplerate = 4; %downsample rate
e = downsample(e,dsamplerate);
% wavup1 = upsample(wavdown1,dsamplerate);
% figure; plot(wavdown1);
% figure; plot(wavup1);
% eff = xcorr(ef);
% figure; plot(ef);
% title('residual sequence');
% xlabel('time sample');
% ylabel('magnitude');
% print('residual sentence','-dpng', '-r300');
% 
% figure; subplot(2,1,1),plot(ef(10001:10320));
% title('residual sequence');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(2,1,2),plot(X(10001:10320));
% title('original speech signal');
% xlabel('time sample');
% ylabel('magnitude');
% print('compare','-dpng', '-r300');
%% task 2 speech re-synthesize
%     shat1 = filter(1,A(1,:),ef(1:num));          % re-synthesize the signal
% for i=2:block
%     shat(i,:) =  filter(1,A(i,:),ef(1+(i-1)*num-10:i*num));
% end
%     shat =shat(:,11:end);
%     shat(1,:)= shat1;
%     shat = shat';
% shat = reshape(shat,1,[]);
% figure; plot(shat);
% wavplay(shat,8000);
num = num/dsamplerate;
%% task 3 k-most
K=20;
et = abs(e);
emost = sort(et); %sorting and find the 20 largest number
emost = emost(end-19:end,:); % select out these number
for j=1:block
    for i=1:num
    if abs(e(i,j)) < min(emost(:,j)) % compare all numbers within a colunm with the smallest number in emost
        e(i,j) = 0;
    end
    end
end

ef2 = reshape(e,1,[]);
% figure; plot(ef2);

    shat2 = filter(1,A(1,:),ef2(1:num));  % re-synthesize the signal
for i=2:block
    shatk(i,:) =  filter(1,A(i,:),ef2(1+(i-1)*num-10:i*num));
end
    shatk =shatk(:,11:end);

    shatk(1,:)= shat2;
    shatk = shatk';
shatk = reshape(shatk,1,[]);
figure; plot(shatk);


shatk = upsample(shatk,dsamplerate);
figure; plot(shatk);
wavwrite(shatk,'resyn_lowquality_3.wav')
% wavplay(shatk,8000);




