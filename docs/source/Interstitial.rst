InterstitialAd
==============

.. py:class:: InterstitialAd(self, UnitID)

    Represents an Interstitial Ad Object. Instance this class in order to create and show
    an interstitial ad. This class is designed to only be used once, meaning
    after you call the `show()` method you should disregard this class. If you need to
    show another interstitial ad then again instance this class. Do not attempt to reuse the
    same class as ads will not be shown.

    :param str UnitID: The UnitID for this Ad.

    .. py:function:: __init__(self,UnitID)

        :param str UnitID: The UnitID for this Ad.

        Constructor function

    .. py:function:: load(self,UnitID)

        :param str UnitID: The UnitID for this Ad.

        Loads an interstitial ad from AdMob Servers. If you call this function when there is already an
        ad loaded, nothing will happen. This is done so as to prevent reloads of ads
        causing more network usage and possible suspicous network traffic report on your
        AdMob account. This function is auto called when instancing the class.

    .. py:function:: show(self, immersive=False)

        :param boolean optional immersive:
            If the ad should be shown in immersive mode or not. If set to True the ad will be
            shown without a navigation bar and notification shade. By default it is set to False.

        Call this function to show your interstitial ad. Function will only run
        if an ad is already loaded or else nothing will happen.

    .. py:function:: is_loaded(self)

        :rtype: boolean

        Returns whether the interstitial ad has been loaded from AdMob servers.

    .. py:function:: is_dismissed(self)

        :rtype: boolean

        Returns if the interstitial ad was dismissed by pressing the close button.
