% lab 3 task 1,2,3
clear all;close all;clc
% signal sourse
t = [0:0.1:10*pi];
signal = sin(t);

%% quantization block_2
level = 255;
step = 2/level;

partition = [-1+step/2:step:1-step/2];
codebook = [-1:step:1];
[quantized, QUANTV] = quantiz(signal, partition, codebook);

%% packetization block_3
k = 127;
packeted = buffer(quantized,k)';

%% RS encoder block_4
m = 8; %bits per symbol
n = 2^m-1; %codeword length and message length
msgwords = gf(packeted, m); %represent data by using a Galois array
codes = rsenc(msgwords,n,k); %perform RS encoder
rscode = codes.x; %extract rows of codewords from the GF array;

%% RS decoder block_9
rsdecode = rsdec(codes,n,k);
% isequal(rsdecode,msgwords) % check if they are equal

%% depacketization block_10
depacketed = reshape(packeted,[],1);

%% dequantization block_11
 unquantizesig = codebook(quantized+1);
 isequal(unquantizesig,signal);
 figure; plot(t,signal,'b',t,unquantizesig,'or');title('Quantized signal and original signal');xlabel('Time sample');ylabel('Magnitude');
%  MSE = abs(signal -unquantizesig); % error signal
%  figure; plot(t,MSE);
 
 
 