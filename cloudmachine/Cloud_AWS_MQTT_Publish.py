import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import mysql.connector
from datetime import datetime, timedelta

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("MyCloudComputer")
# myMQTTClient.configureEndpoint("YOUR.ENDPOINT", 8883)
myMQTTClient.configureEndpoint("ayjz49xxayi5a-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/ubuntu/cert/AmazonRootCA1.pem", "/home/ubuntu/cert/ba58412a7655078cd2e72279ce833edc6d43770e971ba3edb2ef21ea40e2aea1-private.pem.key", "/home/ubuntu/cert/ba58412a7655078cd2e72279ce833edc6d43770e971ba3edb2ef21ea40e2aea1-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
myMQTTClient.publish("cloud/info", "connected", 0)
#myMQTTClient.publish("xxxx/info", "connected", 0)

while 1:
    mydb = mysql.connector.connect(host="localhost",user="ubuntu",password="", database="assignment03")
    mycursor = mydb.cursor()
    now = datetime.now() + timedelta(hours=8)
    one_hour_before = now - timedelta(hours=1)
    now_str = now.strftime("%H:%M:%S")
    one_hour_before_str = one_hour_before.strftime("%H:%M:%S")

    mycursor.execute("SELECT rfid, DATE_FORMAT(start_time, '%%H:%%i:%%s') FROM booking_v1 WHERE capacity = 'andy_4' AND start_time between '%s' AND '%s'" %(one_hour_before_str,now_str))
    booking_table = mycursor.fetchall()
    print(booking_table)
    if (booking_table != None):
        booking_table = str(booking_table)
        myMQTTClient.publish("rpi/booking", booking_table, 0)

    mycursor.execute("SELECT rfid, DATE_FORMAT(start_time, '%%H:%%i:%%s') FROM booking_v1 WHERE capacity = 'sana_4' AND start_time between '%s' AND '%s'" %(one_hour_before_str,now_str))
    booking_table = mycursor.fetchall()
    print(booking_table)
    if (booking_table != None):
        booking_table = str(booking_table)
        myMQTTClient.publish("sana_4/booking", booking_table, 0)

    mycursor.execute("SELECT rfid, DATE_FORMAT(start_time, '%%H:%%i:%%s') FROM booking_v1 WHERE capacity = 'khalid_6' AND start_time between '%s' AND '%s'" %(one_hour_before_str,now_str))
    booking_table = mycursor.fetchall()
    print(booking_table)
    if (booking_table != None):
        booking_table = str(booking_table)
        myMQTTClient.publish("khalid_6/booking", booking_table, 0)

    mycursor.execute("SELECT rfid, DATE_FORMAT(start_time, '%%H:%%i:%%s') FROM booking_v1 WHERE capacity = 'mehrab_8' AND start_time between '%s' AND '%s'" %(one_hour_before_str,now_str))
    booking_table = mycursor.fetchall()
    print(booking_table)
    if (booking_table != None):
        booking_table = str(booking_table)
        myMQTTClient.publish("mehrab_8/booking", booking_table, 0)

    mycursor.close()
    
    time.sleep(5)  #Delay of 2 seconds
