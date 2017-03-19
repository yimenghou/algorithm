%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%                          Lab 2 Task 1                                   %
%                  DCT - based Image Compression                          %
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Step 1.1
clear all; close all; clc
video = aviread('Trees1.avi');   %% read avi video
%%movie(video);                   %% play the movie
length(video);                  %% total number of frames
%%if (length(video) > 2)
    I1 = frame2im(video(1));    %% extract the first frame in to image I1
    I2 = frame2im(video(2));    %% extract the second frame in to image I2
%%end
if(ndims(I1)>2)
    J1 = rgb2gray(I1);          %% convert an rgb image to a gray-scale
    J2 = rgb2gray(I2);          %% convert an rgb image to a gray-scale
end

imwrite(J1, 'frame1.bmp');        %% saved J1 the image in disk
imwrite(J2, 'frame2.bmp');        %% saved J2 the image in disk

figure;
imshow(J1); title('Original frame')

%% Step 1.2

I = imread('frame1');
I = mat2gray(I);
F = dct2(I);                   %% apply the 2D DCT to the image 

figure; 
imshow(F); title ('2D-DCT domain of frame 1');

%% Step 1.3

[N1 N2] = size(F);
shaped = abs(reshape(F, 1, N1 * N2));
sorted = sort(shaped);
th = sorted(round(0.9 * N1 * N2));  
F(abs(F) < th) = 0;

%% Step 1.4
Inv = idct2(F);                     % Inverse DCT
% Normalization
% Inv = Inv + abs(min(min(Inv)));
% Inv = Inv / max(max(Inv));
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

for i = 1: M1
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
figure;                             % Error image
imagesc(error * 30);
colormap('gray');
axis off;
title('Error image');

figure;                             % Compressed image
imagesc(Inv);
colormap('gray');
axis off;
title('Whole image compression')
