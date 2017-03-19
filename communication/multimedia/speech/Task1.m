clear all;
%
% fs=8000;
p=10; % filter order
% X= wavrecord(p*fs,fs,1);
% wavwrite(X,'myvowel.wav');
[X, FS]=audioread('myvowel.wav');
% wavplay(X,8000);

% figure; plot(X);
% title('speech signal recorded of vowel e ');
% xlabel('time sample');
% ylabel('magnitude');
% print('vowel','-dpng', '-r300');

% Xcut=X(10001:12400); % select only one frame
block = 100;
Xbuf = reshape(X,[],block);

% figure; plot(Xcut);
[A ,E] = lpc(Xbuf,p);
e = [];
for i=1:block
    e(:,i) =  filter(A(i,:),1,Xbuf(:,i)); % all-pole filter
end
% e = e(11:end);

% figure; subplot(2,1,1),plot(e);
% title('residual sequence of 300ms frame');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(2,1,2),plot(Xcut);
% title('speech signal of 300ms frame');
% xlabel('time sample');
% ylabel('magnitude');
% print('300msrsandss','-dpng', '-r300');

for i=1:block
shat(:,i) = filter(1,A(i,:),e(:,i)); % all-zero filter
end
s = reshape(shat,1,[]);
resig = audioplayer(s,8000); % re-synthesized signal
play(resig);
% wavwrite(shat,'re_task1.wav');

% figure; subplot(2,1,1),plot(shat);
% title('Re-synthesized signal');
% xlabel('time sample');
% ylabel('magnitude');
% subplot(2,1,2),plot(Xcut);
% title('Original signal');
% xlabel('time sample');
% ylabel('magnitude');
% print('oriandre','-dpng', '-r300');