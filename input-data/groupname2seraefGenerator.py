import csv

# this script generates the content for efgroupname2seraef.py 
# the content is output to bdtest.py (which I copied to efgroupname2seraef.py)

with open('EF_Module_Specs&LUT_Sept2019GroupName2EF.csv', encoding='utf-8-sig') as csvfile:
    reader = csv.DictReader(csvfile)
    region = ''
    closeRegion = False
    closeVegType = False
    closePhase = False
    
    averageEF = {}
    
    output_file  = open('bdtest.py', 'w')
    print("EF_GROUP_NAME_2_SERA_EF={", sep='', end='', file=output_file)
    for row in reader:
        if region != row['Region']:
            region = row['Region']
            if closeVegType:
                print("},", sep='', end='', file=output_file)
            closeVegType = False
            if closePhase: 
                print("},", sep='', end='', file=output_file)
            closePhase = False
            if closeRegion: 
                print("},", sep='', end='', file=output_file)
                closeRegion = False
            
            print('"', region, '":{', sep='', end='', file=output_file)
            closeRegion = True
            vegtype = ''
        
        if vegtype != row['VegType']:
            vegtype = row['VegType']
            if closePhase: 
                print("},", sep='', end='', file=output_file)
            closePhase = False
            if closeVegType: 
                print("},", sep='', end='', file=output_file)
                closeVegType = False

            print('"', vegtype, '":{', sep='', end='', file=output_file)
            closeVegType = True
            phase = ''
        
        if phase != row['Phase']:
            phase = row['Phase']
            if closePhase: 
                print("},", sep='', end='', file=output_file)
                closePhase = False

            print('"', phase.strip(), '":{', sep='', end='', file=output_file)
            closePhase = True
            pollutant = ''
        
        pollutant = row['Pollutant']
        if phase == 'FireAvg':
            averageEF[pollutant] = row['EF']
        
        print('"', pollutant, '":', sep='', end='', file=output_file)
        ef = row['EF']
        if ef == '':
            ef = averageEF[pollutant]
        print('{"EF":', ef, sep='', end='', file=output_file)
        sd = row['SD']
        if sd == '':
            sd = 0
        print(',"SD":', sd, sep='', end='', file=output_file)
        n = row['n']
        if n == '':
            n = 0
        print(',"n":',n, '},', sep='', end='', file=output_file)
            
    print("},},},}", sep='', end='', file=output_file)
    
