import serial
import time

class UART:
    def __init__(self, port="COM11", baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            print(f"✅ Connected to {port} at {baudrate} baud")
            time.sleep(2)  # Give STM32 time to initialize UART
        except serial.SerialException as e:
            print(f"❌ Error: Could not open {port}. {e}")

    def send_data(self, data):
        """ Send strain rate data to STM32 via UART """
        if isinstance(data, float):
            data_str = f"{data:.2f}"  # Format float with two decimals
        else:
            data_str = str(data)

        if self.ser.is_open:
            self.ser.write(data_str.encode())  # Send data
            print(f"📤 Sent: {data_str.strip()}")  # Debug output
        else:
            print("❌ Error: Serial port is not open")

    def receive_data(self):
        """ Receive response from STM32 """
        if self.ser.is_open:
            response_bytes = self.ser.readline()
            filtered_bytes = response_bytes.replace(b'\x00',b'')
            response= filtered_bytes.decode().strip()
            if response:
                print(f"📥 Received: {response}")  # Debug output
            return response
        else:
            print("❌ Error: Serial port is not open")
            return ""

    def close(self):
        """ Close UART connection """
        if self.ser.is_open:
            self.ser.close()
            print("🔌 Serial port closed")

