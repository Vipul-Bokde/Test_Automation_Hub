package pages;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import libraries.*;

public class FirstPage {
	private LocatorsUtils locators;
	private SynchronisationAndWaitsUtils syncwaits;
	private MouseActionsUtils mouseActions;
	private static final Logger logger = LogManager.getLogger(FirstPage.class);
	private By usernameField = By.name("q");
	private By listOfSweet = By.xpath("(//a[@title = 'Wedding Special'])[3]");
	private By searchbutton = By.xpath("//button[@aria-label='search']");

	// Constructor
	public FirstPage(WebDriver driver) {
		this.locators = new LocatorsUtils(driver);
		this.mouseActions = new MouseActionsUtils(driver);
		this.syncwaits = new SynchronisationAndWaitsUtils(driver);
	}

	public void validateSearchBox(String username) {
		locators.sendKeys(usernameField, username);
		String locu =locators.getText(listOfSweet);
		logger.info(locu);
	}
	
	public void clickOnSearchButton() {
		syncwaits.waitForPresenceOfElement(searchbutton, 1);
        mouseActions.clickOnElement(searchbutton);
        logger.info("Clicked successfully");
    }
}
