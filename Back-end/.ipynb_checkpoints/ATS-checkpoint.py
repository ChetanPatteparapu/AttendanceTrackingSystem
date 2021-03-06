import face_recognition
import numpy as np
import attendance
import cv2
import images


# GET ENCODINGS OF THE CURRENT STUDENTS
listOfEncodings = images.getEncodingOfExistingImages()
student_names = images.getStudentNames()

# CAPTURE FROM THE WEBCAM 
cap = cv2.VideoCapture(0)

while True:
    ret,frame = cap.read()
    
    # FOR PERFORMANCE RESIZE THE FRAME TO SMALL PIXELS
    frame_modified = cv2.resize(frame, (0,0), None, 0.25, 0.25)
    frame_modified = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    face_points = face_recognition.face_locations(frame_modified)
    frame_encoding = face_recognition.face_encodings(frame_modified, face_points)
    
    for faceEncode,faceLoc in zip(frame_encoding,face_points):
        matches = face_recognition.compare_faces(listOfEncodings,faceEncode)
        faceDis = face_recognition.face_distance(listOfEncodings,faceEncode)
        matchIndex = np.argmin(faceDis)
        
        if matches[matchIndex]:
            name = student_names[matchIndex].upper()
            y1,x2,y2,x1 = faceLoc
            
            cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,255),2)
            cv2.rectangle(frame, (x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(frame,name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255,255,255),2)
            attendance.markAttendance(name)
    
    cv2.imshow('Recording', frame)
    
    if cv2.waitKey(1) & 0xff == 27:
        break
        
        
cap.release()
cv2.destroyAllWindows()
    
    
            