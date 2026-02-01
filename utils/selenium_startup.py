from utils.config import CHROME_BINARY, DRIVER_PATH
from selenium import webdriver
from selenium.webdriver.chrome.service import Service


# Set Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = CHROME_BINARY
# REQUIRED (new headless, not the legacy garbage)
chrome_options.add_argument("--headless=new")
# Performance
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
# Stability for SPAs
chrome_options.add_argument("--window-size=1920,1080")
chrome_options.add_argument("--disable-background-timer-throttling")
chrome_options.add_argument("--disable-backgrounding-occluded-windows")
chrome_options.add_argument("--disable-renderer-backgrounding")
# Anti-flake
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
# Optional but recommended (Spotify sometimes behaves differently)
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

chrome_service = Service(executable_path=DRIVER_PATH)
driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
print("----Chrome driver was started----")

def get_driver():
    return driver