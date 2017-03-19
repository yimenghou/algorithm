clear all; clc
[wave1, Fs] = audioread('mysentence.wav');
[wave2, Fs] = audioread('re_task2.wav');
% [wave2, Fs] = audioread('resyn3.wav');
% [wave2, Fs] = audioread('resyn_lowquality_3.wav');

num = 20*0.001*Fs; % sample number in each block
block = length(wave1)/num; %block number
% ave = zeros(1,10);
p = 10; % lpc order


%% original signal
xbar1 = reshape(wave1,[],block); % buffer 
[A1 ,E1] = lpc(xbar1,p); % lpc parameter estimate
%% resynthesized sentence
xbar2 = reshape(wave2,[],block); % buffer 
[A2 ,E2] = lpc(xbar2,p); % lpc parameter estimate
%%
A1 = A1(:,2:end).';
A2 = A2(:,2:end).';

A1 = 1 ./ abs(fft(A1, 256));
A2 = 1 ./ abs(fft(A2, 256));
A11 = reshape(A1,1,[]);
A22 = reshape(A2,1,[]);

% figure; plot(A1(:,10));
% hold on; plot(A2(:,10),'r');
%  title('Power spectral comparsion');
% xlabel('time sample m');
% ylabel('magnitude');
% print('powercom','-dpng','-r320');


d = zeros(1,block);

for i=1:block
    d(i) = sum(10 * log10(abs(A1(:,i) - A2(:,i)) .^ 2));
end
figure; plot(d);
title('LPC spectral distance metric');
xlabel('block vector(750 in total)');
ylabel('distortion');
% print('distortion','-dpng','-r320');
% flt = fir1(10,0.1);
% dflt = filter(flt,1,d);
% ave(j) = sum(d)/length(d); % using a average distortion instead of a curve (too noisy to observe)to describe the quality 
% figure; plot(d);

% hold on; plot([1:10:101],d);
% figure;
% hold on;
% plot(p,ave,'-yo');
 