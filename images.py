import os
import cv2
import face_recognition
import numpy as np

# IMPORT IMAGES
path = 'student_images'
images = []
student_names = []
myList = os.listdir(path)

for rawImg in myList:
    # To avoid files that are not images eg: .DS_store file
    if rawImg.startswith('.'):
        continue
        
    current_img = cv2.imread(f'{path}/{rawImg}')
    images.append(current_img)
    student_names.append(os.path.splitext(rawImg)[0])
    
# GET ENCODINGS OF EXISTING IMAGES IN THE LIST    
def getEncodingOfExistingImages():
    global images
    
    listOfEncodings = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img_encoding = face_recognition.face_encodings(img)[0]
        listOfEncodings.append(img_encoding)
    return listOfEncodings


def getStudentNames():
    global student_names
    return student_names