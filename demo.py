from openwpm import CommandSequence, TaskManager
from os.path import abspath, dirname	
import time, datetime

# The list of sites that we wish to crawl
NUM_BROWSERS = 1
sites = [	
    "https://www.cnn.com",	
    # "https://www.nytimes.com",
    # "https://www.cnn.com",	
    "https://www.nytimes.com",	
    # "https://news.yahoo.com",	
]

# Loads the default manager params
# and NUM_BROWSERS copies of the default browser params
manager_params, browser_params = TaskManager.load_default_params(NUM_BROWSERS)

# Update browser configuration (use this for per-browser settings)
for i in range(NUM_BROWSERS):
    # Record HTTP Requests and Responses
    browser_params[i]["http_instrument"] = True
    # Record cookie changes
    browser_params[i]["cookie_instrument"] = True
    # Record Navigations
    browser_params[i]["navigation_instrument"] = True
    # Record JS Web API calls
    browser_params[i]["js_instrument"] = True
    # Record the callstack of all WebRequests made
    browser_params[i]["callstack_instrument"] = True
    # Record DNS resolution
    browser_params[i]["dns_instrument"] = True


# # Modify custom browser flags - refer https://github.com/mozilla/OpenWPM#browser-configuration-options
for i in range(NUM_BROWSERS):
#     # Enable "do not track" in browser
#     browser_params[i]["donottrack"] = True
    # Enable "ghostery" in browser
    browser_params[i]["ghostery"] = True
#     # Enable "disconnect" in browser
#     browser_params[i]["disconnect"] = True
#     # Enable "https-everywhere" in browser
#     browser_params[i]["https-everywhere"] = True
#     # Enable "ublock-origin" in browser
#     browser_params[i]["ublock-origin"] = True
#     # Enable "tracking-protection" in browser
#     # browser_params[i]["tracking-protection"] = True

# Launch only browser 0 headless
browser_params[0]["display_mode"] = "headless"

# fetch current date and time for folder name
dt=datetime.datetime.now()
time_str=time.strftime('%Y_%m_%d_%H_%M_%S')

# Update TaskManager configuration (use this for crawl-wide settings)
manager_params["data_directory"] = dirname(dirname(abspath(__file__)))+"/crawls_"+time_str+"/"
manager_params["log_directory"] = dirname(dirname(abspath(__file__)))+"/crawls_"+time_str+"/"
manager_params["memory_watchdog"] = True
manager_params["process_watchdog"] = True


# Instantiates the measurement platform
# Commands time out by default after 60 seconds
manager = TaskManager.TaskManager(manager_params, browser_params)

# Visits the sites
for site in sites:

    # Parallelize sites over all number of browsers set above.
    command_sequence = CommandSequence.CommandSequence(
        site,
        reset=True,
        callback=lambda success, val=site: print("CommandSequence {} done".format(val)),
    )

    # Start by visiting the page
    command_sequence.get(sleep=3, timeout=60)

    # Run commands across the three browsers (simple parallelization)
    manager.execute_command_sequence(command_sequence)

# Shuts down the browsers and waits for the data to finish logging
manager.close()
