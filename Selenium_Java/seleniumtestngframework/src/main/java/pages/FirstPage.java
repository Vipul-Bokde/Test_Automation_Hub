package pages;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import utilities.ExtentReportManager;

public class FirstPage {

	private WebDriver driver;

	private By usernameField = By.name("q");

	// Constructor
	public FirstPage(WebDriver driver) {
		this.driver = driver;
	}

	public void enterUsername(String username) {
		WebElement usernameInput = driver.findElement(usernameField);
		ExtentReportManager.logInfo("Clicked on search box");
		usernameInput.clear();
		usernameInput.sendKeys(username);
		ExtentReportManager.logInfo(username + " is added as an input in search box");
	}

}
