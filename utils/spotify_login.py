from utils.playwright_startup import PlaywrightDriver



driver = PlaywrightDriver(headless=False)
driver.page.goto("https://accounts.spotify.com")

input("Log in manually, then press Enter...")
driver.close()

# Recommended for - better song matching