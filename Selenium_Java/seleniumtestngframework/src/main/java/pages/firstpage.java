package pages;
import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

public class firstpage {

    private WebDriver driver;

    
    private By usernameField = By.name("q");

    // Constructor
    public firstpage(WebDriver driver) {
        this.driver = driver;
    }
    
    public void enterUsername(String username) {
        WebElement usernameInput = driver.findElement(usernameField);
        usernameInput.clear();
        usernameInput.sendKeys(username);
    }

}
