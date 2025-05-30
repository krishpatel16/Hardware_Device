import RPi.GPIO as GPIO
import time
import globals

LED_PIN = 17 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(LED_PIN, GPIO.OUT)

pwm_led = GPIO.PWM(LED_PIN, 100)  # Initialize PWM on the LED pin with a frequency of 100 Hz
pwm_led.start(0)  # Start PWM with a duty cycle of 0 (LED off initially)

globals.led_start_time = time.time()
print(f"Script started at: {time.ctime(globals.led_start_time)}.")

def led():
    current_time = int(time.time())
    elapsed_time = current_time - globals.led_start_time
    print(f"Elapsed time: {elapsed_time:.2f} seconds.", end='\r')

    if 5 >= elapsed_time >= 1:
        # Gradually increase intensity using PWM
        duty_cycle = int((elapsed_time - 1) / 4 * 100)  # Map 1-5 seconds to 0-100% duty cycle
        if 0 <= duty_cycle <= 100:
            pwm_led.ChangeDutyCycle(duty_cycle)
            print(f"LED intensity: {duty_cycle}% (1-5 seconds) at {time.ctime()}.", end='\r')
    elif 12 >= elapsed_time > 7:
        pwm_led.ChangeDutyCycle(0)  # Turn off LED using PWM (duty cycle 0)
        print(f"LED is OFF (7-12 seconds) at {time.ctime()}.", end='\r')
    else:
        pwm_led.ChangeDutyCycle(0)  # Turn off LED using PWM (duty cycle 0)
        print(f"LED is OFF (outside intervals) at {time.ctime()}.", end='\r')

if __name__ == "__main__":
    try:
        while True:
            led()
            time.sleep(0.1)
    finally:
        pwm_led.stop()  # Stop PWM
        GPIO.cleanup()
        print("\nPWM stopped and GPIO cleanup done.")
