package org.kivads.kivads;

import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.gms.ads.interstitial.InterstitialAd;
import org.kivy.android.PythonActivity;
import java.lang.Boolean;


public class ICallback extends InterstitialAdLoadCallback {

    private InterstitialAd mInterstitialAd;

    private Boolean ready;

    @Override
    public void onAdLoaded(InterstitialAd interstitialAd) {
       // The mInterstitialAd reference will be null until
       // an ad is loaded.
       mInterstitialAd = interstitialAd;
       ready = true;
     }

}
