import requests
import matplotlib.pyplot as plt
from datetime import datetime


class CodeforcesRating:
    def __init__(self, handle):
        self.handle = handle
        self.rating_history = []
        self.get_rating_history()

    def get_rating_history(self):
        url = f"https://codeforces.com/api/user.rating?handle={self.handle}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code == 200:
                contests = response.json()["result"]
                for contest in contests:
                    self.rating_history.append({
                        'contestId': contest['contestId'],
                        'contestName': contest['contestName'],
                        'rank': contest['rank'],
                        'oldRating': contest['oldRating'],
                        'newRating': contest['newRating'],
                        'timestamp': datetime.utcfromtimestamp(contest['ratingUpdateTimeSeconds'])
                    })
            else:
                print(f"Failed to fetch data: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data: {e}")


    def plot_rating_history(self):
        if not self.rating_history:
            print("No rating history available")
            return

        timestamps = [contest['timestamp'] for contest in self.rating_history]
        ratings = [contest['newRating'] for contest in self.rating_history]

        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, ratings, 'ro-', linewidth=1, markersize=4)

        plt.grid(True, linestyle='--', alpha=0.7)
        plt.title(f"Codeforces Rating History for {self.handle}")
        plt.xlabel("Date")
        plt.ylabel("Rating")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()