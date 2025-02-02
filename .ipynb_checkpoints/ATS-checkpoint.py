import face_recognition
import numpy as np
import cv2

import attendance
import images


# GET ENCODINGS OF THE CURRENT STUDENTS
listOfEncodings = images.getEncodingOfExistingImages()
student_names = images.getStudentNames()

# CAPTURE FROM THE WEBCAM 
cap = cv2.VideoCapture(0)

#HASHSET TO KEEP TRACK OF ALREADY MARKED STUDENTS
marked = set()

while True:
    ret,frame = cap.read()
    
    # BELOW IS TO AVOID THE CASE WHEN THERE ARE NO IMAGES
    if len(listOfEncodings) > 0:
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
                cv2.rectangle(frame, (x1,y2-35),(x2,y2),(0,0,0),cv2.FILLED)
                cv2.putText(frame,name, (x1+6, y2-6), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255),2)
                
                if name in marked:
                    continue
                    
                attendance.markAttendance(name)
                # CACHE THE NAME
                marked.add(name)
    
    cv2.imshow('Recording', frame)
    
    if cv2.waitKey(1) & 0xff == 27:
        break
        
        
cap.release()
cv2.destroyAllWindows()