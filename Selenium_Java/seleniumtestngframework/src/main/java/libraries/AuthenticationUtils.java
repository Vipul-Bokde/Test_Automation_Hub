package libraries;

import org.openqa.selenium.WebDriver;
import utilities.ExtentReportManager;

public class AuthenticationUtils {

    private WebDriver driver;

    public AuthenticationUtils(WebDriver driver) {
        this.driver = driver;
    }

    public void handleBasicAuth(String username, String password) {
        String url = driver.getCurrentUrl();
        String authUrl = url.replaceFirst("://", "://" + username + ":" + password + "@");
        driver.get(authUrl);
        ExtentReportManager.logInfo("Handled basic authentication for URL: " + url);
    }
}