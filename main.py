import requests
import asyncio
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")

last_staff_total = 0
last_watchdog_total = 0

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
                    print(f"Staff ban #{staff_total} ({current_time}). This was a staff ban. Be careful!")

                if last_watchdog_total != 0 and watchdog_total > last_watchdog_total:
                    print(f"Watchdog ban #{watchdog_total} ({current_time}). Don't worry, this was an anticheat ban.")

                last_staff_total = staff_total
                last_watchdog_total = watchdog_total

        except Exception as e:
            print(f'Error occurred while checking punishment stats: {e}')

        await asyncio.sleep(1)  # Check every second

banner = """

  _    _             _          _   ____                _   _       _   _  __ _            __      __  __   ___  
 | |  | |           (_)        | | |  _ \              | \ | |     | | (_)/ _(_)           \ \    / / /_ | |__ \ 
 | |__| |_   _ _ __  ___  _____| | | |_) | __ _ _ __   |  \| | ___ | |_ _| |_ _  ___ _ __   \ \  / /   | |    ) |
 |  __  | | | | '_ \| \ \/ / _ \ | |  _ < / _` | '_ \  | . ` |/ _ \| __| |  _| |/ _ \ '__|   \ \/ /    | |   / / 
 | |  | | |_| | |_) | |>  <  __/ | | |_) | (_| | | | | | |\  | (_) | |_| | | | |  __/ |       \  /     | |_ / /_ 
 |_|  |_|\__, | .__/|_/_/\_\___|_| |____/ \__,_|_| |_| |_| \_|\___/ \__|_|_| |_|\___|_|        \/      |_(_)____|
          __/ | |                                                                                                
         |___/|_|                                                                                                


by joshiy13
"""

print(banner)

asyncio.run(check_punishment_stats())