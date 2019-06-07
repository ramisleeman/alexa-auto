import logging, boto3, json
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

#help
# https://docs.aws.amazon.com/iot/latest/developerguide/using-device-shadows.html
# https://docs.aws.amazon.com/iot/latest/developerguide/iot-plant-watering.html
#Northern California RATES REF:
# https://www.pge.com/tariffs/tm2/pdf/ELEC_SCHEDS_EV.pdf



def chargingPlanner(optionSelected):
    if optionSelected == 'fastest':
        logger.info("In Fastest Charging Function")
        JSON_LOAD =  {
        "state": {
            "desired" : {
                "chargingOption" : "NOW",
                "priceArray": [],
                "powerCap": []                
                        }
                }
        }
        sendMQTT_PayLoad(JSON_LOAD)
    
    elif optionSelected == 'cheapest':
        logger.info("In Cheapest Charging Function")        
        JSON_LOAD =  {
        "state": {
            "desired" : {
                "chargingOption" : "LATER",
                "priceArray": getPriceArray(),
                "powerCap": getPowerArray()               
                        }
                }
        }
        sendMQTT_PayLoad(JSON_LOAD)    
    
    elif optionSelected == 'advanced':
        logger.info("In Advanced Charging Function")        
        JSON_LOAD =  {
        "state": {
            "desired" : {
                "chargingOption" : "ADVANCED",
                "priceArray": getPriceArray(),
                "powerCap": getPowerArray()               
                        }
                }
        }
        sendMQTT_PayLoad(JSON_LOAD)        
 
    
def sendMQTT_PayLoad(JSON_LOAD):
    client = boto3.client('iot-data', region_name='us-east-1')     
    response = client.publish(
            topic = '$aws/things/alexa-charger-Pi/shadow/update',
            qos =1,
            payload = json.dumps(JSON_LOAD))
    logger.info("response is %s", response)



def getPriceArray():
    logger.info("In Get Price Array from DynamoDB")
    dynamodb = boto3.resource("dynamodb", region_name = "us-east-1")
    table = dynamodb.Table("utilityInfo")        
    
    try:
        response = table.get_item(Key={"utility": getUtilityName()})
        logger.info(response)
    except ClientError as e:
        logger.info(e.response["Error"]["Message"])
    else:
        if ("Item" in response):
            logger.info(response["Item"]["costList"])
            return [float(x) for x in response["Item"]["costList"]]
        return "itemNotFound" 



def getPowerArray():
    logger.info("In Get Power Array from DynamoDB")
    dynamodb = boto3.resource("dynamodb", region_name = "us-east-1")
    table = dynamodb.Table("utilityInfo")        
    
    try:
        response = table.get_item(Key={"utility": getUtilityName()})
        logger.info(response)
    except ClientError as e:
        logger.info(e.response["Error"]["Message"])
    else:
        if ("Item" in response):
            logger.info("PowerCAP")
            logger.info(response["Item"]["powerCap"])
            return [float(x) for x in response["Item"]["powerCap"]]
        return "itemNotFound"

    
def getUtilityName():
    return "PGE"