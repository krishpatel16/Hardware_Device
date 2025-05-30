import sys
import threading
import time
import RPi.GPIO as GPIO

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

# Set up GPIO
LED_PIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

# AWS IoT Core endpoint and certs
endpoint = "a23kp0hoi8uuhr-ats.iot.eu-west-2.amazonaws.com"
cert_filepath = "RaspberryPi.cert.pem"
key_filepath = "RaspberryPi.private.key"
ca_filepath = "root-CA.crt"
client_id = "basicPubSub"
topic = "/smarthome/commands/led"

# MQTT connection
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

def on_message_received(topic, payload, dup, qos, retain, **kwargs):
    message = payload.decode("utf-8").strip().lower()
    print(f"Received message on topic '{topic}': {message}")
    
    if message == "on":
        GPIO.output(LED_PIN, GPIO.HIGH)
        print("LED turned ON")
    elif message == "off":
        GPIO.output(LED_PIN, GPIO.LOW)
        print("LED turned OFF")

def main():
    print(f"Connecting to {endpoint} with client ID '{client_id}'...")
    connect_future = mqtt_connection.connect()
    connect_future.result()
    print("Connected!")

    print(f"Subscribing to topic '{topic}'...")
    subscribe_future, _ = mqtt_connection.subscribe(
        topic=topic,
        qos=mqtt.QoS.AT_LEAST_ONCE,
        callback=on_message_received
    )
    subscribe_future.result()
    print(f"Subscribed to '{topic}'")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Disconnecting...")
    finally:
        mqtt_connection.disconnect()
        GPIO.cleanup()

if __name__ == "__main__":
    main()
