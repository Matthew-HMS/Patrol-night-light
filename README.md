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

- Python 3
- OpenCV
- Line chatbot
- ngrok

## Instructions

### Step 1. Hardware Setup

Here is the circuit diagram for the hardware setup.

![circuit diagram]()

> **Note:** The LED lights are connected to GPIO 11, 13. The buzzer is in series circuit with Red LEDs. The PIR sensor is connected to GPIO 2(power) and 19(signal). Remember to insert your pi camera into the pi.
### Step 2. Install Dependencies













## References

- [Raspberry Pi Webcam Server](https://pimylifeup.com/raspberry-pi-webcam-server/)
