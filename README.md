## Overview

This is a simple project to demonstrate how to use the Raspberry Pi 4 to control LED nights and using facial recognition to identify the person in front of the camera. The whole project is controlled by Line chatbot. It will send messages to the user if there are any visitors (recognized). The user can also control the LED lights by sending messages to the chatbot. When there's a stranger (unrecognized), the buzzer will be triggered and the user will receive a message from the chatbot. 

## Demo Video

![Demo video]()

## Components
### Hardware

- Raspberry Pi 4
- Raspberry Pi Camera
- LED lights
- Breadboard
- Jumper wires
- Buzzer
- PIR sensor


### Software

- Python 3.7
- OpenCV
- Line chatbot
- ngrok
- mailgun

## Instructions

### Step 1. Hardware Setup

Here is the circuit diagram for the hardware setup.

![circuit diagram](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/circuit.png)

> The LED lights are connected to GPIO 11, 13. The buzzer is in Parallel Circuit with Red LEDs. The PIR sensor is connected to GPIO 2(power) and 19(signal). Remember to insert your pi camera into the pi.

\
<br>

### Step 2. Set up Line chatbot & ngrok

**I strongly recommend running with `python 3`**, it cause some problems when I run with python 2. When pip installing in the following step, **use `pip3` instead of pip**.

1. Follow the instructions in this [tutorial](https://hackmd.io/@Xiugapurin/S1siaZwht) to set up your Line chatbot and ngrok.

2. Set up the environment variables (`export` didn't work for me, so...)
```shell
sudo nano /etc/environment
```
Add the following lines to the file and save it. (Ctrl+X, Y, Enter)
```shell
LINE_CHANNEL_SECRET=your_line_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
```
For me, I had to add this in the python file as well. Put it in the first line! (You dno't have to do these following two if you're going to use my code)
```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
```
Adjust this line to send images and stickers
```python
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, StickerSendMessage, ImageSendMessage
```  

\
<br>

### Step 3. Facial Recognition

1. Install dependencies
```shell
pip3 install --upgrade pip setuptools wheel
pip3 install opencv-python==4.7.0.72
```

2. Follow every steps in this [tutorial](https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition#:~:text=Part%201%3A%20Install%20Dependencies%20for%20Raspberry%20Pi%20Facial,5.%20Install%20face_recognition.%20...%206%206.%20Install%20imutils) to set up the model and email. It's the most difficult part... Remember to use `pip3` instead of `pip`! 

If you want to send emails, add another environment variable in `/etc/environment` file.
```shell
MAILGUN_API_KEY=your_mailgun_api_key
```

\
<br>

### Step 4. Run the program

1. Clone this repository
```shell
git clone https://github.com/Matthew-HMS/Patrol-night-light.git
```

2. Run the program (The python file must be in the same directory with the `pickle` file generated in the previous step)
```shell
sudo -E python3 run.py
```

\
<br>

### Step 5. Set up Motion (Optional)

If you want to use the pi camera to detect motion, you can follow this [tutorial](https://pimylifeup.com/raspberry-pi-webcam-server/). It's very easy to set up. Remember to change the port number to 8081 in the `motion.conf` file.











\
\
<br>


## References

- [Raspberry Pi Webcam Server](https://pimylifeup.com/raspberry-pi-webcam-server/)
- Line chatbot
    - [Set up Line chatbot](https://hackmd.io/@Xiugapurin/S1siaZwht)
    - [Line developers](https://developers.line.biz/en/)
    - [ngrok](https://ngrok.com/)

- [Face Recognition]
    - [opencv-python install tutorial](https://raspberrytips.com/install-opencv-on-raspberry-pi/)
    - [Raspberry Pi for Facial Recognition](https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition#:~:text=Part%201%3A%20Install%20Dependencies%20for%20Raspberry%20Pi%20Facial,5.%20Install%20face_recognition.%20...%206%206.%20Install%20imutils)

