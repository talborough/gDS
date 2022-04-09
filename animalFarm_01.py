# To consume this file (once only) in a Python program: 
 
#     from past.builtins import execfile 
#     execfile ('<file name>.py') 
 
# Start of gDS include file ...
 
from multiprocessing import Manager 
gDSMgr = Manager() 
 
# 
# Define global shared variables for table gFarm 
# 
gFarm_Name = gDSMgr.list() 
gFarm_gCounty_Index = gDSMgr.list() 
 
# 
# Define global shared variables for table gCounty 
# 
gCounty_Name = gDSMgr.list() 
gCounty_Name2Index = gDSMgr.dict() 
 
# 
# Define global shared variables for table gAnimal 
# 
gAnimal_gFarm_Index = gDSMgr.list() 
gAnimal_Type = gDSMgr.list() 
gAnimal_Name = gDSMgr.list() 
gAnimal_RowStatus = gDSMgr.list() 

# 
# Add a row to table gFarm WITHOUT a lock 
# 
def gFarm_AddARow(\
    _Name,\
    _gCounty_Index = None,\
): 
    gFarm_Name.append(_Name) 
    gFarm_gCounty_Index.append(_gCounty_Index) 
    thisIndex = len(gFarm_gCounty_Index) - 1 
    return (thisIndex) 

# 
# Add a row to table gCounty WITHOUT a lock 
# 
def gCounty_AddARow(\
    _Name,\
): 
    gCounty_Name.append(_Name) 
    thisIndex = len(gCounty_Name) - 1 
    return (thisIndex) 

# 
# Add a row to table gAnimal under lock 
# 
def gAnimal_AddARowUnderLock(\
    _gFarm_Index,\
    _Type,\
    _Name,\
    _RowStatus,\
): 
    MasterLock('lock') 
    gAnimal_gFarm_Index.append(_gFarm_Index) 
    gAnimal_Type.append(_Type) 
    gAnimal_Name.append(_Name) 
    gAnimal_RowStatus.append(_RowStatus) 
    thisIndex = len(gAnimal_RowStatus) - 1 
    MasterLock('unlock') 
    return (thisIndex) 

# 
# Print values out for table 'gFarm' 
# 
def gFarm_DumpTable(rangeListToDump = None): 
    print (f'**************') 
    print (f'**************') 
    print ('    Table %24s (using locker = None) has %d entries' % ('gFarm', len(gFarm_Name))) 
    print (f'**************') 
    print (f'**************') 
    print (f'') 
    for i in range (0, len(gFarm_Name)): 
        if (rangeListToDump is None) or (i in rangeListToDump): 
            print ('    Row index = %d' % (i)) 
            print ('    %30s = %10s' % ('gFarm_Name', gFarm_Name[i])) 
            print ('    %30s = %10s  (%30s)' % ('gFarm_gCounty_Index', gFarm_gCounty_Index[i], gCounty_Name[gFarm_gCounty_Index[i]])) 

# 
# Print values out for table 'gCounty' 
# 
def gCounty_DumpTable(rangeListToDump = None): 
    print (f'**************') 
    print (f'**************') 
    print ('    Table %24s (using locker = None) has %d entries' % ('gCounty', len(gCounty_Name))) 
    print (f'**************') 
    print (f'**************') 
    print (f'') 
    for i in range (0, len(gCounty_Name)): 
        if (rangeListToDump is None) or (i in rangeListToDump): 
            print ('    Row index = %d' % (i)) 
            print ('    %30s = %10s' % ('gCounty_Name', gCounty_Name[i])) 

# 
# Print values out for table 'gAnimal' 
# under lock MasterLock 
# 
def gAnimal_DumpTable(rangeListToDump = None): 
    MasterLock('lock') 
    print (f'**************') 
    print (f'**************') 
    print ('    Table %24s (using locker = MasterLock) has %d entries' % ('gAnimal', len(gAnimal_Name))) 
    print (f'**************') 
    print (f'**************') 
    print (f'') 
    for i in range (0, len(gAnimal_Name)): 
        if (rangeListToDump is None) or (i in rangeListToDump): 
            print ('    Row index = %d' % (i)) 
            print ('    %30s = %10s  (%30s)' % ('gAnimal_gFarm_Index', gAnimal_gFarm_Index[i], gFarm_Name[gAnimal_gFarm_Index[i]])) 
            print ('    %30s = %10s' % ('gAnimal_Type', gAnimal_Type[i])) 
            print ('    %30s = %10s' % ('gAnimal_Name', gAnimal_Name[i])) 
            print ('    %30s = %10s' % ('gAnimal_RowStatus', gAnimal_RowStatus[i])) 
    MasterLock('unlock') 
