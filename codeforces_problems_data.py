import requests
from datetime import datetime

class Problem:
    def __init__(self):
        self.handle = "Md_Almizan"
        self.all_problems = []
        self.get_problems(self.handle)

    def get_problems(self, handle):
        url = f"https://codeforces.com/api/user.status?handle={handle}"
        response = requests.get(url)
        response.raise_for_status()
        if response.status_code == 200:
            submissions = response.json()["result"]
            for submission in submissions:
                problem = submission["problem"]
                self.all_problems.append((
                    submission["id"],
                    datetime.utcfromtimestamp(submission["creationTimeSeconds"] + 6 * 3600).strftime('%Y-%m-%d %H:%M:%S'),
                    problem["contestId"],
                    problem["index"],
                    problem["name"],
                    problem.get("rating", "Unrated"),
                    problem.get("tags", []),
                    submission["author"]["participantType"],
                    submission["programmingLanguage"],
                    submission["verdict"],
                    submission["timeConsumedMillis"],
                    float(submission["memoryConsumedBytes"])/1024   ## memoryConsumedKiloBytes
                ))

            return self.all_problems
        else:
            print(f"Failed to fetch data: {response.status_code}")
            return []