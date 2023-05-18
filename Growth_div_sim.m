%% deterministic
clearvars
L_0=4;% initial size
T=1200;% division time in seconds, also specifies the growth rate
t_Rng=240000;% time range of simulation
for i =1:1
    L(1)=L_0;
    for t=2:t_Rng
        L(t)=L(t-1)*exp(log(2)/T);
        if L(t)>2*L_0
            L(t)=L(t)/2;
        end
    end
    plot(L); hold on
end

%% Sizer
L_0=4;% initial size
T=120;% average division time in seconds, also specifies the growth rate
CV_grow = 0.4;% taken from Suckjoon's data
CV_div = 0.055;% suckjoon's data
noiseF = 0.1;% the noise in the sizer factor

L_b=[];
L_d=[];
n_Cell=1;% number of traces to be simulated
t_Rng=24000;% time range of simulation
g=1/T;% for fixed growth
g1=linspace(1*g,1.5*g,t_Rng);% range of changing growth
L=nan(1,t_Rng-1);

for i =1:n_Cell
    L(1)=L_0;% initiate the run
    L_birth=[];
    L_div=[];
    L_div_lim=2*L_0+randn(1)*noiseF;% division cutoff, renewed every division
    for t=2:t_Rng
%         L(t)=L(t-1)+L(t-1)*(exp(log(2)*g)-1)*(1+randn(1,1)*CV_grow);
        L(t)=L(t-1)+L(t-1)*(exp(log(2)*g1(t))-1)*(1+randn(1,1)*CV_grow);
        if L(t)>=L_div_lim
            L_div=[L_div,L(t)];% storing division length
            L(t)=L(t)*0.5*(1+randn(1)*CV_div);% cell division
            L_birth=[L_birth,L(t)];% storing new born length
            L_div_lim=2*L_0*(1+randn(1)*noiseF);% resetting the division cutoff
        end
    end
    plot(L); hold on
    L_b=[L_b,L_birth(1:end-1)];% store in proper order
    L_d=[L_d,L_div(2:end)];
end
c=corrcoef(L_b, L_d); disp(c)

%% timer
close all, clear all;
L_0=4;% initial size
T=1200;
CV_grow = 0.08;
CV_div = 0.055;
noiseF = 0.1;

L_b=[];
L_d=[];
n_Cell=1;
t_Rng=240000;
g=1/T;% for fixed growth
g1=linspace(1*g,0.5*g,t_Rng);% range of changing growth
L=nan(1,t_Rng-1);
for i =1:n_Cell
    L(1)=L_0;
    L_birth=[];
    L_div=[];
    T_div_lim=T*(1+randn(1)*noiseF);
    t_afterDiv=0;
    for t=2:t_Rng
        L(t)=L(t-1)+L(t-1)*(exp(log(2)*g)-1)*(1+randn(1,1)*CV_grow);
%         L(t)=L(t-1)+L(t-1)*(exp(log(2)*g1(t))-1)*(1+randn(1,1)*CV_grow);
        t_afterDiv=t_afterDiv+1;
        if t_afterDiv>=T_div_lim
            L_div=[L_div,L(t)];
            L(t)=L(t)*0.5*(1+randn(1)*CV_div);% cell division
            L_birth=[L_birth,L(t)];
            T_div_lim=T*(1+randn(1)*noiseF);% resetting
            t_afterDiv = 0;
        end
    end
    plot(L); hold on
    L_b=[L_b,L_birth(1:end-1)];
    L_d=[L_d,L_div(2:end)];
end
c=corrcoef(L_b, L_d); disp(c)

%% Adder
close all
L_0=4;% initial size
T=1200;
CV_grow = 0.1;
CV_div = 0.055;
noiseF = 0.1;
L_b=[];
L_d=[];
n_Cell=1;
t_Rng=240000;
g=1/T;% for fixed growth
% g1=linspace(1*g,0.5*g,t_Rng);% range of changing growth
L=nan(1,t_Rng-1);
for i =1:n_Cell
    L(1)=L_0;
    L_birth=[];
    L_div=[];
    L_add=0;
    L_add_lim=L_0*(1+randn(1)*noiseF);
    for t=2:t_Rng
        L_grow = L(t-1)*(exp(log(2)*g)-1)*(1+randn(1,1)*CV_grow);
        L(t)=L(t-1)+L_grow;
        L_add=L_add+L_grow;
        if L_add >= L_add_lim
            % disp([L_add L_add_lim])
            L_div=[L_div,L(t)];
            L(t)=L(t)*0.5*(1+randn(1)*CV_div);% cell division
            L_birth=[L_birth,L(t)];
            L_add_lim=L_0*(1+randn(1)*noiseF);% renewed for every div
            L_add = 0;
        end
    end
    plot(L); hold on
    L_b=[L_b,L_birth(1:end-1)];
    L_d=[L_d,L_div(2:end)];
end
c=corrcoef(L_b, L_d); disp(c)
