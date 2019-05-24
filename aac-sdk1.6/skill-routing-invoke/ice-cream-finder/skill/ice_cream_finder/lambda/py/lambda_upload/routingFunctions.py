from ask_sdk_core.handler_input import HandlerInput
from botocore.exceptions import ClientError
from ask_sdk_model.services.directive import (SendDirectiveRequest, Header, SpeakDirective)
import logging, requests
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def setDestinationFunc(latitude, longtitude, name, address1, address2,  address3, address4, address5, address6, phone):
    logger.info("In setDestinationFunc")
    returnedAddress =''
    returnedAddressSplit1 = ''
    returnedAddressSplit2 = ''
    
    if address1 is not None:
        returnedAddress = address1
        returnedAddressSplit1 = address1
    if address2 is not None:
        returnedAddress = returnedAddress + ' ' + address2
        returnedAddressSplit1 = returnedAddressSplit1 + ' ' + address2
    if address3 is not None:
        returnedAddress = returnedAddress + ' ' + address3
        returnedAddressSplit1 = returnedAddressSplit1 + ' ' + address3
    if address4 is not None:
        returnedAddress = returnedAddress + ' ' + address4
        returnedAddressSplit2 = returnedAddressSplit2 + ' ' + address4
    if address5 is not None:
        returnedAddress = returnedAddress + ' ' + address5
        returnedAddressSplit2 = returnedAddressSplit2 + ' ' + address5
    if address6 is not None:
        returnedAddress = returnedAddress + ' ' + address6
        returnedAddressSplit2 = returnedAddressSplit2 + ' ' + address6
    
    logger.info(returnedAddress)
    logger.info(returnedAddressSplit1)
    logger.info(returnedAddressSplit2)

    return {
        "can_fulfill_intent": None,
        "card": None,
        "outputSpeech": {
            "type": "PlainText",
            "text": "Ok sending driving directions to" + name
        },
        "directives": [ {
                    "type": "Navigation.SetDestination",
                    "destination": {
                        "coordinate": {
                            "latitudeInDegrees": latitude,
                            "longitudeInDegrees": longtitude
                        },
                        "singleLineDisplayAddress": returnedAddress,
                        "multipleLineDisplayAddress":returnedAddressSplit1 + '\n' + returnedAddressSplit2,
                        "name":name,
                    },
                    "transportationMode":"DRIVING",
                    "metadata":{
                        "phoneNumber": phone
                    }
                }
            ],
        "shouldEndSession": True
}
        


## NOT CURRENTLY SUPPORTED FOR CUSTOM SKILLS
def cancelRouteFunc():
    return {
        "type": "Navigation.CancelNavigation"
        }