package org.org.kivads;

import com.google.android.gms.ads.AdListener;
public class BListener extends AdListener {

    private boolean loaded;
    private boolean clicked;

    @Override
    public void onAdLoaded() {
       loaded = true;
     }

    @Override
    public void onAdOpened(){
        clicked = true;
    }

}
