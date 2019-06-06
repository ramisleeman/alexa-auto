package com.amazon.sampleapp;

import android.app.Activity;
import android.content.Context;
import android.content.ContextWrapper;
import android.util.Log;
import com.amazonaws.mobile.client.AWSMobileClient;
import com.amazonaws.mobileconnectors.iot.AWSIotKeystoreHelper;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttLastWillAndTestament;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttManager;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttQos;
import com.amazonaws.regions.Region;
import com.amazonaws.services.iot.AWSIotClient;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.mobileconnectors.iot.AWSIotKeystoreHelper;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttClientStatusCallback;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttLastWillAndTestament;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttManager;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttNewMessageCallback;
import com.amazonaws.mobileconnectors.iot.AWSIotMqttQos;
import com.amazonaws.regions.Region;
import com.amazonaws.regions.Regions;
import com.amazonaws.services.iot.AWSIotClient;
import com.amazonaws.services.iot.model.AttachPrincipalPolicyRequest;
import com.amazonaws.services.iot.model.CreateKeysAndCertificateRequest;
import com.amazonaws.services.iot.model.CreateKeysAndCertificateResult;
import com.amazonaws.AmazonClientException;

import java.security.KeyStore;


public class mqtt_manager extends Activity {
    private static final Regions MY_REGION = Regions.US_EAST_1;
    private static final String CUSTOMER_SPECIFIC_ENDPOINT = "a17ewziahkj38y-ats.iot.us-east-1.amazonaws.com";
    static AWSIotMqttManager mqttManager;
    static AWSIotClient mIotAndroidClient;
    static String keystoreName = "iot_keystore";
    static String keystorePassword = "password";
    static String certificateId = "default";
    private static final String KEYSTORE_NAME = "androiddebugkey";
    private static final String KEYSTORE_PASSWORD = "";
    private static final String CERTIFICATE_ID = "default";
    private static KeyStore clientKeyStore = null;


    /* Init */
    public static void initIoTClient(final String  clientId, Context context) {
        Log.i("AWS-init", "In initIoTClient");
        ContextWrapper wrapper = new ContextWrapper(context);
        final String keystorePath = wrapper.getFilesDir().getPath();

        Region region = Region.getRegion(MY_REGION);
        mqttManager = new AWSIotMqttManager(clientId, CUSTOMER_SPECIFIC_ENDPOINT);
        mqttManager.setKeepAlive(10);


        AWSIotMqttLastWillAndTestament lwt = new AWSIotMqttLastWillAndTestament("my/lwt/topic",
                "Android client lost connection", AWSIotMqttQos.QOS0);

        mqttManager.setMqttLastWillAndTestament(lwt);
        mIotAndroidClient = new AWSIotClient(AWSMobileClient.getInstance());
        mIotAndroidClient.setRegion(region);

        Boolean checkIfKeyStoreIsPresent;
        checkIfKeyStoreIsPresent = AWSIotKeystoreHelper.isKeystorePresent(keystorePath, keystoreName);

        Boolean checkIfAliasIsPresent;
        checkIfAliasIsPresent = AWSIotKeystoreHelper.keystoreContainsAlias(certificateId, keystorePath, keystoreName, keystorePassword);
        try {
            if (checkIfKeyStoreIsPresent) {
                if (checkIfAliasIsPresent) {
                    Log.i("AWS-init:", "Certificate " + certificateId  + " found in keystore - using for MQTT.");
                    // load keystore from file into memory to pass on connection
                    clientKeyStore = AWSIotKeystoreHelper.getIotKeystore(certificateId,keystorePath, keystoreName, keystorePassword);
                } else {Log.i("AWS-init:", "Key/cert " + certificateId + " not found in keystore.");}
            } else {Log.i("AWS-init:", "Keystore " + keystorePath + "/" + keystoreName + " not found.");}
        }
        catch (Exception e) {Log.i("AWS-init:", "An error occurred retrieving cert/key from keystore.");}
    }

    /* Connect */
    public static void mqttConnect(){
        Log.i("AWS-init", "In mqttConnect");
    }


    /* Subscribe */
    public static void mqttSubscribe(){
        Log.i("AWS-init", "In mqttSubscribe");

    }


    /* Publish */
    public static void mqttPublish() {
        Log.i("AWS-init", "In mqttPublish");
    }

}
