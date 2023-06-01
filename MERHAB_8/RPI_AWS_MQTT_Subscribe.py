import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import mysql.connector

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("MERHAB_8")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("ayjz49xxayi5a-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/mehrab/cert/AmazonRootCA1.pem", "/home/mehrab/cert/0ac40abe638f614788ccab48b2eda9be4bb559b3c638aa6728447d2613edf473-private.pem.key", "/home/mehrab/cert/0ac40abe638f614788ccab48b2eda9be4bb559b3c638aa6728447d2613edf473-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

def customCallback(client, userdata, message):
    message.payload = message.payload.decode("utf-8")
    booking_table_str = message.payload[:-1]
    value_list = booking_table_str.split(",")
    mydb = mysql.connector.connect(host="localhost",user="mehrab",password="rasbery", database="assignment03")
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
myMQTTClient.subscribe("mehrab_8/booking", 1, customCallback)

while True:
    time.sleep(1)