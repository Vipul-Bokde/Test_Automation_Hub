// libraries.BrowserActions.java
package libraries;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchWindowException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import java.util.ArrayList;
import java.util.List;

import utilities.ExtentReportManager;

public class BrowserActionsUtils {

    private WebDriver driver;
    private LocatorsUtils locators;

    public BrowserActionsUtils(WebDriver driver) {
        this.driver = driver;
        this.locators = new LocatorsUtils(driver);
    }

    // --- Basic Navigation ---

    public void refresh() {
        driver.navigate().refresh();
        ExtentReportManager.logInfo("Refreshed the page.");
    }

    public void quitBrowser() {
        driver.quit();
        ExtentReportManager.logInfo("Quit the browser.");
    }

    public void closeBrowser() {
        driver.close();
        ExtentReportManager.logInfo("Closed the browser window/tab.");
    }

    public void goBack() {
        driver.navigate().back();
        ExtentReportManager.logInfo("Navigated back.");
    }

    public void goForward() {
        driver.navigate().forward();
        ExtentReportManager.logInfo("Navigated forward.");
    }

    public void maximizeWindow() {
        driver.manage().window().maximize();
        ExtentReportManager.logInfo("Maximized the window.");
    }

    public void openURL(String url) {
        driver.get(url);
        ExtentReportManager.logInfo("Opened URL: " + url);
    }

    // --- Advanced Navigation (Iframes, New Tabs/Windows) ---

    public void switchToFrame(By locator) {
        WebElement element = locators.getElement(locator, 10); // Wait up to 10 seconds
        driver.switchTo().defaultContent();
        driver.switchTo().frame(element);
        ExtentReportManager.logInfo("Switched to frame: " + locator);
    }

    public void switchToFrame(int index) {
        driver.switchTo().frame(index);
        ExtentReportManager.logInfo("Switched to frame with index: " + index);
    }

    public void switchToFrame(String nameOrId) {
        driver.switchTo().frame(nameOrId);
        ExtentReportManager.logInfo("Switched to frame with name or ID: " + nameOrId);
    }

    public void switchToDefaultContent() {
        driver.switchTo().defaultContent();
        ExtentReportManager.logInfo("Switched to default content.");
    }

    public void switchToParentFrame() {
        driver.switchTo().parentFrame();
        ExtentReportManager.logInfo("Switched to parent frame.");
    }

    public void openNewTab(String url) {
        driver.switchTo().newWindow(org.openqa.selenium.WindowType.TAB);
        List<String> tabs = new ArrayList<>(driver.getWindowHandles());
        driver.switchTo().window(tabs.get(tabs.size() - 1));
        driver.get(url);
        ExtentReportManager.logInfo("Opened new tab: " + url);
    }

    public void switchToTab(int index) {
        List<String> tabs = new ArrayList<>(driver.getWindowHandles());
        if (index >= 0 && index < tabs.size()) {
            driver.switchTo().window(tabs.get(index));
            ExtentReportManager.logInfo("Switched to tab: " + index);
        } else {
            String errorMessage = "Invalid tab index: " + index;
            ExtentReportManager.logFail(errorMessage);
            throw new IndexOutOfBoundsException(errorMessage);
        }
    }

    public void switchToWindow(String windowTitle) {
        for (String handle : driver.getWindowHandles()) {
            driver.switchTo().window(handle);
            if (driver.getTitle().contains(windowTitle)) {
                ExtentReportManager.logInfo("Switched to window: " + windowTitle);
                return;
            }
        }
        String errorMessage = "Window with title '" + windowTitle + "' not found.";
        ExtentReportManager.logFail(errorMessage);
        throw new NoSuchWindowException(errorMessage);
    }

    public String getCurrentUrl() {
        String currentURL = driver.getCurrentUrl();
        ExtentReportManager.logInfo("Current URL is: " + currentURL);
        return currentURL;
    }

    public String getTitle() {
        String title = driver.getTitle();
        ExtentReportManager.logInfo("Page Title is: " + title);
        return title;
    }

    public void acceptAlert() {
        try {
            Alert alert = driver.switchTo().alert();
            alert.accept();
            ExtentReportManager.logInfo("Accepted alert.");
        } catch (Exception e) {
            ExtentReportManager.logFail("No alert was present to accept");
        }
    }

    public void dismissAlert() {
        try {
            Alert alert = driver.switchTo().alert();
            alert.dismiss();
            ExtentReportManager.logInfo("Dismissed alert.");
        } catch (Exception e) {
            ExtentReportManager.logFail("No alert was present to dismiss");
        }
    }

    public String getAlertText() {
        try {
            Alert alert = driver.switchTo().alert();
            String alertText = alert.getText();
            ExtentReportManager.logInfo("Alert text: " + alertText);
            return alertText;
        } catch (Exception e) {
            ExtentReportManager.logFail("No alert was present to get the text from");
            return ""; // Or throw an exception if you prefer
        }
    }
}