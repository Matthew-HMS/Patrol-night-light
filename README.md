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

## Instructions

### Step 1. Hardware Setup

Here is the circuit diagram for the hardware setup.

![circuit diagram](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/circuit.png)

> The LED lights are connected to GPIO 11, 13. The buzzer is in Parallel Circuit with Red LEDs. The PIR sensor is connected to GPIO 2(power) and 19(signal). Remember to insert your pi camera into the pi.

### Step 2. Set up Line chatbot & ngrok

**I strongly recommend runing with `python 3`**, it cause some problems when I run with python 2. When pip installing in the following step, **use `pip3` instead of pip**.

1. Follow the instructions in this [tutorial](https://hackmd.io/@Xiugapurin/S1siaZwht) to set up your Line chatbot and ngrok.

2. Set up the environment variables (`export` didn't work for me, so...)
```shell
sudo nano /etc/environment
```
Add the following lines to the file
```shell
LINE_CHANNEL_SECRET=your_line_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
```
For me, I had to add this in the file as well (Put it in the first line!)
```python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
```
Adjust this line to send images and stickers
```python
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageMessage, StickerSendMessage, ImageSendMessage
```

### Step 3. Facial Recognition


### Step 4. Run the program

```shell
sudo -E python3 run.py
```

### Step 5. Set up Motion












## References

- [Raspberry Pi Webcam Server](https://pimylifeup.com/raspberry-pi-webcam-server/)
- Line chatbot
    - [Set up Line chatbot](https://hackmd.io/@Xiugapurin/S1siaZwht)
    - [Line developers](https://developers.line.biz/en/)
    - [ngrok](https://ngrok.com/)



- [Raspberry Pi for Facial Recognition](https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition#:~:text=Part%201%3A%20Install%20Dependencies%20for%20Raspberry%20Pi%20Facial,5.%20Install%20face_recognition.%20...%206%206.%20Install%20imutils)

