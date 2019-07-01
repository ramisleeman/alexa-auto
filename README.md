# alexa-auto

**Prerequisites:** Alexa Auto Android Sample App is already implemented and running per the official instructions:  https://github.com/alexa/aac-sdk



## aac-sdk 1.6

The subfolders located under **aac-sdk 1.6** include a quick reference to implement the following features on top of Alexa Auto SDK 1.6 (Andoid Implementation):


1. **Local Media Implementation:** Quick guide to register a local media device (a USB in this case).

2. **Routing Implementation:** Quick guide to start and cancel routing, using a custom skill that searches for ice-cream shops using a Yelp API and sends the ‘best option’ to the Auto SDK that invokes Google Maps.

3. **MQTT Implementation:** Quick guide to implement MQTT messaging between the Android Sample App and AWS IoT.

In each folder, a README presents a detailed notes on the specific implementation and the aac-sdk folder has the implementation. For the routing example, the sample skill is placed in a separate folder (ice-cream-finder).
The implementation in the aac-sdk folder is based on AUTO SDK 1.6, with only the changes required to implement the described tasks.



## optimizedCharging

**optimizedCharging** is demo skill that interfaces with a home smart charger and then gives the electric vehicle and Alexa user the option to charge their car with the cheapest option possible by interfacing with the grid and getting the cheapest price. 



## alexa-apl
**alexa-apl** is a demo skill implemented in python that illustartes the usuage of videoplayback using both VIDEO_APP and APL.




## voice-can-interface
**voice-can-intrface** is a sample demo that reads the OBD-II port of vehicles and then reports back the faults through an Alexa Skill. 



##tools/apl-list-generator
**apl-list-generator** is a tool that generates <launchRequest.json> through a python script without the need to modify the JSON files. launchRequest.json is used to list items using Amazon's APL.