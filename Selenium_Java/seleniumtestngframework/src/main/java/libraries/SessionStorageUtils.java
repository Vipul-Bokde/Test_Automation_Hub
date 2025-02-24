package libraries;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.JavascriptExecutor;

public class SessionStorageUtils {
    private WebDriver driver;

    public SessionStorageUtils(WebDriver driver) {
        this.driver = driver;
    }

    public void setLocalStorageItem(String key, String value) {
        ((JavascriptExecutor) driver).executeScript(String.format("localStorage.setItem('%s', '%s');", key, value));
    }

    public String getLocalStorageItem(String key) {
        return (String) ((JavascriptExecutor) driver).executeScript(String.format("return localStorage.getItem('%s');", key));
    }

    public void clearLocalStorage() {
        ((JavascriptExecutor) driver).executeScript("localStorage.clear();");
    }
}
