from datetime import datetime

# MARKING ATTENDANCE
def markAttendance(name):
    with open('attendance_register.csv', 'r+') as f:
        myDataList = f.readlines()
        # HASHSET TO AVOID DUPLICATES AND QUICK LOOKUP
        nameList = set()
        for line in myDataList:
            entry = line.split(',')
            nameList.add(entry[0])
            
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name}, {dtString}')