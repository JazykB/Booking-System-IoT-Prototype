import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import mysql.connector

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("sana_4")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("ayjz49xxayi5a-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/sana/certs/AmazonRootCA1.pem", "/home/sana/certs/43f7bb1ccc6be0d97f3685a9a96e3fc2c678966ba6c5b570b5f8712ac8511ab9-private.pem.key", "/home/sana/certs/43f7bb1ccc6be0d97f3685a9a96e3fc2c678966ba6c5b570b5f8712ac8511ab9-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

def customCallback(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    booking_table_str = message.payload[:-1]
    value_list = booking_table_str.split(",")
    mydb = mysql.connector.connect(host="localhost",user="sana",password="sana2001", database="assignment03")
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
myMQTTClient.subscribe("sana_4/booking", 1, customCallback)

while True:
    time.sleep(1)