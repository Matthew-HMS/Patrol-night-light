# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from typing import Text
import os
import sys
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, StickerSendMessage, ImageSendMessage
import RPi.GPIO as GPIO
from time import sleep
from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import imutils
import pickle
import time
import cv2
import requests
import threading
import pyimgur

app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
mailgun_api_key = os.getenv('MAILGUN_API_KEY', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

# authenticate
line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

@app.route("/callback", methods=['POST'])
def callback():
    try:
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)
        handler.handle(body, signature)
    except Exception as e:
        app.logger.error("Error processing request: {}".format(e))
        abort(500)  # Return a 500 Internal Server Error response

    return 'OK'

# 接收訊息的路由
@handler.add(MessageEvent, message=TextMessage)
def reply_message(event):

    if '警鈴' in event.message.text.lower():
        message = [TextSendMessage(text='喔伊喔伊'),
        StickerSendMessage(
            package_id = '8525',
            sticker_id = '16581306'
        )]
        line_bot_api.reply_message(event.reply_token, message)

        call_rasp()

    if '開燈' in event.message.text.lower():
        message = [TextSendMessage(text='燈已開啟'),
        StickerSendMessage(
            package_id = '8522',
            sticker_id = '16581266'
        )]
        line_bot_api.reply_message(event.reply_token, message)
        turn_on()

    if '關閉' in event.message.text.lower():
        message = [TextSendMessage(text='已關閉'),
        StickerSendMessage(
            package_id = '11539',
            sticker_id = '52114113'
        )]
        line_bot_api.reply_message(event.reply_token, message)
        turn_off()

    if 'disconnect' in event.message.text.lower():
        message = [TextSendMessage(text='關閉連線中'),
        StickerSendMessage(
            package_id = '6359',
            sticker_id = '11069851'
        )]
        line_bot_api.reply_message(event.reply_token, message)

        # fps.stop()
        # print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        # print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        # do a bit of cleanup
        cv2.destroyAllWindows()
        # vs.stop()
        os._exit(0)

    if 'pir' in event.message.text.lower():
        message = [TextSendMessage(text='偵測中'),
        StickerSendMessage(
            package_id = '446',
            sticker_id = '2010'
        )]
        line_bot_api.reply_message(event.reply_token, message)
        pir_on()

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='無效指令')
        )



def upload_to_imgur(file_name, client_id):
    im = pyimgur.Imgur(client_id)
    uploaded_image = im.upload_image(file_name, title="Uploaded with PyImgur")
    return uploaded_image.link

# function for setting up emails
def send_message(name):
    return requests.post(
        "https://api.mailgun.net/v3/sandbox190a6b9d6bf844a080e7bdeef2d9a785.mailgun.org/messages",
        auth=("api", mailgun_api_key),
        files=[("attachment", ("image.jpg", open("image.jpg", "rb").read()))],
        data={"from": 'Uknowho@gmail.com',
              "to": ["matthew.in.ncu@g.ncu.edu.tw"],
              "subject": "You have a visitor",
              "html": "<html>" + name + " is at your door.  </html>"})

# Control GPIO
def call_rasp():
    ledpin = 13
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledpin, GPIO.OUT)

    pi_pwm = GPIO.PWM(ledpin, 100)
    pi_pwm.start(0)

    for _ in range(2):
        for duty in range(0, 101, 1):
            pi_pwm.ChangeDutyCycle(duty)
            sleep(0.01)
        sleep(1)

        for duty in range(100, -1, -1):
            pi_pwm.ChangeDutyCycle(duty)
            sleep(0.01)
        sleep(0.5)

    # GPIO.cleanup()

def turn_on():
    ledpin = 11
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledpin, GPIO.OUT)
    GPIO.output(ledpin, 1)



def turn_off():
    ledpin = 11
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(ledpin, GPIO.OUT)
    GPIO.output(ledpin, 0)
    GPIO.cleanup()

def pir_on():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(19, GPIO.IN) 

    last_message_time = 0 
    try:
        while True:
            i=GPIO.input(19)
            if i==0: #When output from motion sensor is LOW
                print("No intruders",i)

            elif i==1: #When output from motion sensor is HIGH
                current_time = time.time()
                if current_time - last_message_time >= 10:  # Check if at least 10 seconds have passed
                    print("Intruder detected", i)
                    line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', TextSendMessage(text='偵測到移動!!'))
                    last_message_time = current_time  # Update the last message time
                else:
                    print("Intruder detected, but waiting before sending another message")
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exception: KeyboardInterrupt")
    finally:
        GPIO.cleanup()


