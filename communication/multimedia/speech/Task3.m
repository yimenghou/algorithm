clear all;close all;clc

[X, FS]=audioread('mysentence.wav'); % read voice
% wavplay(X,8000);
% lpc parameters generating
num = 20*0.001*8000; % sample number in each block
block = length(X)/num; %block number
xbar = reshape(X,[],block); % buffer 
[A ,E] = lpc(xbar,10); % lpc parameter estimate

% residual sequence
e= [];
e1 = filter(A(1,:),1,X(1:num)); % the first block do the normal filter
for i=2:block                   % other blocks filter them consider the last 10 samples of the previous block
    e(i,:) =  filter(A(i,:),1,X(1+(i-1)*num-10:i*num));
end
e =e(:,11:end);
e(1,:)= e1;   % put the first and others together
e=e';
ef = reshape(e,1,[]); % the vector of residual sequence
%  k-most
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

ef2 = reshape(e,1,[]); % a vector of residual sequence
% figure; plot(ef);
% title('residual sequence');
% xlabel('time sample');
% ylabel('magnitude');
% print('residual sentence','-dpng', '-r300');
% % 
% figure; subplot(2,1,1),plot(ef(4501:4820));
% title('residual sequence');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(2,1,2),plot(X(4501:4820));
% title('original speech signal');
% xlabel('time sample');
% ylabel('magnitude');
% print('compare2blockrs','-dpng', '-r300');

 % re-synthesize the signal
    shat2 = filter(1,A(1,:),ef2(1:num)); 
for i=2:block
    shatk(i,:) =  filter(1,A(i,:),ef2(1+(i-1)*num-10:i*num));
end
    shatk =shatk(:,11:end);
    shatk(1,:)= shat2;
    shatk = shatk';
shatk = reshape(shatk,1,[]); % vector of re-synthesized signal
figure; plot(shatk);
wavplay(shatk,8000);
% wavwrite(shatk,'re_task3.wav');
% figure; subplot(3,1,1),plot(X);
% title('Original speech signal');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(3,1,2),plot(shatk);
% title('Re-synthesized signal');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(3,1,3),plot(ef2);
% title('Residual sequence');
% xlabel('time sample');
% ylabel('magnitude');
% print('3com_task3','-dpng', '-r320');

% figure; plot(ef2(4501:4820));
%  title('Residual requence Zoom-in(40ms) K=20');
% xlabel('time sample');
% ylabel('magnitude');
% print('rs_zoomin_3','-dpng','-r320');