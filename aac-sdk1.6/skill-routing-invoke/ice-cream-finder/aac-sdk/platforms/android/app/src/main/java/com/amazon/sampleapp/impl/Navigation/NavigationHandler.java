/*
 * Copyright 2017-2019 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *     http://aws.amazon.com/apache2.0/
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

package com.amazon.sampleapp.impl.Navigation;

import com.amazon.aace.navigation.Navigation;
import com.amazon.sampleapp.impl.Logger.LoggerHandler;
import com.amazon.sampleapp.logView.LogRecyclerViewAdapter;

import org.json.JSONException;
import org.json.JSONObject;

//Added for setDestinationDirective
import android.app.Activity;
import android.content.Intent;
import android.net.Uri;
import android.content.Context;

public class NavigationHandler extends Navigation {

    private static String sTag = "Navigation";
    private LoggerHandler mLogger = null;
    //Added for setDestinationDirective
    private Context mContext;

    public NavigationHandler( Context context, LoggerHandler logger ) {
        mLogger = logger;

        //Added for setDestinationDirective
        mContext = context;
    }

    @Override
    public boolean setDestination(String payload ) {
        // Handle navigation to destination here

        // Added by Rami
        mLogger.postInfo(sTag, "Moki Testing");
        mLogger.postInfo(sTag, payload);

        try {
            // Log payload
            JSONObject template = new JSONObject( payload );
            mLogger.postJSONTemplate( sTag, template.toString(4 ) );

            // Log display card
            mLogger.postDisplayCard( template, LogRecyclerViewAdapter.SET_DESTINATION_TEMPLATE );


            //Added for setDestinationDirective
            //Get lat and long from the payload
            double latitude  = template.getJSONObject("destination").getJSONObject("coordinate").getDouble("latitudeInDegrees");
            double longitude = template.getJSONObject("destination").getJSONObject("coordinate").getDouble("longitudeInDegrees");


            Intent intent = new Intent(android.content.Intent.ACTION_VIEW,
                    Uri.parse("google.navigation:q=" + latitude + "," + longitude));

            // only attempt to open the navigation system if the system can identify an app that can respond to the intent
            if (intent.resolveActivity(mContext.getPackageManager()) != null) {
                mContext.startActivity(intent);
            }

            return true;

        } catch ( JSONException e ) {
            mLogger.postError( sTag, e.getMessage() );
            return false;
        }
    }

    @Override
    public boolean cancelNavigation() {
        mLogger.postInfo( sTag, "Cancel Navigation Called" );

        Intent mapIntent = new Intent(Intent.ACTION_VIEW);
        mapIntent.setPackage("com.google.android.apps.maps");
        mapIntent.setFlags(Intent.FLAG_ACTIVITY_CLEAR_TASK);

        // only attempt to cancel navigation if the system can identify an app that can respond to the intent
        if (mapIntent.resolveActivity(mContext.getPackageManager()) != null) {
            mContext.startActivity(mapIntent);
        }

        return true;
    }
}
