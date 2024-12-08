import requests
import os

def download_input(day, session_cookie):
    url = f"https://adventofcode.com/2024/day/{day}/input"
    cookies = {"session": session_cookie}
    response = requests.get(url, cookies=cookies)
    if response.status_code == 200:
        day_folder = f"day{day:02d}"
        os.makedirs(day_folder, exist_ok=True)  # Create the day's folder if it doesn't exist
        with open(f"{day_folder}/input.txt", "w") as file:
            file.write(response.text.strip())
        print(f"Day {day} input downloaded successfully!")
    else:
        print(f"Failed to download input for Day {day}. HTTP Status: {response.status_code}")

if __name__ == "__main__":
    SESSION_COOKIE = "53616c7465645f5f7f0369fa28945579241364f0cb8fe030a0930f38cc83b7f2c7504c66681cfacba08c61eece5d0a65f7cf586a8e333d0b43201f2d609f3c5b"
    CURRENT_DAY = 8
    download_input(CURRENT_DAY, SESSION_COOKIE)
