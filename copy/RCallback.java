package org.org.kivads;

import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback;
import com.google.android.gms.ads.rewarded.RewardedAd;


public class RCallback extends RewardedAdLoadCallback {

    private RewardedAd mRewardedAd;

    private boolean loaded;

    @Override
    public void onAdLoaded(RewardedAd rewardedAd) {
       // The mRewardedAd reference will be null until
       // an ad is loaded.
       mRewardedAd = rewardedAd;
       loaded = true;
     }

}
