package esc_project;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.Keys;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.chrome.ChromeDriver;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class test_navbar {
	
	static String correctEmail = "auditorandy@gmail.com";
	static String correctPassword = "password";
	static String[] navbarOptions = new String[] {"Directory","Audit","Data","Chats","Broadcast","Account"};
	
	@SuppressWarnings({ "unchecked", "unlikely-arg-type" })
	public static void main(String[] args) throws InterruptedException {		
		System.setProperty("webdriver.edge.driver", "D:\\Storage\\School\\Driver\\edgedriver_win64\\msedgedriver.exe");
		WebDriver driver = new EdgeDriver();
		//driver.get("http://localhost:5000");
		driver.get("https://cl2g2-ezcheck.herokuapp.com/");
		login_test_cases.login(correctEmail, correctPassword, driver);
		test_nav(driver);
		Thread.sleep(1000);
		login_test_cases.login(correctEmail, correctPassword, driver);
		System.out.print("test data\n");
		test_data(driver);
		System.out.print("finish data\n");
		Thread.sleep(1000);
		System.out.print("test audit\n");
		/*test_view_audit(driver);
		System.out.print("finish audit\n");
		Thread.sleep(1000);*/
		/*System.out.print("test directory\n");
		test_directory(driver);
		System.out.print("finish directory\n");*/
		
	}
	
	public static void test_nav(WebDriver driver) throws InterruptedException{
		driver.findElement(By.linkText(navbarOptions[0])).click();
		Thread.sleep(1000);
		driver.findElement(By.linkText(navbarOptions[1])).click();
		driver.findElement(By.linkText("Create")).click();
		Thread.sleep(1000);
		driver.findElement(By.linkText(navbarOptions[1])).click();
		driver.findElement(By.linkText("View")).click();
		Thread.sleep(1000);
		driver.findElement(By.linkText(navbarOptions[2])).click();
		Thread.sleep(1000);
		driver.findElement(By.linkText(navbarOptions[3])).click();
		driver.findElement(By.linkText("Log Out")).click();
	}
	
	public static void test_directory(WebDriver driver) throws InterruptedException {
		driver.findElement(By.linkText("Directory")).click();
		java.util.List<WebElement> directory = driver.findElements(By.tagName("a"));
		
		for(int i=0; i<directory.size();i++) {
			directory.get(i).click();
			Thread.sleep(1000);
			directory.get(i).click();
		}
	}
	
	public static void test_data(WebDriver driver) throws InterruptedException {
		driver.findElement(By.linkText("Data")).click();
		java.util.List<WebElement> data_buttons = driver.findElements(By.className("data_choice"));
		for(int i = 0; i<data_buttons.size(); i++) {
			WebElement cur_button = data_buttons.get(i);
			cur_button.click();
			Thread.sleep(1000);
		}
	}
	
	public static void test_view_audit(WebDriver driver) throws InterruptedException{
		driver.findElement(By.linkText("Audit")).click();
		driver.findElement(By.linkText("View")).click();
		System.out.print("Hello");
		java.util.List<WebElement> view_buttons = driver.findElements(By.tagName("i"));
		for(int i=0; i<view_buttons.size(); i++) {
			WebElement cur_button = view_buttons.get(i);
			cur_button.click();
			Thread.sleep(4000);
			driver.navigate().back();
			Thread.sleep(1000);
			
		}
	}
	
}
