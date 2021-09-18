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

    callback = InterstitialCallback()

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
        return self.callback.loaded

    def is_dismissed(self):
        if self.full_screen_callback.dismissed:
            return True
        else:
            False

    def is_profit(self):
        return


class KivAds:

    initialized = False

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


class TestId:

    INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"
