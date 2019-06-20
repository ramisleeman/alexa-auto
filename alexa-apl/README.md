Sample Alexa Python Skill to illustrate video playback using  Video APP and ALEXA PRESENTATION APL 
=========================================

This demo shows a working sample on how to implement video playback on an Alexa screen enabled device. The demo has support for both the video app and the beta Alexa Presentation APL.



Demo is inspired by the JS implemented demo:

https://github.com/alexa-labs/skill-sample-nodejs-firetv-vlogs



To enable the video interace the following must be added to the skill.json file:

```json
"interfaces": [
  {
    "type": "ALEXA_PRESENTATION_APL"
  },
  {
    "type": "VIDEO_APP"
  }
]
```


* ALEXA_PRESENTATION_APL enables the skill to interface using APL (Alexa Presentation Language)

  Ref: https://developer.amazon.com/docs/alexa-presentation-language/apl-overview.html 

* VIDEO_APP enables the skill to interface using video

  Ref: (https://developer.amazon.com/docs/smarthome/add-custom-voice-interaction-to-a-smart-home-skill-using-ask-cli.html)







Concepts
--------

This simple sample has no external dependencies or session management,
and shows the most basic example of how to create a Lambda function for
handling Alexa Skill video requests.





Additional Resources
--------------------

### Community

-  [Amazon Developer Forums](https://forums.developer.amazon.com/spaces/165/index.html) : Join the conversation!
-  [Hackster.io](https://www.hackster.io/amazon-alexa) - See what others are building with Alexa.

### Tutorials & Guides

-  [Voice Design Guide](https://developer.amazon.com/designing-for-voice/) -
   A great resource for learning conversational and voice user interface design.

### Documentation

-  [Official Alexa Skills Kit Python SDK](https://pypi.org/project/ask-sdk/)
-  [Official Alexa Skills Kit Python SDK Docs](https://alexa-skills-kit-python-sdk.readthedocs.io/en/latest/)
-  [Official Alexa Skills Kit Docs](https://developer.amazon.com/docs/ask-overviews/build-skills-with-the-alexa-skills-kit.html)

