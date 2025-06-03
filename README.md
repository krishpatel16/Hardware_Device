# Hardware Device Project
This project demonstrates how to control an LED connected to a Raspberry Pi using local GPIO and remote MQTT messages via AWS IoT Core.

## File Structure
- **mqtt_led_control.py**
  - Connects the Raspberry Pi to AWS IoT Core using MQTT. Subscribes to a topic and turns the LED on or off (and sets intensity) based on received messages.

- **README.md**
  - This file. Explains the project, file structure, and setup instructions.

## Prerequisites
1. Raspberry Pi with Raspbian OS
2. Python 3 installed
3. An LED connected to GPIO pin 17 (with appropriate resistor)
4. AWS IoT Core account and a registered device (Thing)
5. AWS IoT device certificates (RaspberryPi.cert.pem, RaspberryPi.private.key, root-CA.crt)
6. Internet connection for the Raspberry Pi

## Installation
1. **Install Required Python Packages**
   ```sh
   pip install RPi.GPIO awscrt awsiot
   ```
2. **Prepare AWS IoT Certificates**
   Place AWS IoT device certificates in the project directory:
   - RaspberryPi.cert.pem
   - RaspberryPi.private.key
   - root-CA.crt
   Update the paths in `mqtt_led_control.py` if filenames differ.

3. **Wiring the LED**
   Connect the LED (with a resistor) to GPIO pin 17 and ground on your Raspberry Pi.

4. **Running the Script**
   The script will connect to AWS IoT Core and listen for messages on the `/smarthome/commands/led` topic.
   Send JSON messages (e.g., `{ "state": "on", "brightness": 80 }`) to control the LED.

5. **Stopping the Script**
   Press Ctrl+C in the terminal to stop the script. The GPIO pins will be cleaned up automatically.
