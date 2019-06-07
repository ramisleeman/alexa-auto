from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import json, time, datetime
import RPi.GPIO as GPIO
import numpy as np

#InitDefinitions
global firstTimeCheapest
firstTimeCheapest = True
global firstTimeFastest
firstTimeFastest  = True
global firstTimeAdvanced
firstTimeAdvanced = True

# Setup the GPIO Pins
GPIO_List = [21, 13, 6, 5]
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
[GPIO.setup(x, GPIO.OUT)    for x in GPIO_List]
[GPIO.output(x, GPIO.HIGH)  for x in GPIO_List]

# AWS IoT Variable Definitions
SHADOW_CLIENT = "myShadowClient"
HOST_NAME = "a17ewziahkj38y-ats.iot.us-east-1.amazonaws.com" 
ROOT_CA = "AmazonRootCA1.pem"
PRIVATE_KEY = "3a3f6cd782-private.pem.key"
CERT_FILE = "3a3f6cd782-certificate.pem.crt.txt"
SHADOW_HANDLER = "alexa-charger-Pi"

# Create, configure, and connect a shadow client.
myShadowClient = AWSIoTMQTTShadowClient(SHADOW_CLIENT)
myShadowClient.configureEndpoint(HOST_NAME, 8883)
myShadowClient.configureCredentials(ROOT_CA, PRIVATE_KEY,CERT_FILE)
myShadowClient.configureConnectDisconnectTimeout(10)
myShadowClient.configureMQTTOperationTimeout(5)
myShadowClient.connect()

# Create a programmatic representation of the shadow.
myDeviceShadow = myShadowClient.createShadowHandlerWithName(SHADOW_HANDLER, True)

#Relay Dance Switching
GPIO_List_dance =  GPIO_List[1:]
def fastestLightDance():
    for x in range(3):
        [GPIO.output(y, GPIO.LOW)  for y in GPIO_List_dance]
        time.sleep(0.25)
        [GPIO.output(y, GPIO.HIGH)  for y in GPIO_List_dance]
        time.sleep(0.25)
 
def cheapestLightDance():
    for i in range(2):
        [GPIO.output(x, GPIO.LOW)  for x in GPIO_List_dance]
        time.sleep(0.15)
        [GPIO.output(x, GPIO.HIGH)  for x in GPIO_List_dance]
        time.sleep(0.15)
    [GPIO.output(x, GPIO.LOW) for x in GPIO_List_dance]        

def advancedLightDance():
    for i in range(2):
        [GPIO.output(x, GPIO.LOW)  for x in GPIO_List_dance]
        time.sleep(0.25)
        [GPIO.output(x, GPIO.HIGH)  for x in GPIO_List_dance]
        time.sleep(0.25)
    [GPIO.output(x, GPIO.LOW)  for x in GPIO_List_dance[0:2:-1]]  
    
# Define Activity for the fastest, cheapest, and advanced options
def fastestSelection():
    GPIO.output(21,GPIO.LOW)
    global firstTimeFastest, firstTimeCheapest, firstTimeAdvanced
    if firstTimeFastest:
        fastestLightDance()
    firstTimeFastest  = False
    firstTimeCheapest = True
    firstTimeAdvanced = True
    print("FASTEST")

def cheapestSelection(price):
    GPIO.output(21,GPIO.HIGH)
    global firstTimeFastest, firstTimeCheapest, firstTimeAdvanced
    if firstTimeCheapest:
	cheapestLightDance()
    firstTimeFastest  = True
    firstTimeCheapest = False
    firstTimeAdvanced = True
    #logic to determine when to start charging given the cheapest price constriants
    
    #TOY EXAMPLE
    timeNeededToCharge = 48 #(4 hours from 0 to 100 is equivialnt to 48 minutes for 20% topoff, assuming 4 hours for a full charge)
    #round to the highest 10th minute (to match the data)
    timeNeededToCharge = 50
    #get the current time and search from the found time for the next 24 hours
    cheapestCost = np.inf
    hour = datetime.datetime.now().hour
    min = datetime.datetime.now().minute
    timeIndex = int(np.ceil((hour * 60 + min)/10))
    print("time now in 10-min scale is ", timeIndex)
    
    price_temp = list(price)
    [price.append(x) for x in price_temp]
    #print(price)
    
    #search for the minimum 5 slots (adding to 50 minutes that yields the lowest cost)
    resultIndex = timeIndex
    for index in range(timeIndex, timeIndex + (24*60/10) - 5):
        sumCost = sum(price[index:index+5])
        if sumCost < cheapestCost:
            cheapestCost = sumCost 
            resultIndex = index                 
    print("CHEAPEST")
    print("starting Index is", resultIndex)
    time.sleep((resultIndex-timeIndex)*10*60)
    GPIO.output(21,GPIO.LOW)


def advancedSelected(price, power):
    global firstTimeFastest, firstTimeCheapest, firstTimeAdvanced
    if firstTimeAdvanced:
        advancedLightDance()
    firstTimeFastest  = True
    firstTimeCheapest = True
    firstTimeAdvanced = False  
    GPIO.output(21,GPIO.HIGH)
    print("ADVANCED")
    

def parse_payload(payload, responseStatus, token):
    if responseStatus == "timeout":
	print("Time Out")
	return
    if responseStatus == "rejected":
	print("Response Rejected")
	return
    if responseStatus == "accepted":
	dict = json.loads(payload)
   	if dict["state"]["desired"]["chargingOption"] == "NOW":
            fastestSelection()
    	if dict["state"]["desired"]["chargingOption"] == "LATER":
	    cheapestSelection(dict["state"]["desired"]["priceArray"])
   	if dict["state"]["desired"]["chargingOption"] == "ADVANCED":
	    advancedSelected(dict["state"]["desired"]["priceArray"], dict["state"]["desired"]["powerCap"])

while True:
	try:
	   myDeviceShadow.shadowGet( parse_payload, 5 )
	   time.sleep(15)
	except:
	   time.sleep(2)
