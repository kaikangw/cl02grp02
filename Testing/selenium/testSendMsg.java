package esc_project;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.edge.EdgeDriver;

public class testSendMsg {
	static String tenantEmail = "kopitiam@gmail.com";
	static String tenantPassword = "password";
	public static void main(String[] args) throws InterruptedException {
		// TODO Auto-generated method stub
		System.setProperty("webdriver.edge.driver", "D:\\Storage\\School\\Driver\\edgedriver_win64\\msedgedriver.exe");
		WebDriver driver = new EdgeDriver();
		driver.get("https://cl2g2-ezcheck.herokuapp.com");

		driver.manage().window().maximize();
		login_test_cases.login(tenantEmail, tenantPassword, driver);
		Thread.sleep(2000);
		sendMsg(driver);

	}
	
	public static void sendMsg(WebDriver driver) throws InterruptedException{
		driver.findElement(By.linkText("Chats")).click();
		driver.findElement(By.id("tochat")).click();
		WebElement inputs = driver.findElement(By.className("msger-input"));
		
		inputs.sendKeys("Hello, I am a tenant");
		Thread.sleep(2000);
		driver.findElement(By.className("msger-send-btn")).click();;
	}

}
