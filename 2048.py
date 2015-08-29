"""
Merge function for 2048 game.
"""

def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    
    shift_list = shift_left(line)
    merge_list = merge_pairs(shift_list)
    result_list = shift_left(merge_list)
    
    return result_list

def shift_left(line):
    """
    Function that moves all the values to the left.
    """
    
    result_list = [0] * len(line)
    
    # Put non zero values of line in the first 
    # available position in result_list
    first_available = 0
    for position in range(len(line)):
        if line[position] != 0:
            result_list[first_available] = line[position]
            first_available += 1
            
    return result_list

def merge_pairs(line):
    """
    Function that merges the possible pairs in a line.
    """
    result_list = line
    
    skip_next = False
    for position in range(len(line) - 1):
        if skip_next:
            skip_next = False
        elif line[position] == line[position + 1]:
            result_list[position] = line[position] * 2
            result_list[position + 1] = 0
            skip_next = True
            
    return result_list 

def test():
    """
    Test function.
    """
    
    line = [2, 0, 2, 4]
    print "[2, 0, 2, 4] should return [4, 4, 0, 0], returns " + str(merge(line))
    line = [0, 0, 2, 2]
    print "[0, 0, 2, 2] should return [4, 0, 0, 0], returns " +  str(merge(line))
    line = [2, 2, 0, 0]
    print "[2, 2, 0, 0] should return [4, 0, 0, 0], returns " +  str(merge(line))
    line = [2, 2, 2, 2, 2]
    print "[2, 2, 2, 2, 2] should return [4, 4, 2, 0, 0], returns " +  str(merge(line))
    line = [8, 16, 16, 8]
    print "[8, 16, 16, 8] should return [8, 32, 8, 0], returns " +  str(merge(line))
    
test()
    