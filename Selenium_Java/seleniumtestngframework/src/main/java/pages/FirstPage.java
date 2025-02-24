package pages;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.testng.Assert;

import libraries.*;

public class FirstPage {
	private LocatorsUtils locators;
	private SynchronisationAndWaitsUtils syncwaits;
	private MouseActionsUtils mouseActions;
	private static final Logger logger = LogManager.getLogger(FirstPage.class);

	// LOCATORS LIST
	private By usernameField = By.name("q");
	private By listOfSweet = By.xpath("(//a[@title = 'Wedding Special'])[3]");
	private By searchbutton = By.xpath("//button[@aria-label='search']");
	private By rasgulla_item = By.xpath("(//a[contains(text(), 'Rasgulla')])[1]");
	private By check_rasgulla_price = By.xpath("//div/h6[text()='Price']/following-sibling::div/span");
	private By buy_rasgulla_button = By.xpath("//button[@id='product-buynow-button']");

	// Constructor
	public FirstPage(WebDriver driver) {
		this.locators = new LocatorsUtils(driver);
		this.mouseActions = new MouseActionsUtils(driver);
		this.syncwaits = new SynchronisationAndWaitsUtils(driver);
	}

	public void validateSearchBox(String username) {
		locators.sendKeys(usernameField, username);
		String locu = locators.getText(listOfSweet);
		logger.info(locu);
	}

	public void clickOnSearchButton() {
		syncwaits.waitForPresenceOfElement(searchbutton, 1);
		mouseActions.clickOnElement(searchbutton);
		logger.info("Clicked successfully");
	}

	public void exploresweetNameItem() {
		syncwaits.waitForPresenceOfElement(rasgulla_item, 1);
		mouseActions.clickOnElement(rasgulla_item);
		logger.info("Clicked" + rasgulla_item + "successfully");
		String rasgullaPrice = locators.getText(check_rasgulla_price);
		String priceStr = rasgullaPrice.replace("₹", "");
		double price = Double.parseDouble(priceStr);
		System.out.println(price);
		Assert.assertEquals(price, 125.00, "Rasgulla price is not 125. Actual price: " + rasgullaPrice);
		if (price == 125.00) {
			mouseActions.clickOnElement(buy_rasgulla_button);
			logger.info("Clicked 'Buy Now' button successfully.");
		} else {
			logger.warn("Rasgulla price is not 125. Buy Now button was not clicked.");
		}

	}

}
