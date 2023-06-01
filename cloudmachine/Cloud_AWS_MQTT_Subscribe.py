from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import mysql.connector
from datetime import datetime, timedelta

# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("MyCloudComputer")
myMQTTClient.configureEndpoint("ayjz49xxayi5a-ats.iot.ap-southeast-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/ubuntu/cert/AmazonRootCA1.pem", "/home/ubuntu/cert/ba58412a7655078cd2e72279ce833edc6d43770e971ba3edb2ef21ea40e2aea1-private.pem.key", "/home/ubuntu/cert/ba58412a7655078cd2e72279ce833edc6d43770e971ba3edb2ef21ea40e2aea1-certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Custom MQTT message callback
def customCallback(client, userdata, message):
    # print("Received a new message: ")
    # print(message.payload)
    # print("from topic: ")
    # print(message.topic)
    # print("--------------\n\n")
    message.payload = message.payload.decode("utf-8")
    print(message.payload)
    value_list = message.payload.split(",")
    people = value_list[0][2:-1]
    people = int(people)
    noise = value_list[1][1:]
    temperature = value_list[2][1:-1]
    mydb = mysql.connector.connect(host="localhost",user="ubuntu",password="", database="assignment03")
    mycursor = mydb.cursor()
    now = datetime.now() + timedelta(hours=8)
    one_hour_before = now - timedelta(hours=1)
    now_str = now.strftime("%H:%M:%S")
    one_hour_before_str = one_hour_before.strftime("%H:%M:%S")
    mycursor.execute("SELECT * from booking_v1 WHERE capacity = 'andy_4' AND start_time between '%s' AND '%s' LIMIT 1" %(one_hour_before_str,now_str))
    result = mycursor.fetchone()
    if (result is not None):
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'andy_4'" %('yes',people,noise,temperature))
    else:
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'andy_4'" %('no',people,noise,temperature))
    mydb.commit()

def customCallbackSana_4(client, userdata, message):
    # print("Received a new message: ")
    # print(message.payload)
    # print("from topic: ")
    # print(message.topic)
    # print("--------------\n\n")
    message.payload = message.payload.decode("utf-8")
    print(message.payload)
    value_list = message.payload.split(",")
    people = value_list[0][2:-1]
    people = int(people)
    noise = value_list[1][1:]
    temperature = value_list[2][1:-1]
    mydb = mysql.connector.connect(host="localhost",user="ubuntu",password="", database="assignment03")
    mycursor = mydb.cursor()
    now = datetime.now() + timedelta(hours=8)
    one_hour_before = now - timedelta(hours=1)
    now_str = now.strftime("%H:%M:%S")
    one_hour_before_str = one_hour_before.strftime("%H:%M:%S")
    mycursor.execute("SELECT * from booking_v1 WHERE capacity = 'sana_4' AND start_time between '%s' AND '%s' LIMIT 1" %(one_hour_before_str,now_str))
    result = mycursor.fetchone()
    if (result is not None):
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'sana_4'" %('yes',people,noise,temperature))
    else:
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'sana_4'" %('no',people,noise,temperature))
    mydb.commit()

def customCallbackKhalid_6(client, userdata, message):
    # print("Received a new message: ")
    # print(message.payload)
    # print("from topic: ")
    # print(message.topic)
    # print("--------------\n\n")
    message.payload = message.payload.decode("utf-8")
    print(message.payload)
    value_list = message.payload.split(",")
    people = value_list[0][2:-1]
    people = int(people)
    noise = value_list[1][1:]
    temperature = value_list[2][1:-1]
    mydb = mysql.connector.connect(host="localhost",user="ubuntu",password="", database="assignment03")
    mycursor = mydb.cursor()
    now = datetime.now() + timedelta(hours=8)
    one_hour_before = now - timedelta(hours=1)
    now_str = now.strftime("%H:%M:%S")
    one_hour_before_str = one_hour_before.strftime("%H:%M:%S")
    mycursor.execute("SELECT * from booking_v1 WHERE capacity = 'khalid_6' AND start_time between '%s' AND '%s' LIMIT 1" %(one_hour_before_str,now_str))
    result = mycursor.fetchone()
    if (result is not None):
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'khalid_6'" %('yes',people,noise,temperature))
    else:
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'khalid_6'" %('no',people,noise,temperature))
    mydb.commit()

def customCallbackMerhab_8(client, userdata, message):
    # print("Received a new message: ")
    # print(message.payload)
    # print("from topic: ")
    # print(message.topic)
    # print("--------------\n\n")
    message.payload = message.payload.decode("utf-8")
    print(message.payload)
    value_list = message.payload.split(",")
    people = value_list[0][2:-1]
    people = int(people)
    noise = value_list[1][1:]
    temperature = value_list[2][1:-1]
    mydb = mysql.connector.connect(host="localhost",user="ubuntu",password="", database="assignment03")
    mycursor = mydb.cursor()
    now = datetime.now() + timedelta(hours=8)
    one_hour_before = now - timedelta(hours=1)
    now_str = now.strftime("%H:%M:%S")
    one_hour_before_str = one_hour_before.strftime("%H:%M:%S")
    mycursor.execute("SELECT * from booking_v1 WHERE capacity = 'mehrab_8' AND start_time between '%s' AND '%s'  LIMIT 1" %(one_hour_before_str,now_str))
    result = mycursor.fetchone()
    if (result is not None):
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'mehrab_8'" %('yes',people,noise,temperature))
    else:
        mycursor.execute("UPDATE admin_table SET occupied='%s', people=%d, noise=%s, temperature=%s WHERE room = 'mehrab_8'" %('no',people,noise,temperature))
    mydb.commit()


# Connect and subscribe to AWS IoT
myMQTTClient.connect()
myMQTTClient.subscribe("rpi/data", 1, customCallback)
myMQTTClient.subscribe("khalid_6/data", 1, customCallbackKhalid_6)
myMQTTClient.subscribe("sana_4/data", 1, customCallbackSana_4)
myMQTTClient.subscribe("merhab_8/data", 1, customCallbackMerhab_8)

while True:
    time.sleep(1)