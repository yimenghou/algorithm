function [ sequence ] = zigzag( block )
% blocks in, sequences out
[N1,N2] = size(block);
sequence = zeros(1,N1*N2);
% pointer
countrow = 1;countcol = 1;count = 1;

while countrow<=N1 && countcol<=N2
    if countrow==1 && mod(countrow+countcol,2)==0 && countcol~=N2
		sequence(count) = block(countrow,countcol);
        countcol = countcol+1; % move right at the top
		count = count+1;
		
	elseif countrow==N1 && mod(countrow+countcol,2)~=0 && countcol~=N2
		sequence(count) = block(countrow,countcol);
		countcol = countcol+1; % move right at the bottom
		count = count+1;
		
	elseif countcol==1 && mod(countrow+countcol,2)~=0 && countrow~=N1
		sequence(count) = block(countrow,countcol);
		countrow = countrow+1; % move down at the left
		count = count+1;
		
	elseif countcol==N2 && mod(countrow+countcol,2)==0 && countrow~=N1
		sequence(count) = block(countrow,countcol);
		countrow = countrow+1; % move down at the right
		count = count+1;
		
	elseif countcol~=1 && countrow~=N1 && mod(countrow+countcol,2)~=0
		sequence(count) = block(countrow,countcol);
		countrow = countrow+1; countcol = countcol-1; % move diagonally left down
		count = count+1;
		
	elseif countrow~=1 && countcol~=N2 && mod(countrow+countcol,2)==0
		sequence(count) = block(countrow,countcol);
		countrow = countrow-1; countcol=countcol+1;	% move diagonally right up
		count = count+1;
		
	elseif countrow==N1 && countcol==N2 %obtain the bottom right element
        sequence(end) = block(end); % end of the operation
		break
    end
end
end

