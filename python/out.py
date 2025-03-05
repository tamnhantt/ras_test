import sys
import RPi.GPIO as GPIO 
import time

# Cấu hình GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # Chọn GPIO 18 làm output
pwm = GPIO.PWM(18, 1000)  # Tạo tín hiệu PWM tần số 1kHz
pwm.start(0)

# Hàm chuyển đổi giá trị từ slider thành điện áp (0-3.3V)
def convert_to_voltage(value):
    min_slider = 1
    max_slider = 5
    min_voltage = 0.0
    max_voltage = 3.3

    voltage = ((value - min_slider) / (max_slider - min_slider)) * (max_voltage - min_voltage) + min_voltage
    return round(voltage, 2)

# Nhận dữ liệu từ stdin để chạy liên tục
try:
    print("Listening for data...")
    while True:
        line = sys.stdin.readline().strip()
        if not line:
            continue

        try:
            sensor_name, value = line.split()
            value = float(value)

            voltage = convert_to_voltage(value)
            duty_cycle = (voltage / 3.3) * 100  # Chuyển điện áp thành duty cycle (%)

            # Cập nhật PWM theo giá trị mới
            pwm.ChangeDutyCycle(duty_cycle)

            print(f"Sensor: {sensor_name} - Value: {value} - Voltage: {voltage}V")

        except ValueError:
            print("Invalid input format. Expected: <sensor_name> <value>")
        time.sleep(0.1)  # Giảm tải CPU

except KeyboardInterrupt:
    print("\nStopping...")
    pwm.stop()
    GPIO.cleanup()
