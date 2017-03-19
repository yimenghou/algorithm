clear all;close all; clc
[X, FS]=audioread('bird.wav'); % read voice
% [X, FS]=audioread('mysentence.wav');
% wavplay(X);
% figure; plot(X);
X = [X ;zeros(4744,1)]; % zero padding after the signal to ensure integer
% figure; plot(X);

num = 20*0.001*FS; % sample number in each block
block = length(X)/num; %block number
xbar = reshape(X,[],block); % buffer 
% figure; plot(xbar(:,10));
xham = zeros(num,block);
for i=1:block
    xham(:,i) = xbar(:,i).*hamming(num); 
end
% figure; plot(xham(:,10));
L=5; % decide how many times of zeros padded
xpad = [xham ; zeros(L*num,block)];
spec = abs(fft(xpad));
ceptrum = abs(ifft(log(spec)));

c = 0.5;
figure; subplot(1,2,1)
for i=1:30
c2 = spec(:,i) + i*c; plot(c2);hold on
end
subplot(1,2,2)
for i=1:30
c2 = ceptrum(:,i) + i*c; plot(c2);hold on
end
