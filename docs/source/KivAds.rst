KivAds
======

.. py:class:: KivAds(show_child=False, rating=None, test_id=None, *args)

    Main class for implementing KivAds into your application.
    Initializes the connection with admob servers and allows that app session to show ads.
    It is suggested to instance this class in the `on_build` method in your kivy app.


    :param boolean, optional show_child:
        Whether KivAds should show child ads for the duration of that app session. Make sure you follow
        Google Child Policy and Google Family Policy. KivAds is not responsible if your AdMob account gets
        terminated for not complying with these policies.

    :param str, optional rating:
        The maximum rating of ads to be shown in that session. Defaults to None, meaning the rating level set on your admob
        web console.

    :param str, optional test_id:
        A test_device ID you want to ad to this app session in order to show test ads.
        Defaults to None.

    .. py:attribute:: initialized
        :type: boolean
        :value: False

        Read only property that will depict if KivAds has connected to Admob servers successfully

    .. py:function:: __init__(self,show_child = False,rating=None, test_id=None,*args)

        Constructor Method. Called when instancing class.

    .. py:function:: initialize_connection(self, show_child, rating, test_id)

        :param boolean, optional show_child:
            Whether KivAds should show child ads for the duration of that app session. Make sure you follow
            Google Child Policy and Google Family Policy. KivAds is not responsible if your AdMob account gets
            terminated for not complying with these policies.

        :param str, optional rating:
            The maximum rating of ads to be shown in that session. Defaults to None, meaning the rating level set on your admob
            web console.

        :param str, optional test_id:
            A test_device ID you want to ad to this app session in order to show test ads. Defaults to None.

        Connect your app session with Admob Servers. This function must be called in order
        for your app to show ads. It is auto called when the class is instanced.

    .. py:function:: is_intialized(self)

        :rtype: boolean
        Returns whether the connection with KivMob servers has been initialized and completed.
