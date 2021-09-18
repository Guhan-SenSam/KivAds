from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.utils import platform
from kivy.core.window import Window

from kivymd.app import MDApp
from kivymd.uix.card import MDCard
from kivymd.toast import toast

from kivads import KivAds, TestId, InterstitialAd

Builder.load_string(
    """
<MainScreen>:
    GridLayout:
        cols:1
        MDToolbar:
            title:"KivAds"
        ScrollView:
            GridLayout:
                cols:1
                spacing:dp(20)
                padding:dp(10)
                height:self.minimum_height
                size_hint_y:None
                CardElement:
                    main_text:"Interstitial Ads"
                    secondary_text:"Full-screen ads that cover the interface of an app until closed by the user."
                    image:"assets/interstitial.png"
                    on_release:app.interstitial.show()
                CardElement:
                    main_text:"Banner Ads"
                    secondary_text:"Rectangular ads that appear at the top or bottom of the device screen. Banner ads stay on screen while users are interacting with the app"
                    image:"assets/banner.png"
                CardElement:
                    main_text:"Rewarded Ads"
                    secondary_text:"Ads that reward users for watching short videos and interacting with playable ads and surveys"
                    image:"assets/rewarded.png"
                CardElement:
                    main_text:"Native Ads"
                    secondary_text:"Customizable ads that match the look and feel of your app. You decide how and where they're placed."
                    image:"assets/native.png"

                CardElement:
                    main_text:"Reload Ads"
                    on_release:app.reload_ads(app)




<CardElement>:
    size_hint:1,None
    padding:dp(5)
    image:None
    main_text:""
    secondary_text:""
    md_bg_color:app.theme_cls.accent_dark
    radius:dp(20)
    spacing:dp(5)
    height:dp(200)

    Image:
        source:root.image
        height:root.height - dp(20)
        size_hint:.25,1


    BoxLayout:
        orientation:'vertical'
        size_hint:.75,1

        Label:
            text:root.main_text
            size_hint:None,.2
            size:self.texture_size
            text_size:self.parent.width,self.parent.height/2
            color:0,0,0,1


        Label:
            text:root.secondary_text
            size_hint:None,.8
            size:self.texture_size
            text_size:self.parent.width,self.parent.height/2
            color:0,0,0,.6
            font_size:'16sp'






"""
)


class MainScreen(Screen):
    pass


class MainApp(MDApp):
    def build(self):
        self.ads = KivAds()
        self.interstitial = InterstitialAd(TestId.INTERSTITIAL)
        return MainScreen()

    def reload_ads(self, *args):
        toast("Reloading Ad")
        self.interstitial = InterstitialAd(TestId.INTERSTITIAL)


class CardElement(MDCard):
    pass


if platform != "android":
    Window.size = (360, 800)
if __name__ == "__main__":
    MainApp().run()
