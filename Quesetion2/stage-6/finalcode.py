import heapq
from datetime import datetime, timedelta
import requests

W = {
    "placement": 5,
    "result": 4,
    "event": 2
}

TOP_K = 10
heap = []


class N:
    def __init__(self, nid, cat, msg, ts, read=False):
        self.nid = nid
        self.cat = cat
        self.msg = msg
        self.ts = ts
        self.read = read

    def score(self):
        wt = W.get(self.cat.lower(), 1)
        age = (datetime.now() - self.ts).total_seconds() / 60
        rec = max(0, 1000 - age)
        return wt * 1000 + rec

    def __repr__(self):
        return f"[{self.cat.upper()}] {self.msg} | {self.ts.strftime('%Y-%m-%d %H:%M:%S')}"


def fetch():
    url = "https://mocki.io/v1/6f9c6f4d-f9cf-4f9f-bb9d-123456789abc"

    try:
        r = requests.get(url)
        data = r.json()

        return [
            N(
                x["id"],
                x["category"],
                x["message"],
                datetime.fromisoformat(x["created_at"]),
                x.get("is_read", False)
            )
            for x in data
        ]

    except Exception as e:
        print("Fetch Error:", e)
        return []


def push(n):
    if n.read:
        return

    s = n.score()
    item = (s, n)

    if len(heap) < TOP_K:
        heapq.heappush(heap, item)

    elif s > heap[0][0]:
        heapq.heapreplace(heap, item)


def top():
    return sorted(heap, key=lambda x: x[0], reverse=True)


def simulate():
    arr = [
        N(101, "placement", "Google interview shortlist released", datetime.now() - timedelta(minutes=2)),
        N(102, "event", "Hackathon starts tomorrow", datetime.now() - timedelta(minutes=10)),
        N(103, "result", "Mid Semester Results Published", datetime.now() - timedelta(minutes=5)),
        N(104, "placement", "Microsoft internship applications open", datetime.now() - timedelta(minutes=1)),
        N(105, "event", "AI Workshop Registration Open", datetime.now() - timedelta(minutes=20)),
        N(106, "result", "Lab Internal Marks Uploaded", datetime.now() - timedelta(minutes=15)),
        N(107, "placement", "Amazon Coding Test Scheduled", datetime.now() - timedelta(minutes=3)),
        N(108, "event", "Tech Fest starts next week", datetime.now() - timedelta(minutes=30)),
        N(109, "placement", "TCS Recruitment Drive", datetime.now() - timedelta(minutes=7)),
        N(110, "result", "Assignment Scores Published", datetime.now() - timedelta(minutes=12)),
        N(111, "placement", "Adobe hiring announcement", datetime.now() - timedelta(minutes=4)),
        N(112, "event", "Gaming Tournament Tonight", datetime.now() - timedelta(minutes=25))
    ]

    for x in arr:
        push(x)


def show():
    print("\n========== PRIORITY INBOX ==========\n")

    for i, (s, n) in enumerate(top(), start=1):
        print(f"Rank #{i}")
        print(f"Score    : {round(s, 2)}")
        print(f"Category : {n.cat}")
        print(f"Message  : {n.msg}")
        print(f"Time     : {n.ts}")
        print("-" * 40)


if __name__ == "__main__":
    simulate()
    show()