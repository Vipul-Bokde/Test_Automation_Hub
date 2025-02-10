package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import utilities.ExtentReportManager;

import java.time.Duration;

public class MouseActions {

	private WebDriver driver;
	private static final int DEFAULT_TIMEOUT = 10; // Consistent timeout

	public MouseActions(WebDriver driver) {
		this.driver = driver;
	}

	public void clickOnElement(By locator) {
		try {
			WebElement element = waitForClickable(locator, DEFAULT_TIMEOUT);
			element.click();
			ExtentReportManager.logInfo("Clicked on element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e; // Re-throw to fail the test
		}
	}

	public void clickActionOnElement(By locator) {
		try {
			WebElement element = waitForVisibility(locator, DEFAULT_TIMEOUT); // Wait for visibility
//            highlight(element);
			Actions actions = new Actions(driver);
			actions.moveToElement(element).click(element).perform();
			ExtentReportManager.logInfo("Clicked (using Actions) on element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

//    public void clickJsOnElement(By locator) {
//        try {
//            WebElement element = waitForVisibility(locator, DEFAULT_TIMEOUT); // Ensure element is present
//            driver.executeScript("arguments[0].click();", element);
//            ExtentReportManager.logInfo("Clicked (using JS) on element: " + locator);
//        } catch (Exception e) {
//             ExtentReportManager.logException(e);
//            throw e;
//        }
//    }

	public void doubleClickOnElement(By locator) {
		try {
			WebElement element = waitForVisibility(locator, DEFAULT_TIMEOUT);
//            highlight(element);
			Actions actions = new Actions(driver);
			actions.doubleClick(element).perform();
			ExtentReportManager.logInfo("Double-clicked on element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public void scrollToElement(By locator) {
		try {
			WebElement element = waitForVisibility(locator, DEFAULT_TIMEOUT);
//            highlight(element);
			Actions actions = new Actions(driver);
			actions.moveToElement(element).perform();
			ExtentReportManager.logInfo("Scrolled to element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

//    public void scrollToElementJavascript(By locator) {
//        try {
//             WebElement element = waitForVisibility(locator, DEFAULT_TIMEOUT);
//            driver.executeScript("arguments[0].scrollIntoView();", element);
//            ExtentReportManager.logInfo("Scrolled to element (JS): " + locator);
//        } catch (Exception e) {
//             ExtentReportManager.logException(e);
//            throw e;
//        }
//    }

	public void scrollInWebPage(int positionX, int positionY) { // Use int for positions
		try {
			String script = "window.scrollBy(" + positionX + "," + positionY + ")";
//            driver.executeScript(script);
			ExtentReportManager.logInfo("Scrolled in web page: x=" + positionX + ", y=" + positionY);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

//    public void scrollToDownTheWebPage() {
//        try {
//            String script = "window.scrollTo(0, document.body.scrollHeight)";
//            driver.executeScript(script);
//            ExtentReportManager.logInfo("Scrolled to bottom of web page.");
//        } catch (Exception e) {
//             ExtentReportManager.logException(e);
//            throw e;
//        }
//    }

	public boolean checkElementDisplayed(By locator) {
		try {
			WebElement element = waitForVisibility(locator, DEFAULT_TIMEOUT);
//             highlight(element);
			Actions actions = new Actions(driver);
			actions.moveToElement(element).perform();
			boolean isDisplayed = element.isDisplayed();
			ExtentReportManager.logInfo("Element " + locator + " is displayed: " + isDisplayed);
			return isDisplayed;
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			return false; // Or throw if you want the test to fail
		}
	}

	// Helper Methods (You'll likely have these in Locators or a similar class)

	private WebElement waitForVisibility(By locator, int waitTimeInSeconds) {
		try {
			return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
					.until(ExpectedConditions.visibilityOfElementLocated(locator));
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	private WebElement waitForClickable(By locator, int waitTimeInSeconds) {
		try {
			return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
					.until(ExpectedConditions.elementToBeClickable(locator));
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

//    private void highlight(WebElement element) {
//        // Your highlight implementation (if you have one)
//        if (element != null) {
//        try {
//            String originalStyle = element.getAttribute("style");
//            driver.executeScript("arguments[0].setAttribute('style', arguments[1]);", element, "border: 2px solid red;");
//
//            // You can add a short pause here if you want the highlight to be visible longer
//            Thread.sleep(200); // 0.2 seconds
//
//            driver.executeScript("arguments[0].setAttribute('style', arguments[1]);", element, originalStyle);
//        } catch (Exception e) {
//            ExtentReportManager.logException(e);
//        }
//    }
//    }
}