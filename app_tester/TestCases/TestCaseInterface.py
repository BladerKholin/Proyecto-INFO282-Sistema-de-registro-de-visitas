from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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

    def run(self): # If fails, it shouls raise and print the test data in that test iteration.
        raise NotImplementedError("Subclasses should implement run method")
    
    def setup(self):
        raise NotImplementedError("Subclasses should implement setup method")

    def teardown(self):
        raise NotImplementedError("Subclasses should implement teardown method")
    
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