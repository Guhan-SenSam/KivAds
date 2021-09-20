RewardedInterstitial
====================

.. py:class:: RewardedInterstitial(self,UnitID,on_reward=None)

    This class represent a RewardedInterstitialAd Object. Instance this class to create
    a Rewarded Interstitial Ad.

    :param str UnitID: The UnitID for this Ad.

    :param function on_reward: The function to executed when an user completes watching the reward ad(i.e. earns the reward)

    .. py:function:: __init__(self,UnitID, on_reward=None)

        :param str UnitID: The UnitID for this Ad.

        :param function on_reward: The function to executed when an user completes watching the reward ad(i.e. earns the reward)

        Constructor function

    .. py:function:: load(self,UnitID)

        :param str UnitID: The UnitID for this Ad.

        Loads an reward video ad from AdMob Servers. If you call this function when there is already an
        ad loaded, nothing will happen. This is done so as to prevent reloads of ads
        causing more network usage and possible suspicous network traffic report on your
        AdMob account. This function is auto called when instancing the class.

    .. py:function:: show(self, immersive=False)

        :param boolean optional immersive:
            If the ad should be shown in immersive mode or not. If set to True the ad will be
            shown without a navigation bar and notification shade. By default it is set to False.

        Call this function to show your reward video ad. Function will only run
        if an ad is already loaded or else nothing will happen.

    .. py:function:: is_loaded(self)

        :rtype: boolean

        Returns whether the interstitial ad has been loaded from AdMob servers.

    .. py:function:: is_dismissed(self)

        :rtype: boolean

        Returns if the interstitial ad was dismissed by pressing the close button.

    .. py:function:: get_reward_amount(self)

        :rtype: string

        Returns the amount of reward that the user has received

    .. py:function:: get_reward_type(self):

        :rtype: int

        Returns the type of reward the user has received.
