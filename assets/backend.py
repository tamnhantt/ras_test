import sys

def process_sensor_data(sensor, value):
    print(f"Received data - {sensor}: {value}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python backend.py <sensor_name> <value>")
        sys.exit(1)

    sensor_name = sys.argv[1]
    value = sys.argv[2]

    process_sensor_data(sensor_name, value)
