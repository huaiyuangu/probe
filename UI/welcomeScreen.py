
import framework.controls.Button;
import framework.controls.enums.FindBy;
import factory.ScreenFactory;
import io.appium.java_client.MobileElement;
import io.appium.java_client.pagefactory.AndroidFindBy;
import io.appium.java_client.pagefactory.iOSFindBy;

import BaseScreen


class WelcomeScreen (BaseScreen):
    def __init__(self):
        super(WelcomeScreen).__init__()
        self.setScreenName("Welcome Screem")
        self.start_up_login_button = self.loadButton("//*[contains(@resource-id,'secondary_button')]", FindBy.XPATH);
        self.dismiss_button = self.loadButton("//android.widget.Button[1]", FindBy.XPATH);

    def verifyScreen(self):
        self.logStep("Verifying Welcome page");
        self.verifyPage(self.start_up_login_button);
        return self

    def goToLoginScreen(self):
        self.logStep("Navigating to login page");
        self.start_up_login_button.touch();
        self.dismiss_button.exists();
        self.dismiss_button.touch();
        self._Login_Screen().verifyPage();
        return self

