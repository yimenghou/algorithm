%% inter-frame compression
clear all; close all;clc

% video = aviread('trees1.avi');
% % % movie(video);
% frames = length(video); 
% frame1 = frame2im(video(10));
% frame2 = frame2im(video(11));
% % 
% frame1 = rgb2gray(frame1);
% frame2 = rgb2gray(frame2);
% 
% imwrite(frame1,'frame1.bmp');
% imwrite(frame2,'frame2.bmp');      
%% find motion block
frame1 = imread('frameintra1.bmp'); % load 2 consecutive frames
frame2 = imread('frameintra2.bmp');
% frameoriginal = imread('frame2.bmp');
% figure;imshow(frame1);
% figure;imshow(frame2);
frame1 = mat2gray(frame1); % convert them into grayscale image
frame2 = mat2gray(frame2);
% frameoriginal = mat2gray(frameoriginal);
frame1 = frame1(1:end-1,1:end-1);  % initial images
frame2 = frame2(1:end-1,1:end-1);
% frameoriginal = frameoriginal(1:end-1,1:end-1);

% figure; imshow(frame1);
% title('Old image');
% figure; imshow(frame2);
% title('New image');

[aa,bb] = size(frame1);
framecom = frame1;
th = 50/255; % threshold

Idiff = frame2 - frame1; % error image
% figure; imshow(Idiff);
% title('Difference image');
% print('4_3','-dpng', '-r500');

for i=1:length(Idiff(:))   
if abs(Idiff(i)) < th
    Idiff(i) = 0;
end
end

a = 16*ones(1,15); 
b = 16*ones(1,20);
block = mat2cell(Idiff,a,b);  % use cell to represent block
block1 = mat2cell(frame1,a,b);
block2 = mat2cell(frame2,a,b);
imblock = zeros(15,20);

for i=1:length(a)*length(b) % identify motion blocks
    temp = block{i};
    if isempty (find(temp ~= 0))
        imblock(i) = 0; % unmotioned block(black)
    else
        imblock(i) = 1; % motion block(white)
    end        
end
motionblkratio = length(find(imblock ==1))/length(imblock(:));


imblockkk = kron(imblock,ones(16,16)); % enlarged motion block image
figure; imshow(imblockkk);
title('Motion image Th = 50/255');
% print('4_4','-dpng', '-r500');

%% motion compensation

[c,d] = find(imblock == 1);
table = 16*([c d]-1)+1;
motionblock = find(imblock == 1);
MAE = zeros(225,305);
MV = cat(3,zeros(15,20),zeros(15,20)); % motion vector(3D matrix)

for i=1:length(motionblock)
    temp = block2{motionblock(i)};
    for j=1:225 % make pixel-wised searching
        for k=1:305
            MAE(j,k) = sum(sum(abs(frame1(j:j+15,k:k+15) - temp)))/(16*16);
        end
    end
    [x,y] = find(MAE ==min(min((MAE)))); % coordinates of the top-left pixel of the best block
    x = x(1); y = y(1);% if there are more result, just randomly take one
      MV(c(i),d(i),1) = x-table(i,1);
      MV(c(i),d(i),2) = y-table(i,2);
    framecom(table(i,1):table(i,1)+15,table(i,2):table(i,2)+15) = frame1(x:x+15,y:y+15);
end

figure;
imshow(framecom); title('image after motion compensation')%compensated image
% subplot(1,2,1),imshow(frame2); 
% title('original frame2');
% subplot(1,2,2),imshow(framecom);
% title('compensated frame2');

%% quality evaluation

[N1, N2] = size(frame1);
M1 = round(N1 / 8);                 
M2 = round(N2 / 8);
error = abs(frame2 - framecom);               % Get error values

MSE = 1 / (N1 * N2) * sum(sum(error.^2));   % Compute MSE
PSNR = 10* log10(1/MSE);                  % Compute PSNR

k1 = 0.01;                          % Initial values
k2 = 0.03;
L = 1;
c1 = (k1 * L).^2;
c2 = (k2 * L).^2;
SSIM = zeros(M1, M2);

for i = 1:M1
    for j = 1: M2
        blk_I = frame2((i-1)*8+1:i*8,(j-1)*8+1:j*8);     % Get block from the original image
        blk_Inv = framecom((i-1)*8+1:i*8,(j-1)*8+1:j*8); % Get block from the compressed image
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

% figure;
% subplot(2,2,1),imshow(frame1);title('Old image');
% subplot(2,2,2),imshow(frame2);title('New image');
% subplot(2,2,3),imshow(Idiff);title('Difference image');
% subplot(2,2,4),imshow(imblockkk);title('Motion image Th = 80/255');
% print('4_com80','-dpng', '-r500');

% figure;
% subplot(2,2,1),imshow(frameoriginal);title('Original image');
% subplot(2,2,2),imshow(frame2);title('After intra-frame process');
% subplot(2,2,3),imshow(framecom);title('After inter and intra frame process');
% subplot(2,2,4),imshow(30*error); title('Error image');
% print('intrainter','-dpng', '-r500');
