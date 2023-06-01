import serial
import time
import mysql.connector

# Open serial port
ser = serial.Serial('/dev/ttyACM0', 9600)

# Connect to MySQL server
mydb = mysql.connector.connect(
    host="localhost",  # replace with your host
    user="khalid",  # replace with your username
    password="Mark2K23",  # replace with your password
    database="assignment03"  # replace with your database
)

mycursor = mydb.cursor()

# Create a new table named arduino_data
mycursor.execute("""
CREATE TABLE IF NOT EXISTS arduino_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp TIMESTAMP,
    rfid TEXT,
    ir_blaster_value FLOAT,
    temperature FLOAT,
    humidity FLOAT,
    desired_temperature FLOAT,
    desired_airflow FLOAT,
    noise_sensor_value INT,
    people_count INT,
    door_status TEXT
)
""")

# Initialize data dictionary
data = {}

def fetch_rfid_values():
    # Get all RFID values from the booking table
    mycursor.execute("SELECT rfid FROM booking")
    return [row[0] for row in mycursor.fetchall()]

def send_rfid_to_arduino():
    rfid_values = fetch_rfid_values()
    for rfid in rfid_values:
        # Send each RFID value to the Arduino via the serial port without "RFID:" prefix
        ser.write(f"{rfid}\n".encode())

# Define function to insert data into databas
def insert_data(data):
    try:
        sql = "INSERT INTO arduino_data (ir_blaster_value, temperature, humidity, desired_temperature, desired_airflow, noise_sensor_value, people_count, door_status, rfid) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        print(data)
        mycursor.execute(sql, tuple(data.values()))
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))

def noise_level(noise_value):
    # Define your own thresholds for noise levels
    if noise_value < 10:
        return 'low'
    elif 10 <= noise_value < 20:
        return 'medium'
    else:
        return 'high'

def temperature_level(temperature_value):
    # Define your own thresholds for temperature levels
    if temperature_value < 20:
        return 'low'
    elif 20 <= temperature_value < 30:
        return 'medium'
    else:
        return 'high'

def fetch_last_arduino_data():
    sql = """
    SELECT id, timestamp, rfid, ir_blaster_value, temperature, humidity, 
    desired_temperature, desired_airflow, noise_sensor_value, people_count, door_status 
    FROM arduino_data ORDER BY id DESC LIMIT 1
    """
    mycursor.execute(sql)
    result = mycursor.fetchone()
    if result:
        # Return a dictionary if a row is found
        columns = [i[0] for i in mycursor.description]
        return dict(zip(columns, result))
    else:
        # Return None if no row is found
        return None


def update_room_status(data):
    try:
        sql = "INSERT INTO room_status (count, noise, temperature) VALUES (%s, %s, %s)"
        values = (data['people_count'], noise_level(data['noise_sensor_value']), temperature_level(data['temperature']))
        mycursor.execute(sql, values)
        mydb.commit()
        print("Room status inserted.")
    except mysql.connector.Error as err:
        print("Something went wrong: {}".format(err))


while True:
    try:
        read_serial = ser.readline().decode('utf-8').strip()  # read a '\n' terminated line
        if ":" in read_serial:  # assuming all sensor readings contain ':'
            key, value = read_serial.split(':')
            # Cast people_count to int if possible
            if key == 'people_count':
                try:
                    value = int(value)
                except ValueError:
                    pass  # Ignore the value if it cannot be casted to int
            data[key] = value

        if 'RFID card detected' in data:
            rfid_value = data.get('RFID card detected')
            rfid_values = fetch_rfid_values()
            print("rfid_value:", rfid_value)
            print("rfid_values:", rfid_values)
            if rfid_value in rfid_values:
                print("Data before insertion:", data)  # Debug line
                data['rfid'] = data.pop('RFID card detected')  # Change the key from 'RFID card detected' to 'rfid'
                insert_data(data)
                update_room_status(fetch_last_arduino_data())
                data = {}  # reset the data dictionary after insertion
            else:
                print(f"RFID {rfid_value} is not in the booking table.")
                send_rfid_to_arduino()  # Sending all RFID values to the Arduino
    except Exception as e:
        print(f"Error: {str(e)}")