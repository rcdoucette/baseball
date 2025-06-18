from flask import Flask, Response
import requests
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route("/xfip")
def xfip():
    today = datetime.today()
    start = today - timedelta(days=10)
    start_str = start.strftime("%Y-%m-%d")
    end_str = today.strftime("%Y-%m-%d")

    url = f"https://www.fangraphs.com/leaders-legacy.aspx?pos=all&stats=pit&lg=all&qual=0&type=8&season=2025&season1=2025&ind=0&team=0,ts&rost=0&age=0&filter=&players=0&startdate={start_str}&enddate={end_str}&export=1"
    headers = { 'User-Agent': 'Mozilla/5.0' }

    r = requests.get(url, headers=headers)
    
    print(f"Status: {r.status_code}")
    print(f"First 500 chars: {r.text[:500]}")

    if r.ok and r.text.startswith("Team"):
        return Response(r.text, mimetype="text/csv")
    else:
        return Response("Error fetching FanGraphs data", status=500)


@app.route("/")
def index():
    return "FanGraphs proxy running."

if __name__ == "__main__":
    app.run()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
