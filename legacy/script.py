# Special exception when multiple people are on same bullet slot
class MultiplePeopleCollision(Exception):
    pass 


# bullet manager
bulletToName = {}

# name remainder manager
nameCounts = {}

# maxsize for array generation
maxsize = 0
finalArray = []

def driver():
    with open('input.txt') as f:
        while True:
            line = f.readline()
            if not line: 
                break

            # process each line
            core = lineProcessor(line)
            # store maxsize:
            processor(core[0], core[1], core[2])
            # core = [name_store, number_store, combinedList]

    slotPeople()
    output()


# Process each line
def lineProcessor(line):
    # process each character
    name_store = ''
    nameMode = True 

    i = 0

    for c in line:
        # detect first instance and proceed to find 
        if c == '(':
            i += 1
            break

        if nameMode:
            # append to name
            name_store += c
            i += 1
        
    # strip whitespace 
    name_store = name_store.strip()

    # print(name_store) # - test passing

    print('Processing: ' + name_store)

    number_store = ''

    # process the desired slots
    while i < len(line):
        if line[i] == ')':
            # break to end 
            i += 1
            break

        number_store += line[i]
        i += 1
    
    number_store = int(number_store)
    # print(number_store) #- test passing

    # process desired numbers
    comma_sep_numbers_string = ''
    curlySearch = False
    bulletNumbers = []

    while i < len(line):
        # search for { to begin 
        if line[i] == '{':
            curlySearch = True
            i += 1
            continue

        if line[i] == '}':
            i += 1
            break

        if line[i] == '[':
            break
            # goto next section

        if curlySearch:
            comma_sep_numbers_string += line[i]

        i += 1

    if curlySearch:
        bulletNumbers = comma_sep_numbers_string.split(',')
        bulletNumbers = list(map(int, bulletNumbers))


    # print(bulletNumbers) # test passing

    # process desired ranges
    comma_sep_range_string = ''
    rangeSearch = False
    rangeStartEndNumbers = []

    while i < len(line):
        # search for { to begin 
        if line[i] == '[':
            rangeSearch = True
            i += 1
            continue

        if line[i] == ']':
            i += 1
            break

        if rangeSearch:
            comma_sep_range_string += line[i]

        i += 1

    combinedList = []

    if rangeSearch:
        rangeStartEndNumbers = comma_sep_range_string.split(',')
        rangeStartEndNumbers = list(map(int, rangeStartEndNumbers))
        # activate range generator
        rangeList = generateRange(rangeStartEndNumbers[0], rangeStartEndNumbers[1])
        # combine sets
        # print(rangeList)
        combinedList = rangeList + bulletNumbers

    else:
        # set only, no range
        combinedList = bulletNumbers

    
    combinedList = set(combinedList)
    combinedList = list(combinedList)

    # print(combinedList)

    return [name_store, number_store, combinedList]
    

# range generator 

def generateRange(start, end):
    # list of numbers
    templist = []
    for i in range(start, end+1):
        templist.append(i)

    # return 
    return templist
    
        
# PROCESSOR - store in 

def processor(name_store, number_store, combinedList):
    # handle if there are excess cases

    if number_store > len(combinedList):
        remain = number_store - len(combinedList) 
        nameCounts[name_store] = remain
    
    # process bullets
    for bullet in combinedList:
        if bullet in bulletToName:
            # collision occured, THROW AN ERROR
            print('ERROR: Multiple people on same bullet slot')
            raise MultiplePeopleCollision('Error: Collision Occured')
        else:
            bulletToName[bullet] = name_store

# manage excess by slotting people
# slot in between maxrange, else append
def slotPeople():

    # first empty index
    firstEmpty = 1

    # print(nameCounts)
    
    # iterate through the whole dictionary
    for name in nameCounts:
        nameRemain = nameCounts[name]
        while nameRemain > 0:
            # try to slot in
            if firstEmpty in bulletToName:
                # already has name present
                firstEmpty += 1
                continue
            else: 
                # slot
                bulletToName[firstEmpty] = name
                nameRemain -= 1

# OUTPUT generator
def output():
    with open('output.txt','w') as file:
        for key in sorted(bulletToName.keys()) :
            s = str(key) + ". " + bulletToName[key]
            file.write(s)
            file.write('\n')


# --- RUN ALL CODE ---
driver()
