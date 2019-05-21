# alexa-auto

The subfolders located under aac-sdk 1.6 include quick reference to implement the following features on top of Alexa Auto SDK 1.6 (Andoid Implementation):

1. Local Media Implementation: Quick guide to register a local media device (a USB in this case).

2. Routing Implementation: Quick guide to start and cancel routing, using a custom skill that searches for ice-cream shops and sends the ‘best option’ to the Auto SDK that invokes Google Maps.

3. MQTT Implementation: Quick guide to implement MQTT messaging between the Android Sample App and AWS Lambda. In this example, the temperature sensor from Samsung Tab3 is sent to the cloud. (It is assumed that the Auto SDK Andoid Sample App is running on the Samsung Tab3 Tablet.)

In each folder, a README presents with high level what was implemented and the aac-sdk folder has the implementation. For the routing example, the sample skill is placed in a separate folder (ice-cream-finder).
The implementation in the aac-sdk folder is based on AUTO SDK 1.6, with only the changes required to implement the described tasks.