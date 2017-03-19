import random

closed_list=[]
picked_list=[]

class Point:

    def __init__(self,position,G_value,H_value,F_value):
        '''Initializes the point's data.'''
        self.position=position
        self.G_value=G_value
        self.H_value=H_value
        self.F_value=F_value
        self.distance=distance
    #def __repr__(self):
    #    return '%s' % (self.position,)

class Target:
    def __init__(self,position,item,value):
        '''Initializes the poiont's data.'''
        self.position=position
        self.item=item
        self.value=value

#find target to move to (near or full inventory)
flag_fullinventory = 0



def findTargetList(current_level_layout,current_position_of_monkey):
    target_list=[]
    for i in range(0,len(current_level_layout[0])):
        for j in range(0,len(current_level_layout[0])):
            if current_level_layout[i][j] == 'song' or current_level_layout[i][j] =='album' or current_level_layout[i][j] == 'playlist':
                value=int(abs(current_position_of_monkey[0]-i)+abs(current_position_of_monkey[1]-j)-1)
                positionPoint=[]
                positionPoint.append(i)
                positionPoint.append(j)
                target=Target(positionPoint,current_level_layout[i][j],value)
                target_list.append(target)
    return target_list

def findTarget(target_list):
    min_value = 100
    min_target=None
    for target in target_list:
        if target.value < min_value:
            min_value = target.value
            min_target=target
        '''
        print '--- min F_value ---'
        print '(%d,%d)'%(target.position[0],target.position[1])
        print min_value
        print '--- min F_value ---'
        '''
    return min_target



def move(current_game_state):
    '''This is where you put your AI code!

    The AI looks at the current game state and decides
    the monkey's next move.'''

    # Go to http://github.com/monkey-music-challenge/core
    # for more info about the rules of Monkey Music Challenge

    # The real fun begins when the warmup is over and the competition begins!
    current_level_layout = current_game_state['layout']

    # This is an array of all music items you've currently picked up
    inventory= current_game_state['inventory']

    # The size of an array which indicates all music items you've currently picked up
    inventorySize = current_game_state['inventorySize']

    # The position attribute tells you where your monkey is
    current_position_of_monkey = current_game_state['position']
    # TODO: You may want to do something smarter here
    '''
    return {'command': 'move',
            'direction': random.choice(['up', 'down', 'left', 'right'])}
    
    first_point=findTarget(findTargetList(current_level_layout,current_position_of_monkey)).position

    open_list=[]

    '''add monkey's current position to closed list'''
    closed_list.append(current_position_of_monkey)

    # up
    if current_position_of_monkey[0]-1<0 or current_level_layout[current_position_of_monkey[0]-1][current_position_of_monkey[1]] == 'wall' :
        print 'up bound or wall'
    else:
        judge_point=[current_position_of_monkey[0]-1,current_position_of_monkey[1]]
        print '--- judge_point ---'
        print judge_point
        print '--- judge_point ---'
        if judge_point in closed_list:
            print 'judge_point in closed_list'
            pass
        else:
            print current_level_layout[current_position_of_monkey[0]-1][current_position_of_monkey[1]]
            positionPoint=[]
            positionPoint.append(current_position_of_monkey[0]-1)
            positionPoint.append(current_position_of_monkey[1])
            point=Point(positionPoint,1,1,1)
            open_list.append(point)

    # down
    if current_position_of_monkey[0]+1>len(current_level_layout[0])-1 or current_level_layout[current_position_of_monkey[0]+1][current_position_of_monkey[1]] == 'wall':
        print 'bottom bound or wall'
    else:
        judge_point=[current_position_of_monkey[0]+1,current_position_of_monkey[1]]
        print '--- judge_point ---'
        print judge_point
        print '--- judge_point ---'
        if judge_point in closed_list:
            print 'judge_point in closed_list'
            pass
        elif judge_point in picked_list:
            print 'judge_point in picked_list'
            pass
        else:
            print current_level_layout[current_position_of_monkey[0]+1][current_position_of_monkey[1]]
            positionPoint=[]
            positionPoint.append(current_position_of_monkey[0]+1)
            positionPoint.append(current_position_of_monkey[1])
            point=Point(positionPoint,1,1,1)
            open_list.append(point)

    # left
    if current_position_of_monkey[1]-1<0 or current_level_layout[current_position_of_monkey[0]][current_position_of_monkey[1]-1] == 'wall':
        print 'left bound or wall'
    else:
        judge_point=[current_position_of_monkey[0],current_position_of_monkey[1]-1]
        print '--- judge_point ---'
        print judge_point
        print '--- judge_point ---'
        if judge_point in closed_list:
            print 'judge_point in closed_list'
            pass
        elif judge_point in picked_list:
            print 'judge_point in picked_list'
            pass
        else:
            print current_level_layout[current_position_of_monkey[0]][current_position_of_monkey[1]-1]
            positionPoint=[]
            positionPoint.append(current_position_of_monkey[0])
            positionPoint.append(current_position_of_monkey[1]-1)
            point=Point(positionPoint,1,1,1)
            open_list.append(point)

    # right
    if current_position_of_monkey[1]+1>len(current_level_layout[0])-1 or current_level_layout[current_position_of_monkey[0]][current_position_of_monkey[1]+1] == 'wall':
        print 'right bound or wall'
    else:
        judge_point=[current_position_of_monkey[0],current_position_of_monkey[1]+1]
        print '--- judge_point ---'
        print judge_point
        print '--- judge_point ---'
        if judge_point in closed_list:
            print 'judge_point in closed_list'
            pass
        elif judge_point in picked_list:
            print 'judge_point in picked_list'
            pass
        else:
            print current_level_layout[current_position_of_monkey[0]][current_position_of_monkey[1]+1]
            positionPoint=[]
            positionPoint.append(current_position_of_monkey[0])
            positionPoint.append(current_position_of_monkey[1]+1)
            point=Point(positionPoint,1,1,1)
            open_list.append(point)


    for point in open_list:
        h_value=int(abs(first_point[0]-point.position[0])+abs(first_point[1]-point.position[1])-1)
        point.H_value=h_value
        point.G_value=1
        point.F_value=int(point.H_value+point.G_value)

