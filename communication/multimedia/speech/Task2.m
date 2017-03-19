clear all;close all;clc

[X, FS]=audioread('mysentence.wav'); % read voice
% figure; plot(X);
% title('natural speech sentence');
% xlabel('time sample');
% ylabel('magnitude');

% wavplay(X,8000);
% lpc parameters generating
num = 20*0.001*8000; % sample number in each block
block = length(X)/num; %block number
xbar = reshape(X,[],block); % buffer 
p = 120; %filter order
[A ,E] = lpc(xbar,p); % lpc parameter estimate

e= [];
e1 = filter(A(1,:),1,X(1:num)); % the first block do the normal filter
for i=2:block                   % other blocks filter them consider the last 10 samples of the previous block
    e(i,:) =  filter(A(i,:),1,X(1+(i-1)*num-10:i*num));
end
e =e(:,11:end);
e(1,:)= e1;   % put the first and others together
e=e';
ef = reshape(e,1,[]); % a vector of residual sequence

%% re-synthesize the speech
    shat1 = filter(1,A(1,:),ef(1:num));
for i=2:block
    shat(i,:) =  filter(1,A(i,:),ef(1+(i-1)*num-10:i*num));
end
    shat =shat(:,11:end);
    shat(1,:)= shat1;
    shat = shat';
shat = reshape(shat,1,[]); % a vector of re-synthesized signal
% figure; plot(shat);
sound = audioplayer(shat,8000);
play(sound);

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

% figure; subplot(3,1,1),plot(X);
% title('Original speech signal');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(3,1,2),plot(shat);
% title('Re-synthesized signal');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(3,1,3),plot(ef);
% title('Residual sequence');
% xlabel('time sample');
% ylabel('magnitude');
% print('3com_task2','-dpng', '-r320');

% figure; plot(ef(4501:4820));
%  title('Residual requence Zoom-in(40ms)');
% xlabel('time sample');
% ylabel('magnitude');
% print('rs_zoomin_2','-dpng','-r320');