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

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("merhab_8/info", "connected", 0)
#myMQTTClient.publish("xxxx/info", "connected", 0)

while 1:
    
    mydb = mysql.connector.connect(host="localhost",user="mehrab",password="rasbery", database="assignment03")
    with mydb:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT rfid, people_count, door_status FROM arduino_data ORDER BY id DESC LIMIT 1")
        latest_data = mycursor.fetchone()
        latest_data_str = str(latest_data)
        
    print (latest_data_str)
    myMQTTClient.publish("merhab_8/data", latest_data_str, 0)
    
    time.sleep(5)  #Delay of 2 seconds