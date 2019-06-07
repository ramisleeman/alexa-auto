import logging
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.api_client import DefaultApiClient
from chargingScheduler import chargingPlanner

sb = CustomSkillBuilder(api_client=DefaultApiClient())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchRequestHandler")
        speech_text = "Welcome to Alexa's Charging scheduler, are you looking\
        for the cheapest or fastest charging?"
        handler_input.response_builder.speak(speech_text).set_should_end_session(False)
        return handler_input.response_builder.response


class FastestChargingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("FastestChargingIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FastestChargingIntentHandler")
        chargingPlanner('fastest')
        speech_text = "This is the fastest charging Intent"
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class CheapestChargingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("CheapestChargingIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In CheapestChargingIntentHandler")
        chargingPlanner('cheapest')
        speech_text = "This is the cheapest charging Intent"
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

    
class AdvancedChargingIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AdvancedChargingIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In AdvancedChargingIntentHandler")
        chargingPlanner('advanced')
        speech_text = "This is the advanced charging Intent"
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

  
class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In HelpIntentHandler")
        speech_text = "You can say cheapest, fastest, or advanced"
        ask_text = "What would you like to do?"
        handler_input.response_builder.speak(speech_text).ask(ask_text).set_should_end_session(False)
        return handler_input.response_builder.response


class CancelOrStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        logger.info("In CancelOrStopIntentHandler")
        speech_text = "Goodbye!"
        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response


class FallbackIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        logger.info("In FallbackIntentHandler")
        speech_text = "Did you say something sily, please stick to the script"
        reprompt = "You can say cheapest, fastest, or advanced"
        handler_input.response_builder.speak(speech_text).ask(reprompt)
        return handler_input.response_builder.response


class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In SessionEndedRequestHandler")
        return handler_input.response_builder.response


class CatchAllExceptionHandler(AbstractExceptionHandler):
    def can_handle(self, handler_input, exception):
        return True
    def handle(self, handler_input, exception):    
        logger.error(exception, exc_info=True)
        speech = "Sorry, there was some problem. Please try again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response


sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CheapestChargingIntentHandler())
sb.add_request_handler(FastestChargingIntentHandler())
sb.add_request_handler(AdvancedChargingIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_exception_handler(CatchAllExceptionHandler())
handler = sb.lambda_handler()