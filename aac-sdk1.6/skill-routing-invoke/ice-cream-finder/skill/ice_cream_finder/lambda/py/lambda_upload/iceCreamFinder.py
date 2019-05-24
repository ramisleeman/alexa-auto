# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the implementation of handler classes approach in skill builder.
import logging

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from routingFunctions import setDestinationFunc
from YELP_API import YelpMainFunc
from distanceCalculator import distanceInKmBetweenCoordinates
from ask_sdk_core.api_client import DefaultApiClient
from ask_sdk_core.dispatch_components import AbstractRequestInterceptor
from ask_sdk_core.dispatch_components import AbstractResponseInterceptor
import time

from ask_sdk_core.skill_builder import CustomSkillBuilder


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")
        geoLocationGranted = handler_input.request_envelope.context.geolocation != None
        if geoLocationGranted:
            speech_text = "Do you want me to search for icecream shops around you"
            handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        else:
            speech_text = "Alexa doesnt seem to have permissions to use your location or device doesnt support it"
            handler_input.response_builder.speak(speech_text).set_should_end_session(True)            
        return handler_input.response_builder.response


class YesIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In YesIntent")

        #get current location
        latitude = handler_input.request_envelope.context.geolocation.coordinate.latitude_in_degrees
        longtitude = handler_input.request_envelope.context.geolocation.coordinate.longitude_in_degrees                                                                 

        #define Search Criteria
        DEFAULT_TERM = 'ice cream'
        DEFAULT_LOCATION = str(latitude) + ',' + str(longtitude)
        SEARCH_LIMIT = 5

        #query the YELP API
        dictResponseList = YelpMainFunc(DEFAULT_TERM, DEFAULT_LOCATION, SEARCH_LIMIT)

        #Analyse the results
        #Get all distance of the resturned list
        latList = [x['coordinates']['latitude'] for x in dictResponseList]
        lonList = [x['coordinates']['longitude'] for x in dictResponseList]
        distanceList = [distanceInKmBetweenCoordinates(latitude,longtitude, x,y) for x,y in zip(latList, lonList)]

        #Get all rating of the resturned list
        ratingList = [x['rating'] for x in dictResponseList]
        #scale rating from 1 to 6 and flip the rating so we can pick the minimum of the cost function
        ratingList = [6-x for x in ratingList]

        #Get only if the location is open
        openList = [int(x['hours'][0]['is_open_now']==True) for x in dictResponseList]

        #Generate a score and get the best result
        resultScore = [a*b*c for a,b,c in zip(distanceList,ratingList, openList)]

        #pick the lowest score representing the best selection based on the above simple cost function
        selectedLocationIndex = resultScore.index(min(resultScore))
        
        latLocation  = dictResponseList[selectedLocationIndex]['coordinates']['latitude']
        longLocation = dictResponseList[selectedLocationIndex]['coordinates']['longitude']      
        name         = dictResponseList[selectedLocationIndex]['name']
        address1     = dictResponseList[selectedLocationIndex]['location']['address1']
        address2     = dictResponseList[selectedLocationIndex]['location']['address2']
        address3     = dictResponseList[selectedLocationIndex]['location']['address3']
        address4     = dictResponseList[selectedLocationIndex]['location']['city']
        address5     = dictResponseList[selectedLocationIndex]['location']['state']
        address6     = dictResponseList[selectedLocationIndex]['location']['zip_code']
        phone        = dictResponseList[selectedLocationIndex]['phone']
        return setDestinationFunc(latLocation, longLocation, name, address1, address2, address3, address4, address5, address6, phone)


class NoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In NoIntent")
        speech_text = "Ok Cancelling"
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In Cancel")
        speech_text = "Goodbye!"
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True

    def handle(self, handler_input, exception):
        logger.error(exception, exc_info=True)
        logger.info("In CatchAllExceptionHandler")
        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech = "Sorry, I'm not sure"
        handler_input.response_builder.speak(speech)
        return handler_input.response_builder.response


# Request and Response loggers
class RequestLogger(AbstractRequestInterceptor):
    """Log the alexa requests."""
    def process(self, handler_input):
        logger.debug("Alexa Request: {}".format(
            handler_input.request_envelope.request))

class ResponseLogger(AbstractResponseInterceptor):
    """Log the alexa responses."""
    def process(self, handler_input, response):
        # type: (HandlerInput, Response) -> None
        logger.debug("Alexa Response: {}".format(response))

sb = CustomSkillBuilder(api_client=DefaultApiClient())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
sb.add_global_request_interceptor(RequestLogger())
sb.add_global_response_interceptor(ResponseLogger())
handler = sb.lambda_handler()
