function sigwave = cds2sig( cdswave, interval, points)
%UNTITLED SIGWAVE = CDS2SIG(CDSWAVE, INTERVAL, POINTS) 
%   CDSWAVE is a Cadence-generated waveform read in with cds_srr 
%   INTERVAL is the duration of the interval to be translated
%   POINTS is the number of equidistant points in the output array 

[ pointcount, wavecount ] = size(cdswave.V) ; 

% there may be NaNs in the last row, but they are ignored by max() 
intervalend = max(cdswave.time(end,:)) ; 
intervalstart = intervalend - interval ; 
% first time point should be the same in all vectors 
if (intervalstart < cdswave.time(1,1)) 
    error('interval too large') ;
end 

tick = linspace(intervalstart, intervalend, points + 1) ; 

sigwave.time = tick'; 
for i=1:wavecount
    % set last ix to just before first NaN, if any 
    lastix = pointcount ; 
    for j = 1:pointcount
        if (isnan(cdswave.V(j,i)))
            lastix = j-1 ; 
            break ; 
        end
    end
    sigwave.signals.values(:,i) = ...
        interp1(cdswave.time(1:lastix,i), ...
                cdswave.V(1:lastix,i), ...
                tick, 'spline')' ; 
end 
end

