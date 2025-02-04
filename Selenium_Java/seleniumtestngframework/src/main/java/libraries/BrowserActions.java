package libraries;

import org.openqa.selenium.WebDriver;

public class BrowserActions {
	 private WebDriver driver;

	    // Constructor to initialize WebDriver
	    public BrowserActions(WebDriver driver) {
	        this.driver = driver;
	    }

	    // Refresh the current page
	    public void refresh() {
	        driver.navigate().refresh();
	    }

	    // Quit the browser
	    public void quitBrowser() {
	        driver.quit();
	    }

	    // Go back in browser history
	    public void goBack() {
	        driver.navigate().back();
	    }

	    // Go forward in browser history
	    public void goForward() {
	        driver.navigate().forward();
	    }
	    
	    // Maximize the browser window
	    public void maximizeWindow() {
	        driver.manage().window().maximize();
	    }

	    // Navigate to a given URL
	    public void openURL(String url) {
	        driver.get(url);
	    }
}
