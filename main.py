import requests
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os
import re
import webbrowser

load_dotenv()

API_KEY = os.getenv("API_KEY")

last_staff_total = 0
last_watchdog_total = 0
current_version = "1.3.2"
new_version_displayed = False

def check_new_release():
    try:
        releases_response = requests.get('https://api.github.com/repos/Joshiy13/Ban-Notifier/releases')
        releases_data = releases_response.json()

        if releases_data and len(releases_data) > 0:
            latest_release = releases_data[0]
            latest_release_tag = latest_release['tag_name']
            latest_release_url = latest_release['html_url']

            if compare_versions(latest_release_tag, current_version) > 0:
                return latest_release_url

    except Exception as e:
        print(f'Error occurred while checking for new release: {e}')

    return None

def compare_versions(version1, version2):
    pattern = r'(\d+).(\d+).(\d+)'
    v1_match = re.match(pattern, version1)
    v2_match = re.match(pattern, version2)

    if v1_match and v2_match:
        v1_major, v1_minor, v1_patch = map(int, v1_match.groups())
        v2_major, v2_minor, v2_patch = map(int, v2_match.groups())

        if v1_major != v2_major:
            return v1_major - v2_major
        elif v1_minor != v2_minor:
            return v1_minor - v2_minor
        else:
            return v1_patch - v2_patch

    return 0

# Check for a new release and display the update banner if needed
new_release_url = check_new_release()
if new_release_url:
    updateBanner = """
 _   _                __      __           _                                _ _       _     _      _ 
| \ | |               \ \    / /          (_)                              (_) |     | |   | |    | |
|  \| | _____      __  \ \  / /__ _ __ ___ _  ___  _ __     __ ___   ____ _ _| | __ _| |__ | | ___| |
| . ` |/ _ \ \ /\ / /   \ \/ / _ \ '__/ __| |/ _ \| '_ \   / _` \ \ / / _` | | |/ _` | '_ \| |/ _ \ |
| |\  |  __/\ V  V /     \  /  __/ |  \__ \ | (_) | | | | | (_| |\ V / (_| | | | (_| | |_) | |  __/_|
|_| \_|\___| \_/\_/       \/ \___|_|  |___/_|\___/|_| |_|  \__,_| \_/ \__,_|_|_|\__,_|_.__/|_|\___(_)
    """
    print(updateBanner)
    webbrowser.open_new_tab(new_release_url)
    input("Press enter to exit...")
else:
    banner = """


 _    _             _          _   ____                _   _       _   _  __ _              ____   ____   _____  
| |  | |           (_)        | | |  _ \              | \ | |     | | (_)/ _(_)            / /_ | |___ \ |__ \ \ 
| |__| |_   _ _ __  ___  _____| | | |_) | __ _ _ __   |  \| | ___ | |_ _| |_ _  ___ _ __  | | | |   __) |   ) | |
|  __  | | | | '_ \| \ \/ / _ \ | |  _ < / _` | '_ \  | . ` |/ _ \| __| |  _| |/ _ \ '__| | | | |  |__ <   / /| |
| |  | | |_| | |_) | |>  <  __/ | | |_) | (_| | | | | | |\  | (_) | |_| | | | |  __/ |    | | | |_ ___) | / /_| |
|_|  |_|\__, | .__/|_/_/\_\___|_| |____/ \__,_|_| |_| |_| \_|\___/ \__|_|_| |_|\___|_|    | | |_(_)____(_)____| |
         __/ | |                                                                           \_\               /_/ 
        |___/|_|                                                                                                 
                                                                                           

by joshiy13
    """
    print(banner)

async def check_punishment_stats():
    global last_staff_total, last_watchdog_total

    while True:
        try:
            response = requests.get('https://api.hypixel.net/punishmentstats', params={'key': API_KEY})
            data = response.json()

            if data['success']:
                staff_total = data['staff_total']
                watchdog_total = data['watchdog_total']

                current_time = datetime.now().strftime('%H:%M:%S')

                if last_staff_total != 0 and staff_total > last_staff_total:
                    print(f"Staff ban #{staff_total} ({current_time}).")

                if last_watchdog_total != 0 and watchdog_total > last_watchdog_total:
                    print(f"Watchdog ban #{watchdog_total} ({current_time}).")

                last_staff_total = staff_total
                last_watchdog_total = watchdog_total

            await asyncio.sleep(1)

        except Exception as e:
            print(f'Error occurred while checking punishment stats: {e}')

# Start the punishment stats checking loop
asyncio.run(check_punishment_stats())
