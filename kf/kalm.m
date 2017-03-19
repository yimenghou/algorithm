close all
x = 0:0.01:9.99; y = [ones(1,499) 1:-0.002:0];
Y = [x;y]; Z = Y + 0.1*randn(size(Y));
 % Default initial covariance
%% parameters setting
P0=100*eye(4);
x0=zeros(4,1);
T=0.001;
A=[1 T 0 0;
   0 1 0 0;
   0 0 1 T;
   0 0 0 1];
C=[1 0 0 0;
   0 0 1 0];
Q=0.002*eye(4);
R=1*eye(2);
%% ploting
n=length(4);
[ Xfilt,P ] = kalmfilt(Z,A,C,Q,R,x0,P0)
figure;
plot(Y(1,:),Y(2,:),'rx'); 
hold on
plot(Xfilt(1,:),Xfilt(3,:),'x');
title('True and estimated position');
legend('true position','estimated position');

figure
plot(Xfilt(2,:),'rx');
hold on
plot(Xfilt(4,:),'yx');
title('Speed ');
legend('speed x','speed y');