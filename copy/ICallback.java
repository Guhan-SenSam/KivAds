package org.org.kivads;

import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback;
import com.google.android.gms.ads.interstitial.InterstitialAd;
import org.kivy.android.PythonActivity;


public class ICallback extends InterstitialAdLoadCallback {

    private InterstitialAd mInterstitialAd;

    private boolean loaded;

    @Override
    public void onAdLoaded(InterstitialAd interstitialAd) {
       // The mInterstitialAd reference will be null until
       // an ad is loaded.
       mInterstitialAd = interstitialAd;
       loaded = true;
     }

}
