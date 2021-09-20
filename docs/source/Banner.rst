BannerAd
========

.. py:class:: BannerAd(self, UnitID, size=None, bottom=False)

    This class represents a BannerAd Object. Instance this class to create a banner ad object.
    You can reuse this class as the refreshing of banner ads is controlled by AdMob servers from
    your AdMob console webpage.

    :param str UnitID: The UnitID for this Ad.

    :param [string,int,tuple] size:
        Set the size of the banner ad. You can choose between pre defined sizes, an adaptive size(using Google Adaptive Banner Ads)
        or your own size.

        The available predefined sizes are ['BANNER','LARGE_BANNER','MEDIUM_RECTANGLE','LEADERBOARD'].\n

        If using adaptive banner size then pass an integer for the size argument. This will set the width
        of the ad to whatever integer you passed and will automatically compute the required height based on
        the device density.

        If you want to set your own size, then pass a tuple of width x height in pixels to
        the size argument.

        By default the size is set to `SMART_BANNER`.
        Check here for more info: `<https://developers.google.com/admob/android/banner#banner_sizes>`_

    :param boolean bottom:
        If set to True, it will cause the banner ad to be shown at the bottom of the screen. By default it is set to False.

    .. py:attribute:: showing
        :type: boolean
        :value: False

        Read only property that will return True if the banner ad is currently being shown on screen. Or else it will return False.

    .. py:function:: __init__(self,UnitID,size=None,bottom=False)

        Constructor Function

    .. py:function:: load(self,UnitID,size=None,bottom=False)

        :param str UnitID: The UnitID for this Ad.

        :param [string,int,tuple] size:
            Set the size of the banner ad. You can choose between pre defined sizes, an adaptive size(using Google Adaptive Banner Ads)
            or your own size.

            The available predefined sizes are ['BANNER','LARGE_BANNER','MEDIUM_RECTANGLE','LEADERBOARD'].\n

            If using adaptive banner size then pass an integer for the size argument. This will set the width
            of the ad to whatever integer you passed and will automatically compute the required height based on
            the device density.

            If you want to set your own size, then pass a tuple of width x height in pixels to
            the size argument.

            By default the size is set to `SMART_BANNER`.
            Check here for more info: `<https://developers.google.com/admob/android/banner#banner_sizes>`_

        :param boolean bottom:
            If set to True, it will cause the banner ad to be shown at the bottom of the screen. By default it is set to False.

        Loads a banner ad from AdMob Servers. If you call this function when there is already an
        ad loaded, nothing will happen. This is done so as to prevent reloads of ads
        causing more network usage and possible suspicous network traffic report on your
        AdMob account. This function is auto called when instancing the class.


    .. py:function:: show(self)

        Call this function to show your banner ad. Function will only run
        if an ad is already loaded or else nothing will happen. Function will not run
        if the banner ad is already showing.

    .. py:function:: hide(self)

        Hides the banner ad from the screen

    .. py:function:: is_loaded(self)

        :rtype: boolean

        Returns whether the banner ad has been loaded from AdMob servers.

    .. py:function:: is_clicked(self)

        :rtype: boolean

        Returns if the banner ad was clicked
