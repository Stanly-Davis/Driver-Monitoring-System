#This code was used in Raspberry Pi 3B+


from scipy.spatial import distance as dist
from imutils.video import VideoStream
from imutils import face_utils
import numpy as np
import argparse
import imutils
import time
import dlib
import cv2

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

import smtplib
from email.message import EmailMessage
import imghdr



def eye_aspect_ratio(eye):

    A = dist.euclidean(eye[1], eye[5])
    B = dist.euclidean(eye[2], eye[4])
    C = dist.euclidean(eye[0], eye[3])

    ear = (A + B) / (2.0 * C)

    return ear

def final_ear(shape):

    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    leftEye = shape[lStart:lEnd]
    rightEye = shape[rStart:rEnd]

    leftEAR = eye_aspect_ratio(leftEye)
    rightEAR = eye_aspect_ratio(rightEye)

    ear = (leftEAR + rightEAR) / 2.0

    return (ear, leftEye, rightEye)

def lip_distance(shape):

    top_lip = shape[50:53]
    top_lip = np.concatenate((top_lip, shape[61:64]))

    low_lip = shape[56:59]
    low_lip = np.concatenate((low_lip, shape[65:68]))

    top_mean = np.mean(top_lip, axis=0)
    low_mean = np.mean(low_lip, axis=0)

    distance = abs(top_mean[1] - low_mean[1])

    return distance

def sendMail():
    
    my_canvas = canvas.Canvas("Report.pdf", pagesize=letter)
    my_canvas.drawString(300,700, "Driver Report")
    image_path = 'saved_img.jpg'
    my_canvas.drawImage(image_path, 30, 500, width=100, height=100)

    my_canvas.save()
   
    Sender_Email = "xxxxxxxxxxxx@gmail.com"
    Reciever_Email = "xxxxxxxxxxx@gmail.com"
    Password = "snhw txsv poyt bixk"

    newMessage = EmailMessage()    
    newMessage['Subject'] = "Test Email" 
    newMessage['From'] = Sender_Email  
    newMessage['To'] = Reciever_Email  
    newMessage.set_content('This mail has image of driver attached to it. It shows at what time driver was sleepy.') 

    files = ['Report.pdf']
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name
        newMessage.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(Sender_Email, Password) 
        smtp.send_message(newMessage)      

    

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--webcam", type=int, default=0,help="index of webcam on system")
args = vars(ap.parse_args())

EYE_AR_THRESH = 0.25  #0.2
EYE_AR_CONSEC_FRAMES = 15   # 20   60
YAWN_THRESH = 25

COUNTER = 0

print("Loading the predictor and detector...")
detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")    #This is faster with lower accuracy
predictor = dlib.shape_predictor('shape_predictor_68_face_landmarks.dat')


print("Starting Video Stream....")
vs= VideoStream(usePiCamera=True).start()      #This line is for Raspberry pi camera. To be used in laptop or PC, replace with the line : vs = VideoStream(src=args["webcam"]).start()
time.sleep(1.0)

while True:

    frame = vs.read()
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    #rects = detector(gray, 0)
    rects = detector.detectMultiScale(gray, scaleFactor=1.1,minNeighbors=5, minSize=(30, 30),flags=cv2.CASCADE_SCALE_IMAGE)

    #for rect in rects:
    for (x, y, w, h) in rects:
        rect = dlib.rectangle(int(x), int(y), int(x + w),int(y + h))
        
        shape = predictor(gray, rect)
        shape = face_utils.shape_to_np(shape)

        eye = final_ear(shape)
        ear = eye[0]
        leftEye = eye [1]
        rightEye = eye[2]

        distance = lip_distance(shape)

        leftEyeHull = cv2.convexHull(leftEye)
        rightEyeHull = cv2.convexHull(rightEye)

        lip = shape[48:60]

        if ear < EYE_AR_THRESH:
            COUNTER += 1

            if COUNTER >= EYE_AR_CONSEC_FRAMES:
                cv2.putText(frame, "Sleepy", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.imwrite(filename='saved_img.jpg', img=frame)
                sendMail()
                print("Mail sent")

        else:
            COUNTER = 0
    

        if (distance > YAWN_THRESH):
                cv2.putText(frame, "Yawn", (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


        cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.putText(frame, "YAWN: {:.2f}".format(distance), (300, 60),cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF


    if key == ord("q"): 
        vs.stop()
        cv2.destroyAllWindows()
        break
