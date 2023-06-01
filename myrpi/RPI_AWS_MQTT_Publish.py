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

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("rpi/info", "connected", 0)
#myMQTTClient.publish("xxxx/info", "connected", 0)

while 1:
    mydb = mysql.connector.connect(host="localhost",user="AndyPi",password="PiAndy", database="assignment03")
    with mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count,noise,temperature FROM room_status ORDER BY id DESC LIMIT 1")
        room_status = mycursor.fetchone()
        room_status = str(room_status)
        mycursor.close()
        
    print (room_status)
    myMQTTClient.publish("rpi/data", room_status, 0)
    
    time.sleep(5)  #Delay of 2 seconds