function [ block ] = invzigzag( sequence,N1,N2 )
% sequence in, block out
block = zeros(N1,N2);
% pointer 
countrow = 1;countcol = 1;count = 1;

while count<=N1*N2
	if countrow==1 && mod(countrow+countcol,2)==0 && countcol~=N2
		block(countrow,countcol)=sequence(count);
		countcol=countcol+1;							%move right at the top
		count=count+1;
		
	elseif countrow==N1 && mod(countrow+countcol,2)~=0 && countcol~=N2
		block(countrow,countcol)=sequence(count);
		countcol=countcol+1;							%move right at the bottom
		count=count+1;
		
	elseif countcol==1 && mod(countrow+countcol,2)~=0 && countrow~=N1
		block(countrow,countcol)=sequence(count);
		countrow=countrow+1;							%move down at the left
		count=count+1;
		
	elseif countcol==N2 && mod(countrow+countcol,2)==0 && countrow~=N1
		block(countrow,countcol)=sequence(count);
		countrow=countrow+1;							%move down at the right
		count=count+1;
		
	elseif countcol~=1 && countrow~=N1 && mod(countrow+countcol,2)~=0
		block(countrow,countcol)=sequence(count);
		countrow=countrow+1;		countcol=countcol-1;	%move diagonally left down
		count=count+1;
		
	elseif countrow~=1 && countcol~=N2 && mod(countrow+countcol,2)==0
		block(countrow,countcol)=sequence(count);
		countrow=countrow-1;		countcol=countcol+1;	%move diagonally right up
		count=count+1;
		
	elseif count==N1*N2						%input the bottom right element
        block(end)=sequence(end);							%end of the operation
		break										%terminate the operation
    end
end

