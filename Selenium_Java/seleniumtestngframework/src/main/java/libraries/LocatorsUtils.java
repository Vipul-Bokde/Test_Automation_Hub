package libraries;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

import utilities.ExtentReportManager;

import java.time.Duration;
import java.util.List;

public class LocatorsUtils {

	private WebDriver driver;
	private static final int DEFAULT_TIMEOUT = 10;

	public LocatorsUtils(WebDriver driver) {
		this.driver = driver;
	}

	// Get a single element
	public WebElement getElement(By locator, int waitTimeInSeconds) {
		try {
			return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
					.until(ExpectedConditions.presenceOfElementLocated(locator));
		} catch (Exception e) {
			ExtentReportManager.logException(e); // Log the exception automatically
			throw e;
		}
	}

	// Get a list of elements
	public List<WebElement> getElements(By locator, int waitTimeInSeconds) {
		try {
			return new WebDriverWait(driver, Duration.ofSeconds(waitTimeInSeconds))
					.until(ExpectedConditions.presenceOfAllElementsLocatedBy(locator));
		} catch (Exception e) {
			ExtentReportManager.logException(e);
			throw e;
		}
	}

	// Wrapper method for sendKeys
	public void sendKeys(By locator, String value) {
		try {
			WebElement element = driver.findElement(locator);
			element.clear();
			element.sendKeys(value);
			ExtentReportManager.logInfo("Sent value '" + value + "' to element: " + locator);
		} catch (Exception e) {
			ExtentReportManager.logException(e); // Log the exception automatically
			throw e; // Re-throw the exception to ensure test failure
		}
	}

	public String getText(By locator) {
		try {
			WebElement element = driver.findElement(locator);
			String text = element.getText();
			ExtentReportManager.logInfo("Retrieved text from element: " + text);
			return text;
		} catch (Exception e) {
			ExtentReportManager.logException(e); // Log the exception automatically
			throw e; // Re-throw the exception to ensure test failure
		}
	}

	// Check if an element exists
	public boolean elementExists(By locator) {
		try {
			return driver.findElements(locator).size() > 0;
		} catch (Exception e) {
			return false;
		}
	}

	// Check if an element is displayed
	public boolean elementIsDisplayed(By locator) {
		try {
			WebElement element = getElement(locator, DEFAULT_TIMEOUT);
			return element != null && element.isDisplayed();
		} catch (Exception e) {
			return false;
		}
	}

	// Check if an element is selected
	public boolean elementSelected(By locator) {
		try {
			WebElement element = getElement(locator, DEFAULT_TIMEOUT);
			return element != null && element.isSelected();
		} catch (Exception e) {
			return false;
		}
	}

}
