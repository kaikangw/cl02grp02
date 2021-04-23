package esc_project;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class login_test_cases {
	
	//black box test cases
	static String b1email = "someone.with.id@email.com ";
	static String b1password = "password";
	
	static String b2email = "fake_email";
	static String b2password = "fake-password";
	
	static String b3email = "someone.with.id@email.com";
	static String b3password = "fake-password";
	
	static String b4email = "hello";
	static String b4password = "password";
	
	static String b5email = "";
	static String b5password = "";
	
	static String correctEmail = "auditorandy@gmail.com";
	static String correctPassword = "password";
	
	public static void main(String[] args) throws InterruptedException {
		
		System.setProperty("webdriver.edge.driver", "D:\\Storage\\School\\Driver\\edgedriver_win64\\msedgedriver.exe");
		WebDriver driver = new EdgeDriver();
		driver.get("https://cl2g2-ezcheck.herokuapp.com");
		driver.manage().window().maximize();
		login(b1email,b1password, driver);
		driver.switchTo().alert().accept();
		Thread.sleep(1000);
		login(b2email,b2password, driver);
		driver.switchTo().alert().accept();
		Thread.sleep(1000);
		login(b3email,b3password, driver);
		driver.switchTo().alert().accept();
		Thread.sleep(1000);
		login(b4email,b4password, driver);
		driver.switchTo().alert().accept();
		Thread.sleep(1000);
		login(b5email,b5password, driver);
		driver.switchTo().alert().accept();
		Thread.sleep(1000);
		login(correctEmail,correctPassword, driver);
		
	}
	
	public static void login(String myemail, String mypassword, WebDriver driver) {
		WebElement email = driver.findElement(By.name("username"));
		email.sendKeys(myemail);
		WebElement password = driver.findElement(By.name("password"));
		password.sendKeys(mypassword);
	
		WebElement nextButton = driver.findElement(By.className("logbtn"));
		nextButton.click();
	}
	
	public static void logout(WebDriver driver) {
		WebElement logout = driver.findElement(By.id("logout"));
		logout.click();
	}
	
}
