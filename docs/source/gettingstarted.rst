Getting Started
================

KivAds uses the latest version of Google AdMob SDK (version 20.0.3). This allows
for great compatibility and access of all the latest features that are provided
in the SDK. The downside is that the setup procedure is a little more complicated
than a typical python library/module.

Installation
############

Currently the only installation method availble is to clone the library from
Github and then copy the files manually into location.

1. Clone library from github::

    https://github.com/Guhan-SenSam/KivAds
2. Copy the *kivads.py* to the root of your working directory.
3. Create a folder called *scr* in your working directory.
4. Copy all the contents(5 Java files) from the *copy* folder in the library to the *scr* folder you just created.


.. note:: You need to repeat this procedure for every project you want to use KivAds in.

Setting Up Buildozer
####################

Now that you have successfully installed KivAds, you need to change some things both in
buildozer and python-for-android for KivAds to work. Hopefully these steps will not be
necessary in the future as buildozer is updated.

1. Clone the latest version of python-for-android from `here <https://github.com/kivy/python-for-android>`_ into your working directory.
2. Navigate to this file::

    python-for-android/pythonforandroid/bootstraps/common/build/gradle/wrapper/gradle-wrapper.properties

and change line number 6 from::

    distributionUrl=https\://services.gradle.org/distributions/gradle-6.4.1-all.zip

to::

    distributionUrl=https\://services.gradle.org/distributions/gradle-6.5-all.zip

Currently KivAds only works on this gradle version. Other versions are being tested

3. Change the following fields in your *buildozer.spec* file.::

    android.permissions
    android.api
    android.gradle_dependencies

to::

    android.permissions = INTERNET, ACCESS_NETWORK_STATE
    android.api = 30 # Anything 28 and above is okay
    android.gradle_dependencies = 'com.google.android.gms:play-services-ads:20.3.0'

4. Add your admob app-id to the manifest file in order for ads to work in your app. Change the `android.meta_data` to::

    android.meta_data = com.google.android.gms.ads.APPLICATION_ID=<Your app ID>

Everything should be set up and you can now compile your app.

.. Note:: KivAds only works on android. Ads will not be shown on any other platform
