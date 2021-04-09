from datetime import datetime
import os.path

def markAttendance(name):
    # TODAY'S DATE
    today = datetime.date(datetime.now())
    directory = 'attendance_register'
    file_path = f"{directory}/{today}.csv"
    
    # CHECKS IF THE FILE EXISTS
    exists = os.path.exists(file_path)
    
    # IF THE FILE_PATH DOESN'T EXIST, CREATE ONE
    if exists == False:
        file = open(file_path, 'w')
        file.close()
    
    with open(file_path, 'r+') as f:
        current_register = f.readlines()
        
        name_exists = False
        
        # CHECK IF THE NAME ALREADY EXISTS
        for line in current_register:
            pair = line.split(',')
            
            if pair[0] == name:
                name_exists = True
                
        if name_exists == False:
            c = datetime.now()
            time = c.strftime('%H:%M:%S')
            # record the attendance
            f.writelines(f"\n{name}, {time}")
            

