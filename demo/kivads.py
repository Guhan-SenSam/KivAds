from kivy.logger import Logger
from kivy.metrics import dp
from kivy.properties import BooleanProperty
from kivy.utils import platform

if platform == "android":
    from android import PythonJavaClass, autoclass, java_method, mActivity
    from android.runnable import run_on_ui_thread

    context = mActivity.getApplicationContext()
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
    AdView = autoclass("com.google.android.gms.ads.AdView")
    BListener = autoclass("org.org.kivads.BListener")
    InterstitialCallback = autoclass("org.org.kivads.ICallback")
    FullScreenContentCallback = autoclass("org.org.kivads.FullScreen")
    Gravity = autoclass("android.view.Gravity")
    LayoutParams = autoclass("android.view.ViewGroup$LayoutParams")
    LinearLayout = autoclass("android.widget.LinearLayout")
    AdSize = autoclass("com.google.android.gms.ads.AdSize")
    View = autoclass("android.view.View")
    activity = autoclass("org.kivy.android.PythonActivity")
    _RewardedAd = autoclass("com.google.android.gms.ads.rewarded.RewardedAd")
    RewardCallback = autoclass("org.org.kivads.RCallback")
    _RewardedInterstitialAd = autoclass(
        "com.google.android.gms.ads.rewardedinterstitial.RewardedInterstitialAd"
    )
    RewardInterstitialCallback = autoclass("org.org.kivads.RICallback")


class RewardEarnedListener(PythonJavaClass):
    __javainterfaces__ = ["com/google/android/gms/ads/OnUserEarnedRewardListener"]

    __javacontext__ = "app"

    callback = None

    rewarded = False

    @java_method("(Lcom/google/android/gms/ads/rewarded/RewardItem;)V")
    def onUserEarnedReward(self, reward):
        self.reward = reward
        # Run the `on_reward` callback that the user has provided
        if self.callback:
            self.callback()
        self.rewarded = True


class RewardedInterstitial:

    callback = RewardInterstitialCallback()

    reward_listener = RewardEarnedListener()

    full_screen_callback = FullScreenContentCallback()

    def __init__(self, UnitID, on_reward=None):
        if platform == "android":
            Logger.info("KivAds: Loading Interstitial Rewarded Ad")
            self.on_reward = on_reward
            self.callback.loaded = False
            self.callback.mRewardedIinterstitialAd = None
            self.load(UnitID)

    @run_on_ui_thread
    def load(self, UnitID):

        if not self.callback.loaded:
            builder = AdRequestBuilder().build()
            _RewardedInterstitialAd.load(context, UnitID, builder, self.callback)
        else:
            Logger.info("KivAds: Interstitial Ad already Loaded and Ready to Show")

    @run_on_ui_thread
    def show(self, immersive=False):

        if self.callback.loaded:
            if immersive:
                self.callback.mRewardedInterstitialAd.setImmersiveMode(True)
            # If user has given a callback we set it here or else we leave it as None
            if self.on_reward:
                self.reward_listener.callback = self.on_reward
            # Set the full screen content callback
            self.full_screen_callback.dismissed = False
            self.callback.mRewardedInterstitialAd.setFullScreenContentCallback = (
                self.full_screen_callback
            )
            self.callback.mRewardedInterstitialAd.show(mActivity, self.reward_listener)
            self.callback.loaded = False
        else:
            Logger.info("KivAds:The ad hasn't loaded yet. Not showing")

    def is_loaded(self):
        return self.callback.loaded

    def is_dismissed(self):
        if self.full_screen_callback.dismissed:
            return True
        else:
            False

    def get_reward_amount(self):
        return self.reward_listener.reward.getAmount()

    def get_reward_type(self):
        return self.reward_listener.reward.getType()


class RewardedAd:

    callback = RewardCallback()

    reward_listener = RewardEarnedListener()

    full_screen_callback = FullScreenContentCallback()

    def __init__(self, UnitID, on_reward=None):
        if platform == "android":
            Logger.info("KivAds: Loading Rewarded Ad")
            self.on_reward = on_reward
            self.callback.loaded = False
            self.callback.mRewardedAd = None
            self.load(UnitID)

    @run_on_ui_thread
    def load(self, UnitID):
        if not self.callback.loaded:
            builder = AdRequestBuilder().build()
            _RewardedAd.load(context, UnitID, builder, self.callback)
        else:
            Logger.info("KivAds: Interstitial Ad already Loaded and Ready to Show")

    @run_on_ui_thread
    def show(self, immersive=False):
        if self.callback.loaded:
            if immersive:
                self.callback.mRewardedAd.setImmersiveMode(True)
            # If user has given a callback we set it here or else we leave it as None
            if self.on_reward:
                self.reward_listener.callback = self.on_reward
            # Set the full screen content callback
            self.full_screen_callback.dismissed = False
            self.callback.mRewardedAd.setFullScreenContentCallback = (
                self.full_screen_callback
            )
            self.callback.mRewardedAd.show(mActivity, self.reward_listener)
            self.callback.loaded = False
        else:
            Logger.info("KivAds:The ad hasn't loaded yet. Not showing")

    def is_loaded(self):
        return self.callback.loaded

    def is_dismissed(self):
        if self.full_screen_callback.dismissed:
            return True
        else:
            False

    def get_reward_amount(self):
        return self.reward_listener.reward.getAmount()

    def get_reward_type(self):
        return self.reward_listener.reward.getType()


