# KivAds

Monetize your apps with KivAds using Google AdMob api.

KivAds uses the latest version of Google AdMob sdk(version 20.0.0). KivAds exposes most of the functions and operations available in the Admob sdk as easy to use python functions, allowing you to quickly integrate ads into your app. So far in testing KivAds works 100% reliabily on devices from android 6 all the way upto android 11.

## Important Info

* Because KivAds uses the latest SDk version, some of its functionality is implemented using java classes. Do not worry as you don't need to change any of these files, only copy them to your working directory as stated below.

## Documentation

[readthdocs](https://kivads.readthedocs.io/en/latest/)
[discord](https://discordapp.com/users/822127725535428639/).


## Demo
There is a demo program inside the demo folder. Also included is a compiled apk which you can install and try out the different types of ads that are available.


## Things To Do
These are the things that are still left to be implemented in KivAds.

- [ ] Native Ads(May or May not be added. Need to figure out how to attach android layouts to a kivy widget)
- [ ] Make Individual Demos


## Installation
Currently cloning the repo is the only installation method. For more detailed info refer to the documentation.

## Requirements

KivAds requires some changes to your buildozer.spec file and also python-for-android module in order to work. Hopefully in the future there wouldn't be a need to change any of python-for-android files.

1. Clone the latest version of [python-for-android](https://github.com/kivy/python-for-android) into your working directory.

2. Navigate to this file `python-for-android/pythonforandroid/bootstraps/common/build/gradle/wrapper/gradle-wrapper.properties` and change line number 6 from
`distributionUrl=https\://services.gradle.org/distributions/gradle-6.4.1-all.zip
`
to `distributionUrl=https\://services.gradle.org/distributions/gradle-6.5-all.zip
`

    I am still testing other gradle versions to see if they will work with KivAds.

3. Now change the following fields in your `buildozer.spec` file.
`android.permissions`,
`android.api`,
`android.gradle_dependencies`

    to this
    ```
    android.permissions = INTERNET, ACCESS_NETWORK_STATE
    android.api = 30 # Anything 28 and above is okay
    android.gradle_dependencies = 'com.google.android.gms:play-services-ads:20.3.0'
    ```

4. Now you need to add your admob app-id to the manifest file in order for ads to work in your app. Change the `android.meta_data`
to
```
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=<Your app ID>
```

5. After adding your code in your python file. Copy all the files in the src folder of this repo into a folder called src in your working directory. Then change the following field in your buildozer.spec file `android.add_src` to `android.add_src = src`.


## Test Ids
You can use this ID(Provided By Google) in order to test ads on your app without the need of an admob account. Just remember to change these to your actual AdMob id's or else you wont be able to earn any revenue. KivAds also provides Test Ids for all types of ads within your code.

Test App Id: `ca-app-pub-3940256099942544~3347511713`


## Important Links
* https://developers.google.com/admob/android/quick-start
* https://github.com/kivy/python-for-android
