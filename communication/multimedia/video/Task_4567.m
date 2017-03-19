% lab 3 task 4,5,6,7
clear all;close all;clc
%% load image
I = imread('lena.bmp');
I = mat2gray(I);
figure; imshow(I); title('Original image');
% print('b2_1','-dpng', '-r500');
[N1, N2] = size(I);
M1 = N1/16; % how many blocks in rows
M2 = N2/16; % how many blocks in cols
%% flags (here to change parameters!)
interleaving = 1; % flag: 1 or 0
type = 'noisy'; % 'noisy' or 'packet' or 'none'
t = 70; % how many errors per packet
crate = 0.5; % compression rate (This is fixed in this project)
lostpacketrate = 0.03; % lost packets rate
%% block-based 2D DCT, zigzag scaning and compression
Idct = zeros(N1, N2); % blank image
dctcoef = zeros(256,256);
count = 1;
for i = 1: M1 
    for j = 1:M2
        blk_I = I((i-1)*16+1:i*16,(j-1)*16+1:j*16);
        blk_F = dct2(blk_I); % DCT
        dctcoef(:,count) = zigzag(blk_F); %zigzag scaning
        Idct((i-1)*16+1:i*16,(j-1)*16+1:j*16) = blk_F; 
        count = count+1;
    end
end
compressedct = dctcoef(1:crate*256,:); % compression
signal = reshape(compressedct,[],1);
%% quantization 
level = 255;
step = (max(signal)-min(signal))/level;
codebook = min(signal):step:max(signal);
partition = min(signal)+step/2:step:max(signal)-step/2;
[quantized, ~] = quantiz(signal, partition, codebook);
%% packetization
k = 127; % symbols per packet
packeted = buffer(quantized,k); 
%% RS encoding
m = 8; % Number of bits per RS encoded symbol
n = (2^m)-1; % Codeword length
msgwords = gf(packeted,m)';
codes = rsenc(msgwords,n,k);
rscode = codes.x; 
%% interleaving
[a,b] = size(rscode);
if interleaving
    temp = (reshape(rscode,b,a))';
else
    temp = rscode;
end
    codeinter = gf(temp,m);
 %% channel
switch type
    case 'noisy'
         noise = (1+ randint(size(codeinter,1),n,n)).*randerr(size(codeinter,1),n,t);
         afterchannel = codeinter + noise; % add noise to the code
    case 'packet'
        e_packet = zeros(1,n);
        errorpacket = gf(e_packet,m);        
        index = randi(255,round(a*lostpacketrate),1);
        for i=1:round(a*lostpacketrate)
        codeinter(index(i),:) = errorpacket; % replace the ith codeword by a packet with zero value
        end
        afterchannel = codeinter;
    case 'none'
        afterchannel = codeinter;
end
%% deinterleaving
if interleaving
   afterdeinter = reshape(afterchannel',a,b);
else
   afterdeinter = afterchannel;
end
%% RS decoding
[dec,cnumerr] = rsdec(afterdeinter,n,k);
packets = dec.x;
%% depacketization
afterdepac = reshape(packets',1,[]);
%% dequantisation
afterdequantized = zeros(1,length(afterdepac));
for i=1:length(afterdepac)
    afterdequantized(i) = codebook(afterdepac(i)+1);
end
%% inverse DCT, zigzag scaning and compression
invsignal = buffer(afterdequantized,128);
compressedctinv = [invsignal;zeros(size(invsignal))];
Invi = zeros(N1, N2); 
count = 1;
for i = 1: M1
    for j = 1:M2
        dctcoef1 = invzigzag(compressedctinv(:,count),M1,M2);
        blk_Inv = idct2(dctcoef1);
        Invi((i-1)*16+1:i*16,(j-1)*16+1:j*16) = blk_Inv;
        count = count+1;
    end
end
figure; imshow(Invi); title('Reconstructed image');
% print('b2_2','-dpng', '-r500');
%% image quality evaluation
error = abs(I - Invi);               % Get error values

MSE = 1 / (N1 * N2) * sum(sum(error.^2));   % Compute MSE
PSNR = 10* log10(1/MSE);                  % Compute PSNR

k1 = 0.01;
k2 = 0.03;
L = 1;
c1 = (k1 * L).^2;
c2 = (k2 * L).^2;
SSIM = zeros(M1, M2);

for i = 1:M1
    for j = 1: M2
        blk_I = I((i-1)*16+1:i*16,(j-1)*16+1:j*16);     % Get block from the original image
        blk_Inv = Invi((i-1)*16+1:i*16,(j-1)*16+1:j*16); % Get block from the compressed image
        myu_x = mean(mean(blk_I));                  % Compute means
        myu_y = mean(mean(blk_Inv));
        cov_all = cov(blk_I,blk_Inv);
        sigma_x = cov_all(1,1);       % Compute variances
        sigma_y = cov_all(2,2);     
        sigma_xy = cov_all(1,2); % Compute convariance
        SSIM(i, j) = (2 * myu_x * myu_y + c1) * (2 * sigma_xy + c2) / ((myu_x.^2 + myu_y.^2 + c1) * (sigma_x + sigma_y + c2));    % Compute SSIM
    end
end

MSSIM = 1 / (M1 * M2) * sum(sum(SSIM));             % Compute MSSIM