class BannerAd:

    adview = AdView(context)

    adlistener = BListener()

    showing = False

    def __init__(self, UnitID, size=None, bottom=False):
        if platform == "android":
            Logger.info("KivAds: Loading Banner Ad")
            self.adlistener.loaded = False
            self.load(UnitID, size, bottom)

    @run_on_ui_thread
    def load(self, UnitID, size, bottom):
        if not self.adlistener.loaded:
            if isinstance(size, tuple):
                banner_size = AdSize(size[0], size[1])
            elif isinstance(size, int):
                banner_size = AdSize.getCurrentOrientationAnchoredAdaptiveBannerAdSize(
                    context, size / dp(1)
                )
            elif size == "BANNER":
                banner_size = AdSize.BANNER
            elif size == "LARGE_BANNER":
                banner_size = AdSize.LARGE_BANNER
            elif size == "MEDIUM_RECTANGLE":
                banner_size = AdSize.MEDIUM_RECTANGLE
            elif size == "FULL_BANNER":
                banner_size = AdSize.FULL_BANNER
            elif size == "LEADERBOARD":
                banner_size = AdSize.LEADERBOARD
            else:
                banner_size = AdSize.SMART_BANNER
            self.adview.setAdSize(banner_size)
            self.adview.setAdUnitId(UnitID)
            self.adview.setVisibility(View.GONE)
            self.adview.setAdListener(self.adlistener)

            layout = LinearLayout(context)
            layout.addView(self.adview)
            layoutParams = LayoutParams(
                LayoutParams.MATCH_PARENT, LayoutParams.MATCH_PARENT
            )
            layout.setLayoutParams(layoutParams)
            if bottom:
                layout.setGravity(Gravity.BOTTOM)
            activity.addContentView(layout, layoutParams)
            builder = AdRequestBuilder().build()
            self.adview.loadAd(builder)
        else:
            Logger.info(
                "KivAds: Banner Ad already loaded. Call show() method to display"
            )

    @run_on_ui_thread
    def show(self):
        if self.adlistener.loaded:
            if not self.showing:
                self.adview.setVisibility(View.VISIBLE)
                self.showing = True
            else:
                Logger.info(
                    "KivAds: Banner Ad already showing, Ignoring this function call"
                )
        else:
            Logger.info("KivAds: Banner Ad not loaded, not showing")

    @run_on_ui_thread
    def hide(self):
        self.adview.setVisibility(View.GONE)
        self.showing = False

    def is_loaded(self):
        return self.adlistener.loaded

    def is_clicked(self):
        return self.adlistener.clicked


class InterstitialAd:

    callback = InterstitialCallback()

    full_screen_callback = FullScreenContentCallback()

    def __init__(self, UnitID):
        if platform == "android":
            Logger.info("KivAds: Loading Interstitial Ad")
            self.callback.loaded = False
            self.callback.mInterstitialAd = None
            self.load(UnitID)

    @run_on_ui_thread
    def load(self, UnitID):
        if not self.callback.loaded:
            builder = AdRequestBuilder().build()
            _InterstitialAd.load(
                context,
                UnitID,
                builder,
                self.callback,
            )
        else:
            Logger.info("KivAds:Interstitial Ad already Loaded and Ready to Show")

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
            Logger.warning("KivAds:The ad hasn't loaded yet. Not showing")

    def is_loaded(self):
        return self.callback.loaded

    def is_dismissed(self):
        if self.full_screen_callback.dismissed:
            return True
        else:
            False


class KivAds:

    initialized = False

    def __init__(self, show_child=False, rating=None, test_id=None, *args):
        if platform == "android":
            Logger.info("KivAds: Running on Android")
            self.initialize_connection(show_child, rating, test_id)
        else:
            Logger.warning("KivAds: Not on android, Ads will not be shown")

    def initialize_connection(self, show_child, rating, test_id):
        Logger.info("KivAds: Initializing Google SDK connection")
        self.initialized = True
        # Set if to show child ads or not
        if show_child:
            requestConfiguration = (
                RequestConfigurationBuilder().setTagForChildDirectedTreatment(
                    RequestConfiguration.TAG_FOR_CHILD_DIRECTED_TREATMENT_TRUE
                )
            )
        else:
            requestConfiguration = (
                RequestConfigurationBuilder().setTagForChildDirectedTreatment(
                    RequestConfiguration.TAG_FOR_CHILD_DIRECTED_TREATMENT_FALSE
                )
            )
        # Set Content Rating levels
        if rating == "G":
            requestConfiguration.setMaxAdContentRating(
                RequestConfiguration.MAX_AD_CONTENT_RATING_G
            )
        elif rating == "PG":
            requestConfiguration.setMaxAdContentRating(
                RequestConfiguration.MAX_AD_CONTENT_RATING_PG
            )
        elif rating == "T":
            requestConfiguration.setMaxAdContentRating(
                RequestConfiguration.MAX_AD_CONTENT_RATING_T
            )
        elif rating == "MA":
            requestConfiguration.setMaxAdContentRating(
                RequestConfiguration.MAX_AD_CONTENT_RATING_MA
            )

        # Add the test devices if there are any
        if test_id:
            requestConfiguration.setTestDeviceIds(test_id)
        MobileAds.setRequestConfiguration(requestConfiguration.build())
        MobileAds.initialize(context)

    def is_intialized(self):
        return self.initialized


class TestID:

    """This class contains various TestIDs that can be used while you are tesing your app.
    Remeber to change these when you do the final build for your app or you won't earn any money.
    """

    INTERSTITIAL = "ca-app-pub-3940256099942544/1033173712"
    """ Test id for Interstitial ads
    """

    BANNER = "ca-app-pub-3940256099942544/6300978111"
    """ Test id for Banner Ads
    """

    REWARD = "ca-app-pub-3940256099942544/5224354917"
    """ Test id for Reward Video Ads
    """

    REWARD_INTERSTITIAL = "ca-app-pub-3940256099942544/5354046379"
    """ Test id for Reward Interstitial Ads
    """
