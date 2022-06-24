# bullet manager
bulletToName = {}

# name remainder manager
nameCounts = {}

# maxsize for array generation
maxsize = 0
finalArray = []


# Process each line
def lineProcessor(line) -> list:
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

    # process desired numbers
    comma_sep_numbers_string = ''
    curlySearch = False
    bulletNumbers = []

    while i < len(line):
        # search for { to begin 
        if line[i] == '<':
            curlySearch = True
            i += 1
            continue

        if line[i] == '>':
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
        try:
            rangeList = generateRange(rangeStartEndNumbers[0], rangeStartEndNumbers[1])
            combinedList = rangeList + bulletNumbers
        except IndexError:
            print("No range passed")
            pass
        # combine sets
        # combinedList = rangeList + bulletNumbers

    else:
        # set only, no range
        combinedList = bulletNumbers

    
    combinedList = set(combinedList)
    combinedList = list(combinedList)

    return [name_store, number_store, combinedList]


def generateRange(start, end) -> list:
    templist = []
    for i in range(start, end+1):
        templist.append(i)

    return templist


def processor(name_store, number_store, combinedList) -> None:
    # handle if there are excess cases

    # Special exception when multiple people are on same bullet slot
    class MultiplePeopleCollision(Exception):
        pass

    if number_store > len(combinedList):
        remain = number_store - len(combinedList) 
        nameCounts[name_store] = remain
    
    # process bullets
    for bullet in combinedList:
        if bullet in bulletToName:
            print(bullet)
            # collision occured, THROW AN ERROR
            print('ERROR: Multiple people on same bullet slot')
            raise MultiplePeopleCollision('Error: Collision Occured')
        else:
            bulletToName[bullet] = name_store

# manage excess by slotting people
# slot in between maxrange, else append
def slotPeople() -> None:

    # first empty index
    firstEmpty = 1
    
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


def generate_output_file():
    with open("output.txt", "w") as file:
        for key in sorted(bulletToName.keys()) :
            s = str(key) + ". " + bulletToName[key]
            file.write(s)
            file.write('\n')
        file.close()


def driver(name: str,
           total_num_spots: int,
           called_spots=0,
           range_called_spots=0
           ) -> list:

    # lines = ["Jack Owens (11) <2>",
    #         "Bob Jones (4) <16, 17>"
    #         ]

    line = f"{name} ({total_num_spots}) <{called_spots}> [{range_called_spots}]"
    print(f"line is {line}")

    # for line in lines:

    # process each line
    core = lineProcessor(line) # -> [name_store, number_store, combinedList]
    print(core)
    # store maxsize:
    processor(core[0], core[1], core[2])

    slotPeople()
    generate_output_file()
    
    raw_values = []
    for key in sorted(bulletToName.keys()):
        s = str(key) + ". " + bulletToName[key]
        raw_values.append(s)

    return raw_values


# driver("Bob Jones", total_num_spots=9, range_called_spots=[1,5], called_spots=42)
# driver("Bob Jones", total_num_spots=9, called_spots=42)
# driver("Bob Jones", total_num_spots=7)
