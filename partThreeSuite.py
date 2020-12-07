from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver import Chrome
import os


from applitools.selenium import (
    logger,
    VisualGridRunner,
    Eyes,
    Target,
    BatchInfo,
    BrowserType,
    DeviceName,
    Region,
    IosDeviceInfo,
    IosDeviceName,
    ScreenOrientation,
)


url = "https://demo.applitools.com/tlcHackathonMasterV2.html"


def set_up(eyes):

    # You can get your api key from the Applitools dashboard
    eyes.configure.set_api_key("iT99w9RjQBj3M10943La99ithIhn0HA3GfzLK2MBYjpH1Nc110")

    # create a new batch info instance and set it to the configuration
    eyes.configure.set_batch(BatchInfo("Holiday Shopping"))

    # Add browsers with different viewports
    # Add mobile emulation devices in Portrait mode
    eyes.configure.add_browser(1200, 800, BrowserType.CHROME)
    eyes.configure.add_browser(1200, 800, BrowserType.FIREFOX)
    eyes.configure.add_browser(1200, 800, BrowserType.EDGE_LEGACY)
    eyes.configure.add_browser(1200, 800, BrowserType.SAFARI)
    eyes.configure.add_browser(IosDeviceInfo(IosDeviceName.iPhone_X, ScreenOrientation.PORTRAIT))


################
#    TEST 1    #
################

def test1(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        web_driver.get(url)

        # Call Open on eyes to initialize a test session
        viewport_size = {'width' :1200, 'height' :800}
        eyes.open(web_driver, "AppliFashion", "Test 1", viewport_size)

        # check the login page with fluent api, see more info here
        # https://applitools.com/docs/topics/sdk/the-eyes-sdk-check-fluent-api.html
        #eyes.check("step1", Target.window().fully().with_name("main page"))
        eyes.check("main page", Target.window().fully())
        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()
    except Exception as e:
        eyes.abort_async()
        print(e)

################
#    TEST 2    #
################

def test2(web_driver, eyes):
    try:
        # Navigate to the url we want to test
        web_driver.get(url)

        # Call Open on eyes to initialize a test session
        viewport_size = {'width' :1200, 'height' :800}
        eyes.open(web_driver, "AppliFashion", "Test 2", viewport_size)

        web_driver.find_element_by_id("SMALL____105").click()
        web_driver.find_element_by_id("filterBtn").click()
        product_grid = web_driver.find_element_by_id("product_grid")
        location = product_grid.location
        size = product_grid.size
        region_grid_shoes = Region(product_grid.rect["x"],product_grid.rect["y"],product_grid.rect["width"], product_grid.rect["height"])
        eyes.check_region(region_grid_shoes, "filter by color")

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()

    except Exception as e:
        eyes.abort_async()
        print(e)

################
#    TEST 3    #
################

def test3(web_driver, eyes):
    shoesTitleLocator= "//div[@id='product_grid']//div[@class='grid_item']//h3[contains(text(),'Appli Air x Night')]"
    try:
        # Navigate to the url we want to test
        web_driver.get(url)

        # Call Open on eyes to initialize a test session
        viewport_size = {'width' :1200, 'height' :800}
        eyes.open(web_driver, "AppliFashion", "Test 3", viewport_size)

        web_driver.find_element_by_xpath(shoesTitleLocator)
        web_driver.find_element_by_xpath(shoesTitleLocator+"/..").click()

        eyes.check("product details", Target.window().fully())

        # Call Close on eyes to let the server know it should display the results
        eyes.close_async()

    except Exception as e:
        eyes.abort_async()
        print(e)




################
#   TEARDOWN   #
################

def tear_down(web_driver, runner):
    # Close the browser
    web_driver.quit()

    # we pass false to this method to suppress the exception that is thrown if we
    # find visual differences
    all_test_results = runner.get_all_test_results(False)
    print(all_test_results)



################
#     MAIN     #
################
# Create a new chrome web driver
web_driver = Chrome(ChromeDriverManager().install())

# Create a runner with concurrency of 1
runner = VisualGridRunner(1)

# Create Eyes object with the runner, meaning it'll be a Visual Grid eyes.
eyes = Eyes(runner)

set_up(eyes)

try:
    # Note to see visual bugs, run the test using the above URL for the 1st run.
    # but then change the above URL to https://demo.applitools.com/index_v2.html
    # (for the 2nd run)
    test1(web_driver, eyes)
    test2(web_driver, eyes)
    test3(web_driver, eyes)

finally:
    tear_down(web_driver, runner)
