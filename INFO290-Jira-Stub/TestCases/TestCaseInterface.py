from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import datetime

# Consider practices: Showing screenshot on failure, logging, and handling exceptions.
"""For each test, consider saving into an array:
    results.append({
        'input': test_case['input'],
        'expected': test_case['expected'],
        'actual': actual_text,
        'success': is_success
    })
"""

def wait_and_find(driver, by, value, timeout=10):
    """Wait for an element to be present and then find it"""
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return driver.find_element(by, value)
    except Exception as e:
        print(f"Element not found with locator {by}: {value}")
        print(f"Current page source: {driver.page_source}")
        raise e


class TestCaseInterface:
    def __init__(self, driver):
        self.driver = driver
        self.test_data = {}  # Store test data for failure reporting
        self.screenshots_dir = os.getenv('SCREENSHOTS_DIR', 'screenshots')
        self.enable_screenshots = os.getenv('ENABLE_SCREENSHOTS', 'true').lower() == 'true'
        
        # Create screenshots directory if it doesn't exist
        if self.enable_screenshots and not os.path.exists(self.screenshots_dir):
            os.makedirs(self.screenshots_dir)

    def run(self): # If fails, it should raise and print the test data in that test iteration.
        raise NotImplementedError("Subclasses should implement run method")
    
    def setup(self):
        raise NotImplementedError("Subclasses should implement setup method")

    def teardown(self):
        raise NotImplementedError("Subclasses should implement teardown method")
    
    def capture_test_data(self, key, value):
        """Capture test data for failure reporting"""
        self.test_data[key] = value
    
    def take_screenshot(self, description=""):
        """Take a screenshot and return the file path"""
        if not self.enable_screenshots:
            return None
            
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            test_name = self.__class__.__name__
            filename = f"{test_name}_{description}_{timestamp}.png" if description else f"{test_name}_{timestamp}.png"
            filepath = os.path.join(self.screenshots_dir, filename)
            
            self.driver.save_screenshot(filepath)
            print(f"📸 Screenshot saved: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Failed to take screenshot: {str(e)}")
            return None
    
    def get_test_data(self):
        """Get captured test data"""
        return self.test_data.copy()
    
    def clear_test_data(self):
        """Clear captured test data"""
        self.test_data.clear()
    
    def print_results(self, results):
        for i, result in enumerate(results):
            print(f"Test {result['id']}:")
            print(f"  Input: {result['input']}")
            print(f"  Expected: {result['expected']}")
            print(f"  Actual: {result['actual']}")
            print(f"  Success: {result['success']}")
        
        total_passed = sum(1 for result in results if result['success'])
        print(f"Total passed: {total_passed}")
        

        print(
            "OK!" if total_passed == len(results) else
            f"Failed [id]: {[ r["id"] for r in results if not r["success"]]}"
        )

    def get_name(self):
        raise NotImplementedError("Subclasses should implement get_name method")
    
    def get_description(self):
        raise NotImplementedError("Subclasses should implement get_description method")

    def wait_and_find(self, by, value, timeout=5):
        return wait_and_find(self.driver, by, value, timeout)