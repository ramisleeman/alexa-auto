# alexa-auto
## quick guide to implement mqtt using AWS IoT on the Android Auto Sample App



**AWS Steps Required:**

1. Create a certificate and key under **Amazon Cognito Console**
   * Go to https://console.aws.amazon.com/cognito
   
   * Click "Manage Identity Pools"
   
   * Click "Create new identity pool"
   
   * Give a name to the Identity pool name
   
   * Check the Enable access to unauthenticated identities
   
   * Click create pool
   
   *  On the next page click Allow
     
      NOTE: Under details you can see that 2 roles were created Cognito_"PoolName"_Auth_Role and Cognito_"PoolName"Unauth_Role
      
    * Click Allow
   
    * Change Platform to Android
   
    *  Capture the Identity pool ID and the region that will show up in the Get AWS Credentials box, these will be utilized later in the application code.
   
2. Attach a policy to the IAM Console so permissions are allowed to do the required AWS IoT calls.

   * Go to https://console.aws.amazon.com/iam/
   * Click on roles on the side bar
   * Search the roles for the pool name that was created in step 1. There should be 2 roles:
     * Cognito_"PoolName"_Auth_Role
     * Cognito_"PoolName"Unauth_Role
   * Click on the Cognito_"PoolName"Unauth_Role
   * Click on the Add inline policy
   * Navigate to the JSON Tab and paste the below:

   ```JSON

   {
    "Version": "2012-10-17",
    "Statement": [
    {
            "Effect": "Allow",
            "Action": [
                "iot:AttachPrincipalPolicy",
                "iot:CreateKeysAndCertificate"
            					],
            "Resource": [
            "*"
            ]
        }
        ] 
     }

   ```

   *    Setup is complete to permit the Alexa auto sample app to connect to the AWS IoT platform using Cognito and upload certificates and policies.

3. Create a policy and attach it to the Device Certificate that will permit a connection to the AWS IoT message broker to allow publish and subscribe operations.

   * Go to https://console.aws.amazon.com/iot/
   
   * Click on secure in the left tab
   
   * Click on Policies under Secure in the left tab
   
   * Click on create
   
   * Name the policy
   
   * Click on advanced and paste the below:
   
   ```JSON
       {
         "Version": "2012-10-17",
         "Statement": [
           {
             "Effect": "Allow",
             "Action": "iot:Connect",
             "Resource": "*"
           },
           {
             "Effect": "Allow",
             "Action": [
               "iot:Publish",
               "iot:Subscribe",
               "iot:Receive"
             ],
             "Resource": "*"
           }
         ]
       }
   ```





**Android Auto Steps Required:**

* Open MainActivity.java located under:

  /aac-sdk/samples/android/app/src/main/java/com/amazon/sampleapp

  And change the following 3 parameters:

```java
private static final Regions MY_REGION = Regions.FILL-HERE;
```
```java
private static final String CUSTOMER_SPECIFIC_ENDPOINT = "FILL-HERE";
```
``` java
private static final String AWS_IOT_POLICY_NAME = "FILL-HERE";
```


1. CUSTOMER_SPECIFIC_ENDPOINT is located under the setting page located in the following link:

https://console.aws.amazon.com/iot/ 

2. AWS_IOT_POLICY_NAME is the policy name that was created is step 3 

3. MY_REGION is located under Sample code in the identity pool in the following link (Step 1 Above)
   https://console.aws.amazon.com/cognito 

* Open awsconfiguration.json located under:

  ```
  /aac-sdk/samples/android/app/src/main/res/raw
  ```

And change the following 2 parameters:

```json
    "PoolId": "FILL-HERE",
    "Region": "FILL-HERE"
```
PoolID and Region can be found in https://console.aws.amazon.com/cognito under AWS Credentials (Step 1 above).

PS: Region should be in lower case ex: "us-east-1"



**Android Auto and AWS Configuration is now complete and the system should be to subscribe and publish messages through the AWS IoT broker.**



**Summary of changes done to the Android Sample App:**

1. Add awsconfiguration.json located under:

   /aac-sdk/samples/android/app/src/main/res/raw

2. Change the build.grade to include aws dependencies:

   1. ```java
      implementation "com.amazonaws:aws-android-sdk-iot:2.11.+"
      implementation "com.amazonaws:aws-android-sdk-mobile-client:2.11.+"
      ```

3. 