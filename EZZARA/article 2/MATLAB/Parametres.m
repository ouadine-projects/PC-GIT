pas=0.01; %sample time de quelques blocs
%%%%%%%%%%%%%%%Paramètre liés au quadri-rotor%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
m=0.400;% masse du quadri-rotor
g =9.806; %l’accélération de la pesanteur
d =0.205 %d is the distance between the quadrotor center of mass and the rotation axis of propeller 
Kp =2.9842e-5 %K is the lift coefficient
Kd =3.2320e-7%the drag coefficient
Jr=2.8385e-5 %the rotor inertia
Ix=3.8278e-3, Iy=3.8278e-3, Iz=7.1345e-3;
Kfax =5.5670e-4, Kfay =5.5670e-4, Kfaz =6.3540e-4;%the aerodynamic friction coefficients around (X,Y,Z)
Kftx =0.032, Kfty =0.032, Kftz =0.048;% the translation drag coefficients

%%%%%%%%%%%%%%%Les Coefficient ai %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
a1=(Iy-Iz)/Ix;
a2=(-Kfax/Ix);
a3=(-Jr/Ix);
a4=(Iz-Ix)/Iy;
a5=(-Kfay/Iy);
a6=(Jr/Iy);
a7=(Ix-Iy)/Iz;
a8=(-Kfaz/Iz);
a9=(-Kftx/m);
a10=(-Kfty/m);
a11=(-Kftz/m);
b1=(d/Ix);
b2=d/Iy;
b3=1/Iz;
%%%%%%%%%%%%%%%Inversion de la matrice %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
law1=[Kp Kp Kp Kp;-Kp 0 Kp 0;0 -Kp 0 Kp;Kd -Kd Kd -Kd]
law2=inv(law1)
% K4=0.00001;
%%%%%%%%%%%%%%%Incertitude %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
DKfax=0.25*Kfax;
DKfay=0.25*Kfay;
DKfaz=0.25*Kfaz;

DKftx=0.25*Kftx;
DKfty=0.25*Kfty;
DKftz=0.25*Kftz;