# Find the point with minimal value of F_value
    open_list.reverse()
    min_F_value = 100
    for point in open_list:
        if point.F_value < min_F_value:
            min_F_value = point.F_value
            min_point=point
    
    #closed_list.append([min_point.position[0],min_point.position[1]])


#make decision

    direction='up'
    if min_point.position[0] - current_position_of_monkey[0] < 0 and min_point.position[1] == current_position_of_monkey[1]:
        print 'go up'
        direction='up'
    elif min_point.position[0] - current_position_of_monkey[0] > 0 and min_point.position[1] == current_position_of_monkey[1]:
        print 'go down'
        direction='down'
    elif min_point.position[0] == current_position_of_monkey[0] and min_point.position[1]-current_position_of_monkey[1] < 0:
        print 'go left'
        direction='left'
    elif min_point.position[0] == current_position_of_monkey[0] and min_point.position[1]-current_position_of_monkey[1] > 0:
        print 'go right'
        direction='right'


    if current_level_layout[min_point.position[0]][min_point.position[1]] == 'song' or current_level_layout[min_point.position[0]][min_point.position[1]] == 'playlist' or current_level_layout[min_point.position[0]][min_point.position[1]] == 'album' : # or current_level_layout[min_point.position[0]][min_point.position[1]] == 'user'
        if current_level_layout[min_point.position[0]][min_point.position[1]] == 'user':
            pass
        else:
            picked_point=[min_point.position[0],min_point.position[1]]
            picked_list.append(picked_point)
            del closed_list[:]
    print '@@@@@@@'

    #return direction #'up'
    return {'command': 'move','direction': direction}


#input





