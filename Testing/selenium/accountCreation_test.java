package esc_project;

import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.edge.EdgeDriver;
import org.openqa.selenium.support.ui.Select;

public class accountCreation_test {
	static String adminEmail = "admin@gmail.com";
	static String adminPassword = "password";
	
	public static void main(String[] args) throws InterruptedException {		
		System.setProperty("webdriver.edge.driver", "D:\\Storage\\School\\Driver\\edgedriver_win64\\msedgedriver.exe");
		WebDriver driver = new EdgeDriver();
		driver.get("https://cl2g2-ezcheck.herokuapp.com");
		driver.manage().window().maximize();
		login_test_cases.login(adminEmail, adminPassword, driver);
		Thread.sleep(2000);
		createAcc(driver);
		Thread.sleep(2000);
		editAccount(driver);
		Thread.sleep(2000);
		createAcc(driver);
		Thread.sleep(2000);
		deleteAccount(driver);
		Thread.sleep(2000);
		logout(driver);
	}
	
	public static void createAcc(WebDriver driver) throws InterruptedException {
		driver.findElement(By.name("createAccount")).click();
		Thread.sleep(2500);
		WebElement email = driver.findElement(By.name("email"));
		email.sendKeys("euyansang@gmail.com");
		WebElement username = driver.findElement(By.name("username"));
		username.sendKeys("Eu Yan Sang");
		WebElement password = driver.findElement(By.name("password"));
		password.sendKeys("password");
		WebElement tenancy = driver.findElement(By.name("tenancy"));
		tenancy.sendKeys("50");
		WebElement location = driver.findElement(By.name("location"));
		location.sendKeys("#01-54");
		Select accountType = new Select(driver.findElement(By.name("accountType")));
		accountType.selectByVisibleText("Tenant");
		Select instituition = new Select(driver.findElement(By.name("instituition")));
		instituition.selectByVisibleText("NCCS");
		Thread.sleep(2500);
		WebElement register = driver.findElement(By.id("registerBtn"));
		register.click();
		Thread.sleep(2000);
		WebElement back = driver.findElement(By.id("back"));
		back.click();
	}
	
	public static void editAccount(WebDriver driver) throws InterruptedException {
		driver.findElement(By.name("editAccount")).click();
		Thread.sleep(2500);
		List<WebElement> table = driver.findElements(By.id("chooseUser"));
		table.get(table.size()-1).click();
		Thread.sleep(2000);
		WebElement instituition = driver.findElement(By.name("instituition"));
		instituition.sendKeys("KKH");
		Thread.sleep(2000);
		WebElement change = driver.findElement(By.tagName("Button"));
		change.click();
		Thread.sleep(2000);
		WebElement back = driver.findElement(By.id("back"));
		back.click();
	}
	
	public static void deleteAccount(WebDriver driver) throws InterruptedException {
		driver.findElement(By.name("deleteAccount")).click();
		Thread.sleep(2000);
		List<WebElement> table = driver.findElements(By.id("chooseUser"));
		Thread.sleep(2000);
		table.get(table.size()-1).click();
		Thread.sleep(3000);
		WebElement back = driver.findElement(By.id("back"));
		back.click();
	}
	
	public static void logout(WebDriver driver) {
		driver.findElement(By.id("logout")).click();
	}
}
