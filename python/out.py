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
    min_slider = 0
    max_slider = 5
    min_voltage = 0.0
    max_voltage = 3.3

    voltage = ((value - min_slider) / (max_slider - min_slider)) * (max_voltage - min_voltage) + min_voltage
    return round(voltage, 2)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python backend.py <sensor_name> <value>")
        sys.exit(1)

    sensor_name = sys.argv[1]
    try:
        value = float(sys.argv[2])
        voltage = convert_to_voltage(value)
        duty_cycle = (voltage / 3.3) * 100  # Chuyển điện áp thành duty cycle (%)

        # Cập nhật PWM theo giá trị mới
        pwm.ChangeDutyCycle(duty_cycle)
        
        print(f"Sensor: {sensor_name} - Value: {value} - Voltage: {voltage}V")
    except ValueError:
        print("Invalid input. Expected a numeric value for <value>.")
    
    time.sleep(0.1)  # Giảm tải CPU
    
    # Dừng PWM và giải phóng GPIO
    pwm.stop()
    GPIO.cleanup()
