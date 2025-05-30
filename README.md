# Hardware Device Project
This project demonstrates how to control an LED connected to a Raspberry Pi using both local GPIO control and remote MQTT messages via AWS IoT Core.

## File Structure 
1. mqtt_led_control.py
Connects the Raspberry Pi to AWS IoT Core using MQTT. It subscribes to a topic and turns the LED on or off based on received messages.

2. GPIO_LED.py
Controls the LED locally using PWM (Pulse Width Modulation) to adjust its brightness over time. It uses a global variable to track the start time and changes the LED’s intensity based on elapsed time.

3. globals.py
Stores global variables, such as the LED start time, for use across scripts.

4. README.md
This file. Explains the project, file structure, and setup instructions.

### Setup Instructions

## Prerequisites
1. Raspberry Pi with Raspbian OS
2. Python 3 installed
3. An LED connected to GPIO pin 17 (with appropriate resistor)
4. AWS IoT Core account and a registered device (Thing)
5. AWS IoT device certificates (RaspberryPi.cert.pem, RaspberryPi.private.key, root-CA.crt)
6. Internet connection for the Raspberry Pi


### Installation
1. **Install Required Python Packages**
Open a terminal and run:
pip install RPi.GPIO awscrt awsiot

2. **Prepare AWS IoT Certificates**
Place AWS IoT device certificates in the project directory:
    RaspberryPi.cert.pem
    RaspberryPi.private.key
    root-CA.crt
Update the paths in mqtt_led_control.py if filenames differ.

3. **Wiring the LED**
Connect the LED (with a resistor) to GPIO pin 17 and ground on your Raspberry Pi.

4. **Running the Scripts**
The script will connect to AWS IoT Core and listen for messages on the /smarthome/commands/led topic.
Send "on" or "off" messages to this topic to control the LED.

5. **Stopping the Scripts**
Press Ctrl+C in the terminal to stop either script. The GPIO pins will be cleaned up automatically.
