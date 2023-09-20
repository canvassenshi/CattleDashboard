import requests
from flask import Flask, render_template, request, url_for, redirect
import statistics as pd
import math


app = Flask(__name__)
app.config["SECRET_KEY"] = "dshbjsdbgjksdg"

r = requests.get('https://api.thingspeak.com/channels/2102600/feeds.json?')
data = r.json()


cleanData = {}

for feed in data['feeds']:
    if feed['field1'] not in cleanData.keys():
        cleanData[feed['field1']] = [feed['field2'], feed['field3'], feed['field4']]


milkL = [int(milk[0]) for milk in cleanData.values()]
temps = [int(temp[1]) for temp in cleanData.values()]
steps = [int(steps[2]) for steps in cleanData.values()]

avg_milk = pd.mean(milkL)
avg_temps = pd.mean(temps)
avg_steps = math.ceil(pd.mean(steps))


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        val = cowId = request.form.get("cowId")
        cowId = cleanData[f"COW_{cowId}"]
        milk, t, steps = cowId[0], cowId[1], cowId[2]
    return render_template("app.html", cowId = val, milk=milk, steps=steps, temp=t, avg_milk = avg_milk, avg_temps = avg_temps, avg_steps = avg_steps)



if __name__ == "__main__":
    app.run(debug=True)





