# Binary Search Algorithm
def binarySearch(values:list, target:int):
    notFound = True

    start = 0
    end = len(values) - 1

    while notFound:
        section = values[start:end]
        mid = len(section) // 2

        # print(start, end, mid, section[mid])
        # print(section)
        
        if section[mid] > target:
            end -= mid
        
        elif section[mid] < target:
            start += mid
        else:
            return start + mid
        
        if(len(section) <= 1):
            return start