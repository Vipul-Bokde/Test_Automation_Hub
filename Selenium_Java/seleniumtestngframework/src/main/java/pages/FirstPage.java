package pages;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import libraries.Locators;

public class FirstPage {
	private Locators locators;

	private By usernameField = By.name("q");
	private By listOfSweet = By.xpath("(//a[@title = 'Wedding Special'])[3]");

	// Constructor
	public FirstPage(WebDriver driver) {
		this.locators = new Locators(driver);
	}

	public void enterUsername(String username) {
		locators.sendKeys(usernameField, username);
		String locu =locators.getText(listOfSweet);
		System.out.println(locu);
	}

}
