import json, logging
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_model.interfaces.alexa.presentation.apl import (
    RenderDocumentDirective, ExecuteCommandsDirective,
    ControlMediaCommand, MediaCommandType)
from ask_sdk_model.interfaces.videoapp import (
    LaunchDirective, VideoItem, Metadata)
from ask_sdk_model import Response
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_core.utils import is_request_type, is_intent_name
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def _load_apl_document(file_path):
    with open(file_path) as f:
        return json.load(f)

class ListItemPressedHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return (is_request_type("Alexa.Presentation.APL.UserEvent")(handler_input) and int(handler_input.request_envelope.request.arguments[0]) > 0)

    def handle(self, handler_input):
        logger.info("In ListItemPressedHandler")
        videoItems = _load_apl_document("./sampleDataSource.json")
        videoItems = videoItems["fireTVVlogsData"]["properties"]["videoItems"]
        selected_item = int(handler_input.request_envelope.request.arguments[0])
        apl_directive = RenderDocumentDirective(
            token="VideoPlayerToken",
            document=_load_apl_document("./videoPlayer.json"),
            datasources={
                "fireTVVlogsData": {
                    "type": "object",
                    "properties": {
                        "selectedItem": selected_item,
                        "videoItems": videoItems
                    }
                }
            }
        )
        execute_directive = ExecuteCommandsDirective(
            token="VideoPlayerToken",
            commands=[
                ControlMediaCommand(
                    component_id="myVideoPlayer",
                    command=MediaCommandType.play)
            ]
        )

        return handler_input.response_builder.speak("playing").add_directive(apl_directive).add_directive(execute_directive).response

class PlaySaidVideo(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("SelectByNumberIntent")(handler_input)
    def handle(self, handler_input):
        logger.info("In PlaySaidVideo")

        try:
            valueCap = int(handler_input.request_envelope.request.intent.slots["ordinal"].value[0]) - 1
        except:
            valueCap = int(handler_input.request_envelope.request.intent.slots["cardinal"].value[0])- 1
        videoItems = _load_apl_document("./sampleDataSource.json")
        videoItems = videoItems["fireTVVlogsData"]["properties"]["videoItems"]

        apl_directive = RenderDocumentDirective(
            token="VideoPlayerToken",
            document=_load_apl_document("./videoPlayer.json"),
            datasources={
                "fireTVVlogsData": {
                    "type": "object",
                    "properties": {
                        "selectedItem": valueCap,
                        "videoItems": videoItems
                    }
                }
            }
        )
        execute_directive = ExecuteCommandsDirective(
            token="VideoPlayerToken",
            commands=[
                ControlMediaCommand(
                    component_id="myVideoPlayer",
                    command=MediaCommandType.play)
            ]
        )

        return handler_input.response_builder.speak("playing").add_directive(apl_directive).add_directive(execute_directive).response

class LaunchAPLVideoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("playAPL_Video")(handler_input)
    def handle(self, handler_input):
        logger.info("In LaunchAPLVideoIntentHandler")
        apl_directive = RenderDocumentDirective(
            token="APL_VideoPlayer",
            document=_load_apl_document("./launchRequest.json"),
            datasources=_load_apl_document("./sampleDataSource.json")
        )
        return handler_input.response_builder.speak("Here are the videos, enjoy!").add_directive(apl_directive).response

class LaunchVideoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        logger.info("In LaunchVideoIntentHandler")
        handler_input.response_builder.speak("welcome to the video demo! You can say: play normal video or play APL video").set_should_end_session(False)
        return handler_input.response_builder.response

class NormalVideoIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return is_intent_name("playVideoApp")(handler_input)

    def handle(self, handler_input):
        logger.info("In NormalVideoIntentHandler")

        video_directive = LaunchDirective(
            video_item=VideoItem(
                source="https://electro-resources.s3.amazonaws.com/testVideo.mp4",
                metadata=Metadata(
                    title="hungry moki",
                    subtitle="This is moki wanting a bite of the cheese pie across the table"
                )
            )
        )
        return handler_input.response_builder.add_directive(video_directive).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        return handler_input.response_builder.response


sb = SkillBuilder()
sb.add_request_handler(LaunchVideoIntentHandler())
sb.add_request_handler(NormalVideoIntentHandler())
sb.add_request_handler(LaunchAPLVideoIntentHandler())
sb.add_request_handler(ListItemPressedHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(PlaySaidVideo())
handler = sb.lambda_handler()
