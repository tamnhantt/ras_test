import RPi.GPIO as GPIO
import time
from flask import Flask, request, jsonify
from flask_cors import CORS # type: ignore

# Cấu hình Flask
app = Flask(__name__)
CORS(app)

# Cấu hình GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)  # Chọn GPIO 18 làm output
pwm = GPIO.PWM(18, 1000)  # Tạo tín hiệu PWM với tần số 1kHz
pwm.start(0)  # Bắt đầu với duty cycle 0%

# Hàm chuyển đổi giá trị slider thành điện áp (0 - 3.3V)
def convert_to_voltage(value):
    min_slider = 1
    max_slider = 5
    min_voltage = 0.0
    max_voltage = 3.3

    voltage = ((value - min_slider) / (max_slider - min_slider)) * (max_voltage - min_voltage) + min_voltage
    return round(voltage, 2)

# API nhận dữ liệu từ Flutter
@app.route('/receive_data', methods=['POST'])
def receive_data():
    try:
        data = request.json
        sensor_name = data.get("sensorname")
        value = float(data.get("value"))

        # Chuyển đổi giá trị thành điện áp
        voltage = convert_to_voltage(value)
        duty_cycle = (voltage / 3.3) * 100  # Tính duty cycle cho PWM

        # Điều chỉnh tín hiệu PWM
        pwm.ChangeDutyCycle(duty_cycle)

        print(f"Sensor: {sensor_name} - Value: {value} - Voltage: {voltage}V - Duty Cycle: {duty_cycle}%")

        return jsonify({
            "status": "success",
            "message": f"Đã cập nhật tín hiệu PWM từ {sensor_name}",
            "voltage": voltage,
            "duty_cycle": duty_cycle
        }), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# API dừng chương trình và reset GPIO
@app.route('/shutdown', methods=['POST'])
def shutdown():
    pwm.stop()
    GPIO.cleanup()
    return jsonify({"status": "success", "message": "Hệ thống đã tắt và GPIO được reset"}), 200

# Khởi động server
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("\nStopping server...")
        pwm.stop()
        GPIO.cleanup()
