package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import utilities.ExtentReportManager;

public class MouseActionsUtils {

	private WebDriver driver;
	private static final int DEFAULT_TIMEOUT = 10;
	private SynchronisationAndWaitsUtils syncwaits;

	public MouseActionsUtils(WebDriver driver) {
		this.driver = driver;
		this.syncwaits = new SynchronisationAndWaitsUtils(driver);
	}

	public void clickOnElement(By locator) {
		try {
			WebElement element = syncwaits.waitForElementToBeClickable(locator, DEFAULT_TIMEOUT);
			highlightElement(driver, element, "yellow");
			element.click();
			ExtentReportManager.logInfo("Clicked on element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e; // Re-throw to fail the test
		}
	}

	public void clickActionOnElement(By locator) {
		try {
			WebElement element = syncwaits.waitForVisibilityOfElement(locator, DEFAULT_TIMEOUT);
			Actions actions = new Actions(driver);
			actions.moveToElement(element).click(element).perform();
			ExtentReportManager.logInfo("Clicked (using Actions) on element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public void doubleClickOnElement(By locator) {
		try {
			WebElement element = syncwaits.waitForVisibilityOfElement(locator, DEFAULT_TIMEOUT);
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
			WebElement element = syncwaits.waitForVisibilityOfElement(locator, DEFAULT_TIMEOUT);
			Actions actions = new Actions(driver);
			actions.moveToElement(element).perform();
			ExtentReportManager.logInfo("Scrolled to element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	public void scrollInWebPage(int positionX, int positionY) {
		try {
			String script = "window.scrollBy(" + positionX + "," + positionY + ")";
			((JavascriptExecutor) driver).executeScript(script);
			ExtentReportManager.logInfo("Scrolled in web page: x=" + positionX + ", y=" + positionY);
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	private void highlightElement(WebDriver driver, WebElement element, String color) {
		if (driver instanceof JavascriptExecutor) {
			JavascriptExecutor js = (JavascriptExecutor) driver;
			js.executeScript("arguments[0].style.backgroundColor = '" + color + "'", element);

			// Optional: Briefly pause to see the highlight (for demonstration)
			try {
				Thread.sleep(500); // Adjust duration as needed
				js.executeScript("arguments[0].style.backgroundColor = ''", element); // Reset the color after click
			} catch (InterruptedException e) {
				Thread.currentThread().interrupt(); // Restore interrupt status
			}
		}
	}
}