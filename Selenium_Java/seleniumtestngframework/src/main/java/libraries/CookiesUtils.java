package libraries;

import org.openqa.selenium.Cookie;
import org.openqa.selenium.WebDriver;
// ... other imports

public class CookiesUtils {
	private WebDriver driver;

	public CookiesUtils(WebDriver driver) {
		this.driver = driver;
	}

	public void addCookie(Cookie cookie) {
		driver.manage().addCookie(cookie);
	}

	public Cookie getCookie(String name) {
		return driver.manage().getCookieNamed(name);
	}

	public void deleteCookie(String name) {
		driver.manage().deleteCookieNamed(name);
	}

	public void deleteAllCookies() {
		driver.manage().deleteAllCookies();
	}
}