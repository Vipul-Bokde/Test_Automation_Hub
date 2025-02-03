package libraries;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class AlertsAndFrames {

	private WebDriver driver;

	// Constructor to initialize WebDriver
	public AlertsAndFrames(WebDriver driver) {
		this.driver = driver;
	}

	// Switch to a specific frame using locator type and locator
	public void switchToFrame(String locatorType, String locator) {
		WebElement element = locateElement(locatorType, locator);
		driver.switchTo().defaultContent(); // Switch to the default content before moving to the frame
		driver.switchTo().frame(element); // Switch to the desired frame
	}

	// Accept an alert (click OK)
	public void alertOk() {
		Alert alert = driver.switchTo().alert();
		alert.accept(); // Clicks "OK" on the alert
	}

	// Get the text from the alert
	public String alertGetText() {
		Alert alert = driver.switchTo().alert();
		return alert.getText(); // Returns the text of the alert
	}

	// Dismiss an alert (clicks "Cancel" or "No")
	public void alertDismiss() {
		Alert alert = driver.switchTo().alert();
		alert.dismiss(); // Clicks "Cancel" or dismisses the alert
	}

	// Utility method to locate element based on locator type (ID, Xpath, etc.)
	private WebElement locateElement(String locatorType, String locator) {
		switch (locatorType.toLowerCase()) {
		case "id":
			return driver.findElement(By.id(locator));
		case "name":
			return driver.findElement(By.name(locator));
		case "xpath":
			return driver.findElement(By.xpath(locator));
		case "css":
			return driver.findElement(By.cssSelector(locator));
		case "class":
			return driver.findElement(By.className(locator));
		case "tag":
			return driver.findElement(By.tagName(locator));
		default:
			throw new IllegalArgumentException("Locator type not supported: " + locatorType);
		}
	}
}
