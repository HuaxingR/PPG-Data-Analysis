function [ y ] = myfiltfilt( x,Nord,wn,type,plot_filt )
%LPF Summary of this function goes here
%   Detailed explanation goes here
%0=>LPF IIR
%1=>HPF IIR
%2=>BPF IIR
%3=>DS/US+HBF
%4=>LPF FIR
%5=>HPF US + LPF

if type==0
    [b,a] = butter(Nord,wn,'low');
    y = filtfilt(b,a,x);
elseif type==1
    [b,a] = butter(Nord,wn,'high');
    y = filtfilt(b,a,x);
elseif type==2
    [b,a] = butter(Nord,wn,'bandpass');
    y = filtfilt(b,a,x);
elseif type==3
    [b]= firhalfband(40,(1/8)/(0.5));
    a=1;
    if Nord>1
        for i=1:log2(Nord)
            y1 = filtfilt(b,a,x);
            y1_ds=downsample(y1,2);
            x=y1_ds;
        end
        y=y1_ds;
    else
        y=x;
    end
    
elseif type==4
    rp = 1;           % Passband ripple
    rs = 20;          % Stopband ripple
    fs = 1;        % Sampling frequency
    f = wn;    % Cutoff frequencies
    a = [1 0];        % Desired amplitudes
    dev = [(10^(rp/20)-1)/(10^(rp/20)+1)  10^(-rs/20)];
    [n,fo,ao,w] = firpmord(f,a,dev,fs);
    b = firpm(n,fo,ao,w);
    y = filtfilt(b,a,x);
    
elseif type==5
    [b]= firhalfband(40,(1/8)/(0.5));
    a=1;
    if Nord>1
        for i=1:log2(Nord)
            y1_us=upsample(x,2)*2;
            y1_filt = filtfilt(b,a,y1_us);
            x=y1_filt;
        end
        y=y1_filt;
    else
        y=x;
    end
end

if plot_filt==1
    freqz(b,a,1024*8,11e3);
    y=0;
end