import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import mysql.connector

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("MyRPI")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("ayjz49xxayi5a-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/AndyPi/cert/AmazonRootCA1.pem", "/home/AndyPi/cert/86fa8df62ffea71a3165fbc140a512a34b048405d4ee9ef9aabc22b58a7f620f-private.pem.key", "/home/AndyPi/cert/86fa8df62ffea71a3165fbc140a512a34b048405d4ee9ef9aabc22b58a7f620f-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

def customCallback(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    booking_table_str = message.payload[:-1]
    value_list = booking_table_str.split(",")
    mydb = mysql.connector.connect(host="localhost",user="AndyPi",password="PiAndy", database="assignment03")
    mycursor = mydb.cursor()
    mycursor.execute("TRUNCATE TABLE booking")
    i = 0
    while i < (len(value_list)):
        rfid=value_list[i][2:]
        i=i+1
        start_time=value_list[i][1:-1]
        i=i+1
        print(rfid)
        print(start_time)
        mycursor.execute("INSERT INTO booking (rfid, start_time) VALUES (%s, %s)" %(rfid,start_time))
        mydb.commit()
    mycursor.close()

# Connect and subscribe to AWS IoT
myMQTTClient.connect()
myMQTTClient.subscribe("rpi/booking", 1, customCallback)

while True:
    time.sleep(1)