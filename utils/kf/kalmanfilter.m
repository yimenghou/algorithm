function [ Xfilt,P ] = kalmfilt(Y,A,C,Q,R,x0,P0)

[~,N] = size(Y); % N = number of samples, p = number of "sensors"
n=length(A); % n = system order
Xpred = zeros(n,N+1);% Kalman predicted states
Xfilt = zeros(n,N+1);% Kalman filtered states
% Filter initialization:
% Index 1 means time 0, no measurements
P = P0; 
Xfilt(:,1) = x0;% Initial covariance matrix (uncertainty)
Xpred(:,1) = A*x0; % Prediction of x(1) at time t=0, from (18) in handout
P = A*P*A'+Q;% Uncertainty update, from (19) in handout
for t=2:N+1 
    Xfilt(:,t) = Xpred(:,t-1) + P*C'*inv(C*P*C'+R)*(Y(:,t-1)-C* Xpred(:,t-1)); % Filter update based on measurement Y(:,t-1), from (15) in handout
    P = P - P*C'*inv(C*P*C'+ R)*C*P;... % Uncertainty update, from (16)
    Xpred(:,t) = A*Xfilt(:,t);% Prediction, from (18)
    P = A*P*A'+Q; % From (19)
end
end