# function for facial recognition
def run_facial_recognition():
    # initialize the video stream and allow the camera sensor to warm up
    print("[INFO] starting video stream...")
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)

    # Initialize 'currentname' to trigger only when a new person is identified.
    currentname = "Unknown"
    face_count = 0
    last_email_time = 0
    unknown_count = 0
    # Determine faces from encodings.pickle file model created from train_model.py
    encodingsP = "encodings.pickle"
    # use this xml file
    cascade = "haarcascade_frontalface_default.xml"

    # load the known faces and embeddings along with OpenCV's Haar
    # cascade for face detection
    print("[INFO] loading encodings + face detector...")
    data = pickle.loads(open(encodingsP, "rb").read())
    detector = cv2.CascadeClassifier(cascade)

    # start the FPS counter
    fps = FPS().start()

    # loop over frames from the video file stream
    while True:
        # grab the frame from the threaded video stream and resize it
        # to 500px (to speedup processing)
        frame = vs.read()
        frame = imutils.resize(frame, width=500)

        # convert the input frame from (1) BGR to grayscale (for face
        # detection) and (2) from BGR to RGB (for face recognition)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(gray, scaleFactor=1.1,
                                          minNeighbors=5, minSize=(30, 30),
                                          flags=cv2.CASCADE_SCALE_IMAGE)

        # OpenCV returns bounding box coordinates in (x, y, w, h) order
        # but we need them in (top, right, bottom, left) order, so we
        # need to do a bit of reordering
        boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

        # compute the facial embeddings for each face bounding box
        encodings = face_recognition.face_encodings(rgb, boxes)
        names = []

        # loop over the facial embeddings
        for encoding in encodings:
            # attempt to match each face in the input image to our known
            # encodings
            matches = face_recognition.compare_faces(data["encodings"],
                                                     encoding)
            name = "Unknown"

            # check to see if we have found a match
            if True in matches:
                # find the indexes of all matched faces then initialize a
                # dictionary to count the total number of times each face
                # was matched
                matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                counts = {}
                unknown_count = 0

                # loop over the matched indexes and maintain a count for
                # each recognized face face
                for i in matchedIdxs:
                    name = data["names"][i]
                    counts[name] = counts.get(name, 0) + 1

                # determine the recognized face with the largest number
                # of votes (note: in the event of an unlikely tie Python
                # will select first entry in the dictionary)
                name = max(counts, key=counts.get)

                # update the list of names
                if currentname != name:
                    currentname = name
                    face_count = 1  # reset face_count whenever a new face is identified
                elif currentname == name:
                    face_count += 1  # increment face_count if the same face is identified again

                # If the same face has been identified for 10 frames, send an email
                if face_count > 10:
                    current_time = time.time()
                    if current_time - last_email_time > 30:  # check if at least XX seconds have passed
                        print(currentname)
                        # Take a picture to send in the email
                        img_name = "image.jpg"
                        cv2.imwrite(img_name, frame)
                        print('Taking a picture.')

                        # Now send me an email to let me know who is at the door
                        # call_rasp()
                        # request = send_message(name)
                        # print('Status Code: ' + format(request.status_code))  # 200 status code means email sent successfully
                        face_count = 0  # reset face_count after sending the email
                        last_email_time = current_time  # update the time the last email was sent

                        line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', TextSendMessage(text=currentname + '來囉'))
                        line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', StickerSendMessage(package_id=11537, sticker_id=52002738))
                        imgurl = upload_to_imgur('image.jpg', '33ba7dac79aee17')
                        line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', ImageSendMessage(original_content_url=imgurl, preview_image_url=imgurl))

            else:
                # If no faces are recognized, send an email
                current_time = time.time()
                if current_time - last_email_time > 30 and unknown_count > 20:  # check if at least XX seconds have passed
                    print("Unknown guy at the door")
                    # Take a picture to send in the email
                    img_name = "image.jpg"
                    cv2.imwrite(img_name, frame)
                    print('Taking a picture.')
                    # Now send me an email to let me know who is at the door
                    call_rasp()
                    request = send_message(name)
                    print('Status Code: ' + format(request.status_code))  # 200 status code means email sent successfully
                    unknown_count = 0
                    last_email_time = current_time  # update the time the last email was sent
                    line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', TextSendMessage('有陌生人來囉'))
                    line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', StickerSendMessage(package_id=446, sticker_id=2011))
                    imgurl = upload_to_imgur('image.jpg', '33ba7dac79aee17')
                    line_bot_api.push_message('Uf644275d87b924c7cb25b89d355a090e', ImageSendMessage(original_content_url=imgurl, preview_image_url=imgurl))

            # update the list of names
            names.append(name)
            if name == 'Unknown':
                unknown_count += 1
            else:
                unknown_count = 0

        # loop over the recognized faces
        for ((top, right, bottom, left), name) in zip(boxes, names):
            # draw the predicted face name on the image - color is in BGR
            cv2.rectangle(frame, (left, top), (right, bottom),
                          (0, 255, 225), 2)
            y = top - 15 if top - 15 > 15 else top + 15
            cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
                        .8, (0, 255, 255), 2)

        # display the image to our screen
        cv2.imshow("Facial Recognition is Running", frame)


        # update the FPS counter
        fps.update()

        # stop the timer and display FPS information
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            fps.stop()
            print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
            print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

            # do a bit of cleanup
            cv2.destroyAllWindows()
            vs.stop()
            sys.exit()


# threading for concurrent execution
t1 = threading.Thread(target=run_facial_recognition)
t2 = threading.Thread(target=app.run)

if __name__ == "__main__":
    t1.start()
    t2.start()