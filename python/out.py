from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Cấu hình GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
pwm = GPIO.PWM(18, 1000)  # Tạo tín hiệu PWM với tần số 1kHz
pwm.start(0)

def convert_to_voltage(value):
    min_slider, max_slider = 1, 5
    min_voltage, max_voltage = 0.0, 3.3
    voltage = ((value - min_slider) / (max_slider - min_slider)) * (max_voltage - min_voltage) + min_voltage
    return round(voltage, 2)

@app.route('/update_pwm', methods=['POST'])
def update_pwm():
    try:
        data = request.get_json()
        sensor_name = data.get("sensor_name")
        value = float(data.get("value"))

        voltage = convert_to_voltage(value)
        duty_cycle = (voltage / 3.3) * 100
        pwm.ChangeDutyCycle(duty_cycle)

        response = {
            "sensor": sensor_name,
            "value": value,
            "voltage": voltage,
            "status": "success"
        }
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000, debug=True)
    except KeyboardInterrupt:
        print("Stopping server...")
        pwm.stop()
        GPIO.cleanup()
