import cv2
import numpy as np
import os 

print(dir (cv2.face))
recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('/home/pi/Desktop/haarcascade_frontalface_default.xml')
cascadePath = "/home/pi/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
items = ['Deol', 'Intruder'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video widht
cam.set(4, 480) # set video height

# Define min window size to be recognized as a face
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

def FACE_RECOGNITION():
    while True:

        ret, img =cam.read()
        img = cv2.flip(img, -1) # Flip vertically

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
           )

        for(x,y,w,h) in faces:

            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])


            if (confidence < 100 and confidence >37):
                    id = 0
                    confidence = "  {0}%".format(round(100 - confidence)) 
            elif(confidence<37):
                    id = 1
                    confidence = "  {0}%".format(round(100 - confidence))
            else:
                    id = 1
                    confidence = "  {0}%".format(round(100 - confidence))
        
            cv2.putText(img, str(items[id]), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
            if(id==0):
                print()
            #bus_.write_byte(addr, 0x1) # switch the house led on as the owner is home
                
            elif(id==1):
            #EMAIL()# the intruder is detected send the mail to the user
                cv2.imwrite('/home/pi/Desktop/Intruder.jpg', img) 
    
        cv2.imshow('camera',img) 

        k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
FACE_RECOGNITION()

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()