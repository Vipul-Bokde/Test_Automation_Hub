package libraries;

import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
// ... other imports

public class JavaScriptsUtils {
    private WebDriver driver;

    public JavaScriptsUtils(WebDriver driver) {
        this.driver = driver;
    }

    public void executeJS(String script) {
        ((JavascriptExecutor) driver).executeScript(script);
    }

    public Object executeJSWithReturnValue(String script, Object... args) {
        return ((JavascriptExecutor) driver).executeScript(script, args);
    }

    public void scrollToElement(WebElement element) {
        ((JavascriptExecutor) driver).executeScript("arguments[0].scrollIntoView(true);", element);
    }
}