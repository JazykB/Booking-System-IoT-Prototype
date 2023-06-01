import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import mysql.connector


# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("KHALID_6")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("ayjz49xxayi5a-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/khalid/cert/AmazonRootCA1.pem", "/home/khalid/cert/d7e6edba8fde2e245374d098ac9b5b20406e7f2482059747eb5307306454f92f-private.pem.key", "/home/khalid/cert/d7e6edba8fde2e245374d098ac9b5b20406e7f2482059747eb5307306454f92f-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("khalid_6/info", "connected", 0)
#myMQTTClient.publish("xxxx/info", "connected", 0)

while 1:
    mydb = mysql.connector.connect(host="localhost",user="khalid",password="Mark2K23", database="assignment03")
    with mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count,noise,temperature FROM room_status ORDER BY id DESC LIMIT 1")
        room_status = mycursor.fetchone()
        room_status = str(room_status)
        mycursor.close()
        
    print (room_status)
    myMQTTClient.publish("khalid_6/data", room_status, 0)
    
    time.sleep(5)  #Delay of 2 seconds