package libraries;
import org.openqa.selenium.By;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.FluentWait;
import org.openqa.selenium.support.ui.WebDriverWait;
import java.time.Duration;
import java.util.concurrent.Callable;
import org.awaitility.Awaitility;

import utilities.ExtentReportManager;

public class SynchronisationAndWaitsUtils {

    private WebDriver driver;

    public SynchronisationAndWaitsUtils(WebDriver driver) {
        this.driver = driver;
    }

    // --- Explicit Waits (WebDriverWait) ---

    public WebElement waitForPresenceOfElement(By locator, int waitTimeInSeconds) {
        try {
            return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
                    .until(ExpectedConditions.presenceOfElementLocated(locator));
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }
    }

    public WebElement waitForVisibilityOfElement(By locator, int waitTimeInSeconds) {
        try {
            return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
                    .until(ExpectedConditions.visibilityOfElementLocated(locator));
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }
    }

    public WebElement waitForElementToBeClickable(By locator, int waitTimeInSeconds) {
        try {
            return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
                    .until(ExpectedConditions.elementToBeClickable(locator));
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }
    }

    public void waitForInvisibilityOfElement(By locator, int waitTimeInSeconds) {
        try {
            new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
                    .until(ExpectedConditions.invisibilityOfElementLocated(locator));
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }
    }

    // --- Fluent Wait ---

    public WebElement fluentWaitForElement(By locator, int timeoutSeconds, int pollingSeconds) {
        try {
            return new FluentWait<>(driver)
                    .withTimeout(Duration.ofSeconds(timeoutSeconds))
                    .pollingEvery(Duration.ofSeconds(pollingSeconds))
                    .ignoring(NoSuchElementException.class)
                    .until(ExpectedConditions.presenceOfElementLocated(locator));
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }
    }

    // --- Awaitility Waits ---

    public void awaitForCondition(Callable<Boolean> condition, int timeoutSeconds, int pollIntervalMillis) {
        try {
            Awaitility.await()
                    .atMost(Duration.ofSeconds(timeoutSeconds))
                    .pollInterval(Duration.ofMillis(pollIntervalMillis))
                    .until(condition);
        } catch (Exception e) {
            ExtentReportManager.logException(e);
            throw e;
        }
    }
}