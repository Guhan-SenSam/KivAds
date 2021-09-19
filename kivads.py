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


class RewardedAd:
    """This class represent a RewardedVideoAd Object. Instance this class to create
    a RewardedVideo Ad. This class takes two arguments, `UnitID` and on_reward.
    `UnitID`: The UnitID for this ad.
    `on_reward`: A method to be called when an user completely watches the reward video ad.
    """

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
        """This function is used to load the reward ad. You don't need to call this
        as when you instance the class it is auto ran. If ad is already loaded nothing
        will happen.
        """

        if not self.callback.loaded:
            builder = AdRequestBuilder().build()
            _RewardedAd.load(context, UnitID, builder, self.callback)
        else:
            Logger.info("KivAds: Interstitial Ad already Loaded and Ready to Show")

    @run_on_ui_thread
    def show(self, immersive=False):
        """Show your reward video ad. Takes one argument `immersive`. When set to
        True your ad will be shown without the navigation drawer and the notification shade.
        Function will only run if an ad is already loaded or else nothing will happen.
        """

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
        """Call this function to check if the reward video ad has been loaded"""
        return self.callback.loaded

    def is_dismissed(self):
        """
        Returns if the ad was dismissed by pressing the close button
        """

        if self.full_screen_callback.dismissed:
            return True
        else:
            False

    def get_reward_amount(self):
        """Returns the reward amount"""
        return self.reward_listener.reward.getAmount()

    def get_reward_type(self):
        """Returns the reward type"""
        return self.reward_listener.reward.getType()


class BannerAd:
    """This class represents a BannerAd Object. Instance this class to create a banner ad object.
    You can reuse this class as the refreshing of banner ads is controlled by AdMob servers from
    your AdMob console webpage. The BannerAd class takes three arguments,
    UnitId: The UnitId of the Banner ad

    size: This argument allows you to set the size of the banner ad. You can choose between
    pre defined sizes, an adaptive size(using Google Adaptive Banner Ads) or your own size.
    The available predefined sizes are ['BANNER','LARGE_BANNER','MEDIUM_RECTANGLE','LEADERBOARD'].
    If using adaptive banner size then pass an integer for the size argument. This will set the width
    of the ad to whatever integer you passed and will automatically compute the required height based on
    the device density. If you want to set your own size, then pass a tuple of width x height in pixels to
    the size argument. By default the size is set to `SMART_BANNER`.
    Check here for more info: `https://developers.google.com/admob/android/banner#banner_sizes`

    bottom: This is a boolean argument. If set to True, it will cause the banner ad to be shown at the
    bottom of the screen. By default it is set to False.
    """

    adview = AdView(context)

    adlistener = BListener()

    showing = False
    """ This is a read only property that will return True if the banner ad is
    currently being shown on screen. Or else it will return False
    """

    def __init__(self, UnitID, size=None, bottom=False):
        if platform == "android":
            Logger.info("KivAds: Loading Banner Ad")
            self.adlistener.loaded = False
            self.load(UnitID, size, bottom)

    @run_on_ui_thread
    def load(self, UnitID, size, bottom):
        """
        Function to load the banner ad. There is no need to call this manually
        it will be called automattically when instancing the class
        """
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
        """
        Call this function to show the banner ad. If no ad was loaded warning will be
        raised and nothing will happen. If banner ad is already showing, nothing will
        happen
        """

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
        """
        Hides the banner ad from screen
        """

        self.adview.setVisibility(View.GONE)
        self.showing = False

    def is_loaded(self):
        """
        Returns if the banner ad was loaded
        """

        return self.adlistener.loaded

    def is_clicked(self):
        """
        Returns if the banner ad was clicked
        """

        return self.adlistener.clicked


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

    full_screen_callback = FullScreenContentCallback()

    def __init__(self, UnitID):
        if platform == "android":
            Logger.info("KivAds: Loading Interstitial Ad")
            self.callback.loaded = False
            self.callback.mInterstitialAd = None
            self.load(UnitID)

    @run_on_ui_thread
    def load(self, UnitID):
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
            Logger.info("KivAds:Interstitial Ad already Loaded and Ready to Show")

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
            Logger.warning("KivAds:The ad hasn't loaded yet. Not showing")

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

    KivAds class takes three argument, `show_child`,`rating` and `test_id`.
    Setting 'show_child' argument to True will make
    your app show only child ads for that app session. By default this value is set to False. Setting it to
    None will discole to AdMob that you have not specified if you want to show child ads or not. I recommend
    to keep this at True or False(if u target above age 18) and not at None.

    The `rating` argument takes a string to represnt the maximum rating of ads that your app will show during that
    session. The available options are ['G','PG','T','MA']. By default the rating level is set to None. Meaning
    your app will use th rating level set in your AdMob we console.

    Remember to properly read Google Admob policies on showing ads to people under the age of 18.
    KivAds assumes no responsiblity if you do not comply with Google Family policy and/or Admob Child Policies.
    It is your job to ensure that the age appropriate ads are shown to your audience.

    If you want to set your device as a testing device. Pass its ad id throught the argument `test_id`. This will
    add it as a test device for the duration of the app session.
    """

    initialized = False
    """ Read only property that will depict if KivAds has connected to Admob servers successfully
    """

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

    """ Returns whether the KivAds has initialized the connection to AdMob Servers
    """


class TestId:

    """This class contains various testids that can be used while you are tesing your app.
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
