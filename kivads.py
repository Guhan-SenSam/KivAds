from kivy.properties import BooleanProperty
from kivy.utils import platform
from kivy.logger import Logger

if platform == "android":
    from android import mActivity, autoclass, cast
    from android.runnable import run_on_ui_thread

    context = mActivity.getApplicationContext()
    AndroidBool = autoclass("java.lang.Boolean")
    AndroidString = autoclass("java.lang.String")
    MobileAds = autoclass("com.google.android.gms.ads.MobileAds")
    AdRequest = autoclass("com.google.android.gms.ads.AdRequest")
    AdRequestBuilder = autoclass("com.google.android.gms.ads.AdRequest$Builder")
    RequestConfigurationBuilder = autoclass(
        "com.google.android.gms.ads.RequestConfiguration$Builder"
    )
    RequestConfiguration = autoclass("com.google.android.gms.ads.RequestConfiguration")

    _InterstitialAd = autoclass(
        "com.google.android.gms.ads.interstitial.InterstitialAd"
    )

    InterstitialCallback = autoclass("org.org.kivads.ICallback")
    FullScreenContentCallbackI = autoclass("org.org.kivads.IFullScreen")


class InterstitialAd:
    """This class represents an Interstitial Ad Object. Instance this clas in your code
    in order to create and show an ad. This class is designed to only be used once, meaning
    after you call the `show()` method you should disregard this class. If you need to
    show another interstitial ad then again instance this class. Do not attempt to reuse the
    same class as ads will not be shown(This behaviour may change based on what others suggest).
    """

    callback = InterstitialCallback()
    """This is the callback that is triggered when an ad is loaded. You dont need to
    change anything regarding this callback.
    """

    full_screen_callback = FullScreenContentCallbackI()

    def __init__(self, UnitID):
        if platform == "android":
            Logger.info("KivAds: Loading Interstitial Ad")
            # Set the loaded and the dismissed properties to false
            # self.callback.loaded = False
            self.callback.mInterstitialAd = None
            self.load_interstitial(UnitID)

    @run_on_ui_thread
    def load_interstitial(self, UnitID):
        """Loads an interstitial ad from AdMob Servers. This function takes a single
        argument, the ad UnitID. If you call this function when there is already an
        ad loaded, nothing will happen. This is done so as to prevent reloads of ads
        causing more network usage and possible suspicous network traffic report on your
        AdMob account
        """

        if not self.callback.loaded:
            builder = AdRequestBuilder().build()
            _InterstitialAd.load(
                context,
                UnitID,
                builder,
                self.callback,
            )
        else:
            Logger.info("KivAds: Interstitial Ad already Loaded and Ready to Show")

    @run_on_ui_thread
    def show(self, immersive=False):
        """Call this function to show your interstitial ad. Function will only run
        if an ad is already loaded or else nothing will happen. This function also takes
        one argument,`immersive`. When set to True your ad will be shown in immersive mode.
        This means the navigation bar and the notification bar wont be shown. By default
        this argument is False.
        """

        if self.callback.loaded:
            self.full_screen_callback.dismissed = False
            self.callback.mInterstitialAd.setFullScreenContentCallback(
                self.full_screen_callback
            )
            if immersive:
                self.callback.mInterstitialAd.setImmersiveMode(True)
            self.callback.mInterstitialAd.show(mActivity)
            self.callback.loaded = False
        else:
            Logger.warning("KivAds: The ad hasn't loaded yet. Not showing")

    def is_loaded(self):
        """Returns if the ad is loaded"""

        return self.callback.loaded

    def is_dismissed(self):
        """
        Returns if the ad was dismissed by pressing the close button
        """

        if self.full_screen_callback.dismissed:
            return True
        else:
            False


class KivAds:
    """This is the main class that you need for implementing KivAds into your application.
    This class initializes the connection with admob servers and allows that app session to show ads.
    It is suggested to instance this class in the `on_build` method in your kivy app.

    KivAds class takes one argument, `show_child`. Setting this argument to True will make
    your app show only child ads for that app session. By default this value is set to False.

    Remember to properly read Google Admob policies on showing ads to people under the age of 18.
    KivAds assumes no responsiblity if you do not comply with Google Family policy and/or Admob Child Policies.
    It is your job to ensure that the age appropriate ads are shown to your audience.
    """

    initialized = False
    """ Read only property that will depict if KivAds has connected to Admob servers successfully
    """

    def __init__(self, show_child=False, *args):
        if platform == "android":
            Logger.info("KivAds: Running on Android")
            self.initialize_connection(show_child)
        else:
            Logger.warning("KivAds: Not on android, Ads will not be shown")

    def initialize_connection(self, show_child):
        Logger.info("KivAds: Initializing Google SDK connection")
        self.initialized = True
        if show_child:
            requestConfiguration = (
                RequestConfigurationBuilder()
                .setTagForChildDirectedTreatment(
                    RequestConfiguration.TAG_FOR_CHILD_DIRECTED_TREATMENT_TRUE
                )
                .build()
            )
        else:
            requestConfiguration = (
                RequestConfigurationBuilder()
                .setTagForChildDirectedTreatment(
                    RequestConfiguration.TAG_FOR_CHILD_DIRECTED_TREATMENT_FALSE
                )
                .build()
            )
        MobileAds.setRequestConfiguration(requestConfiguration)
        MobileAds.initialize(context)

    def is_intialized(self):
        return self.initialized

    """ Returns whether the KivAds has initialized the connection to AdMob Servers
    """


class TestId:

    """This class contains various testids that can be used while you are tesing your app.
    Remeber to change these when you do the final build for your app or you won't earn any money.

    """

    INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"
    """ Test id for Interstitial ads
    """
