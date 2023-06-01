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

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("sana_4/info", "connected", 0)
#myMQTTClient.publish("xxxx/info", "connected", 0)

while 1:
    mydb = mysql.connector.connect(host="localhost",user="sana",password="sana2001", database="assignment03")
    with mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count,noise,temperature FROM room_status ORDER BY id DESC LIMIT 1")
        room_status = mycursor.fetchone()
        room_status = str(room_status)
        mycursor.close()
        
    print (room_status)
    myMQTTClient.publish("sana_4/data", room_status, 0)
    
    time.sleep(5)  #Delay of 2 seconds