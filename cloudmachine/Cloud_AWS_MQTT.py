import time  #Import time library
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient


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
    time.sleep(2)  #Delay of 2 seconds
    
    value = 200
    payload = '{"cloud message: ":'+ str(value) +'}'
    print (payload)
    myMQTTClient.publish("cloud/data", payload, 0)
