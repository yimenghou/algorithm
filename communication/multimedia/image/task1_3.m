%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                          Lab 2 Task 1.3                                 %
%                  DCT - based Image Compression                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Step 3.5
clear all;close all;clc;

I = imread('frame1'); % Original image
Inv = imread('I3.bmp'); % Wavelet compressed image
I = mat2gray(I);
Inv = mat2gray(Inv);

[N1, N2] = size(I);
error = abs(I - Inv);               % Get error values

MSE = 1 / (N1 * N2) * sum(sum(error.^2));   % Compute MSE
PSNR = 10* log10(1/MSE);                  % Compute PSNR

M1 = round(N1 / 8);                 % Initial values
M2 = round(N2 / 8);
k1 = 0.01;
k2 = 0.03;
L = 1;
c1 = (k1 * L).^2;
c2 = (k2 * L).^2;
SSIM = zeros(M1, M2);

for i = 1:M1
    for j = 1: M2
        blk_I = I((i-1)*8+1:i*8,(j-1)*8+1:j*8);     % Get block from the original image
        blk_Inv = Inv((i-1)*8+1:i*8,(j-1)*8+1:j*8); % Get block from the compressed image
        myu_x = mean(mean(blk_I));                  % Compute means
        myu_y = mean(mean(blk_Inv));
        cov_all = cov(blk_I, blk_Inv);
        sigma_x = cov_all(1, 1);
        sigma_y = cov_all(2, 2);
        sigma_xy = cov_all(1, 2);
        SSIM(i, j) = (2 * myu_x * myu_y + c1) * (2 * sigma_xy + c2) / ((myu_x.^2 + myu_y.^2 + c1) * (sigma_x + sigma_y + c2));    % Compute SSIM
    end
end

MSSIM = 1 / (M1 * M2) * sum(sum(SSIM));             % Compute MSSIM

%% Plot
figure;
imshow(I);
title('Original image');


figure;                             % Compressed image
imagesc(Inv);
colormap('gray');
axis off;
title('Wavelet compressed image')


figure;                             % Error image
imagesc(error * 30);
colormap('gray');
axis off;
title('Error image');



