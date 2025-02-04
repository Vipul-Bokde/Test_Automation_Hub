package pages;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import libraries.Locators;
import setup.BaseSetup;

public class FirstPage {
	private Locators locators;
	private static final Logger logger = LogManager.getLogger(FirstPage.class);
	private By usernameField = By.name("q");
	private By listOfSweet = By.xpath("(//a[@title = 'Wedding Special'])[3]");

	// Constructor
	public FirstPage(WebDriver driver) {
		this.locators = new Locators(driver);
	}

	public void enterUsername(String username) {
		locators.sendKeys(usernameField, username);
		String locu =locators.getText(listOfSweet);
		logger.info(locu);
	}

}
