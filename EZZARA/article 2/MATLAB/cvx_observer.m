%%%%%%%%%%%Robust sensor fault estimation and fault-tolerant control for uncertain Lipschitz nonlinear systems
Lf=35;
e1=0.5;
Y1=0.3*ones(4,12);%Y1=0.2*ones(4,12);

Ce=eye(22);

cvx_begin sdp

variable P(22,22) symmetric 
variable M1(22,12) 
variable M2(22,12)

P-0.001*eye(22)>=0;

PI1=P*Ap-M1*Cp*Ap-M2*Cp+(P*Ap-M1*Cp*Ap-M2*Cp)'+Ce'*Ce;

[PI1 (P-M1*Cp)*Dp
 ((P-M1*Cp)*Dp)' -e1*e1*eye(16)]-1*eye(38)<=0;

cvx_end
try chol(P);
%     clc
    disp('Matrix is symmetric positive definite%%%%%%%%%')
catch ME
    disp('%%%%%%%%%%Matrix is NOT symmetric positive definite%%%%%%%%%')
end
H=inv(P)*M1;
L1=inv(P)*M2;
T=eye(22)-H*Cp;
M=T*Ap-L1*Cp;
G=T*Bp;
N=T;
L2=(T*Ap-L1*Cp)*H;
L=L1+L2;