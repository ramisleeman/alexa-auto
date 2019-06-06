# alexa-auto
## quick guide to implement local music source


#### implementation of local music control on top of the Alexa auto SDK

##### Prerequisites: Alexa Auto Android Sample App is already implemented and running per the official instructions:  https://github.com/alexa/aac-sdk

Local Media support includes support for the following sources:

   - Source_BLUETOOTH;
   - Source_USB;
   - Source_FM_RADIO;
   - Source_AM_RADIO;
   - Source_SATELLITE_RADIO;
   - Source_LINE_IN;
   - Source_COMPACT_DISC;



The supported sources can be found in LocalMediaSourceBinder.h located in this directory:
/aac-sdk/platforms/android/aace/src/main/cpp/include/aace/alexa/



As an example, to enable USB music, The following implementation is required:

1. Add a JAVA class under this directory:
/aac-sdk/samples/android/app/src/main/java/com/amazon/sampleapp/impl/LocalMediaSource/

2. Follow the same logic as the already implemented CD <CDLocalMediaSource.java>located under the same directory

3. Modify the MainActivity.java file by adding the following:

```
// import the added class
import com.amazon.sampleapp.impl.LocalMediaSource.USBLocalMediaSource;

//define the class
private USBLocalMediaSource mUSBLocalMediaSource;

       
mUSBLocalMediaSource =  new USBLocalMediaSource(this, mLogger, USBLocalMediaSource.Source.USB);

//register the USB player and throw an exception if not successful 
if ( !mEngine.registerPlatformInterface(mUSBLocalMediaSource) )
   throw new RuntimeException( "Could not register Mock USB player Local Media Source platform interface" );
```

Now that the source is registered, you can implement the activity around this implementation. This should be done in the implemented class (USBLocalMediaSource.java), and this is specific to the hardware that is used for the implementation.