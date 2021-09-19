package org.org.kivads;

import com.google.android.gms.ads.FullScreenContentCallback;

public class FullScreen extends FullScreenContentCallback {

    private boolean dismissed;

    @Override
    public void onAdDismissedFullScreenContent() {
     // Called when the ad is dismissed
     dismissed = true;

    }
}
