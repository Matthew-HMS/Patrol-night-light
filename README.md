## Overview

This is a simple project to demonstrate how to use the Raspberry Pi 4 to control LED nights and using facial recognition to identify the person in front of the camera. The whole project is controlled by Line chatbot. It will send messages to the user if there are any visitors (recognized). When there's a stranger (unrecognized), the buzzer will be triggered and the user will receive a message from the chatbot. The user can control the whole system by sending messages to the chatbot.

<br>

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

<br>

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
Add the following lines to the file, change it to your secret, token and id then save it. (Ctrl+X, Y, Enter)
```shell
LINE_CHANNEL_SECRET=your_line_channel_secret
LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
LINE_USER_ID=your_line_user_id
```
You have to reboot the pi to make it work when you add an environment variable !
```shell
sudo reboot
```
Check if the environment variables are set correctly.
```shell
printenv
```  

3. Add Imgur Service
```shell
pip3 install pyimgur
```
Follow the tutorial in this [link](https://ithelp.ithome.com.tw/articles/10241006) to set up your Imgur account and get your client id. Then add it to the environment variables as well.
```shell
sudo nano /etc/environment
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
sudo nano /etc/environment
```
Add your mailgun api key to the file, then save it. (Ctrl+X, Y, Enter)
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

Follow the instructions in this [tutorial](https://pimylifeup.com/raspberry-pi-webcam-server/) to set up the Motion. Remember to enable the camera in the `raspi-config` file.

When Motion is on, it will occupy the camera's resource. So you can't use the Motion and `run.py` at the same time. However, the Motion will automatically turn on when you reboot the pi.

Turn it off by typing this in the terminal.
>⚠️ **You have to turn it off before running the `run.py` file.**
```shell
sudo systemctl stop motion
```

Turn it on by typing this in the terminal.
```shell
sudo systemctl start motion
```
Go here to see the streaming. (within the same network)
```shell
http://your_pi_ip:8081
```

<br>

I recommend setting `movie_output on` but `picture_output off`in the `motion.conf` file. It will record a video when there's a motion detected, and won't take pictures. It might cause some lags on streaming though.
```shell
sudo nano /etc/motion/motion.conf
```
You can find the .mp4 files in `/motion` directory.
```shell
cd /motion
```
And that's it! You can now control the system by sending messages to the chatbot.

\
\
<br>

## How to use

1. Send `help` to the chatbot to see the instructions.

![help](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/help.png)

2. Send `開燈` to turn on the Yellow LED lights.

![light](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/light.png)

3. Send `pir` to turn on the PIR sensor. (It will send a message to the user as long as there's a motion detected) 

![pir](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/pir.png)

4. Send `關閉` to turn off the Yellow LED lights and PIR sensor.

![off](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/stop.png)

5. Send `警鈴` to test the alert system. (Trigger the buzzer and Red LEDs)

![ring](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/ring.png)

6. Send `disconnect` to stop the program.

![disconnect](https://github.com/Matthew-HMS/Patrol-night-light/blob/main/readme_img/disconnect.png)

\
\
<br>

## References

- Line chatbot
    - [Set up Line chatbot](https://hackmd.io/@Xiugapurin/S1siaZwht)
    - [Line developers](https://developers.line.biz/en/)
    - [ngrok](https://ngrok.com/)
    - [Imgur set up](https://ithelp.ithome.com.tw/articles/10241006)
    - [Line Push Message](https://ithelp.ithome.com.tw/articles/10337875)

- Face Recognition
    - [opencv-python install tutorial](https://raspberrytips.com/install-opencv-on-raspberry-pi/)
    - [Raspberry Pi for Facial Recognition](https://www.tomshardware.com/how-to/raspberry-pi-facial-recognition#:~:text=Part%201%3A%20Install%20Dependencies%20for%20Raspberry%20Pi%20Facial,5.%20Install%20face_recognition.%20...%206%206.%20Install%20imutils)
    - [Mailgun](https://www.mailgun.com/)

- [Raspberry Pi Webcam Server](https://pimylifeup.com/raspberry-pi-webcam-server/)

- [GPIO Pinout](https://pinout.xyz/)


