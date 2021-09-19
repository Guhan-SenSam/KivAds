package org.org.kivads;

import com.google.android.gms.ads.rewardedinterstitial.RewardedInterstitialAdLoadCallback;
import com.google.android.gms.ads.rewardedinterstitial.RewardedInterstitialAd;


public class RICallback extends RewardedInterstitialAdLoadCallback {

    private RewardedInterstitialAd mRewardedInterstitialAd;

    private boolean loaded;

    @Override
    public void onAdLoaded(RewardedInterstitialAd rewardedAd) {
       // The mRewardedAd reference will be null until
       // an ad is loaded.
       mRewardedInterstitialAd = rewardedAd;
       loaded = true;
     }

}
