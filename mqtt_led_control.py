import sys
import threading
import time
import json
import RPi.GPIO as GPIO

GPIO.setwarnings(False) 

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

LED_PIN = 13 #PWM pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)


pwm_led = GPIO.PWM(LED_PIN, 100)
pwm_led.start(0) 



endpoint = "a23kp0hoi8uuhr-ats.iot.eu-west-2.amazonaws.com"
cert_filepath = "RaspberryPi.cert.pem" 
key_filepath = "RaspberryPi.private.key" 
ca_filepath = "root-CA.crt" 
client_id = "basicPubSub"
topic = "smarthome/commands/led"


# MQTT connection setup
event_loop_group = io.EventLoopGroup(1)
host_resolver = io.DefaultHostResolver(event_loop_group)
client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
mqtt_connection = mqtt_connection_builder.mtls_from_path(
    endpoint=endpoint,
    cert_filepath=cert_filepath,
    pri_key_filepath=key_filepath,
    client_bootstrap=client_bootstrap,
    ca_filepath=ca_filepath,
    client_id=client_id,
    clean_session=False,
    keep_alive_secs=6
)

# Callback to handle incoming messages
def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    
    try:
        data = json.loads(payload.decode("utf-8"))
        state = data.get("state", "").strip().upper()
        brightness = data.get("brightness", 0)


        try:
            brightness = int(brightness)
            if not 0 <= brightness <= 100:
                
                brightness = max(0, min(100, brightness)) # Clamp value
        except ValueError:
            
            brightness = 0

        print(f"Parsed state: {state}, Brightness: {brightness}%.")

        if state == "ON":
            print(f"Attempting to set LED duty cycle to {brightness}%.")
            pwm_led.ChangeDutyCycle(brightness)
            print(f"LED set to {brightness}% brightness.")
        elif state == "OFF":
            print("Attempting to turn LED OFF (duty cycle 0%).")
            pwm_led.ChangeDutyCycle(0) 
            print("LED turned OFF.")
        else:
            print(f"Unknown state received: {state}. LED remains as is..")

    except json.JSONDecodeError:
        print(f"Error: Invalid JSON payload received: {payload.decode('utf-8')}.")
    except Exception as e:
        print(f"An unexpected error occurred in on_message_received: {e}.")

# Main MQTT handling
def main():
    print(f"Connecting to {endpoint} with client ID '{client_id}'...")
    connect_future = mqtt_connection.connect()
    try:
        connect_future.result(timeout=10)
        print("Connected! in Norwich.")
    except Exception as e:
        print(f"Connection failed: {e}.")
        sys.exit(1) 

    print(f"Subscribing to topic '{topic}' ...")
    subscribe_future, _ = mqtt_connection.subscribe(
        topic=topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )
    try:
        subscribe_future.result(timeout=10)
        print(f"Subscribed to '{topic}'.")
    except Exception as e:
        print(f"Subscription failed: {e}.")
        sys.exit(1) 

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
    finally:
        pwm_led.stop()
        mqtt_connection.disconnect()
        GPIO.cleanup()
        print("PWM stopped, MQTT client disconnected, GPIO cleanup done.")

if __name__ == "__main__":
    main()