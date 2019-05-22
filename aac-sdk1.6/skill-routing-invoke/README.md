# alexa-auto
## quick guide to implement navigation invocation from a custom skill


##### Prerequisites: Alexa Auto Android Sample App is already implemented and running per the official instructions:  https://github.com/alexa/aac-sdk


![highlevel architecture](Resources/skill-routing-invoke.png)





This demo requires the implementation of 2 pieces:

- Alexa Auto SDK must modified to invoke Google Maps from the Tablet. Added logic also supports canceling navigation as well.

-  A Sample Skill that once triggered will invoke Yelp API and responds back with the closest and highest rating ice-cream shop in the proximity of the Android Tablet. A simple cost function is implemented to return a specific ice-cream shop.

### Alexa Auto SDK Changes

Changes must be implemented in the NavigationHandler.java folder located in the following direcotory:

/aac-sdk/samples/android/app/src/main/java/com/amazon/sampleapp/impl/Navigation/

