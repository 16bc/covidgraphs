import time
from flask import Flask
from flask import render_template
from flask import Markup
from fetcher import CovidData

app = Flask(__name__)

@app.route("/")
def show_list():
    links = ''
    try:
        covid = CovidData()
        frus = covid.first_rus()
        for i, item in enumerate(covid.data):
            regname = item['name']
            if i == frus:
                links += '<hr><span class="font-weight-bold">РОССИЯ</span><hr>'
            links += '<a href="' + str(i) + '">' + regname + '</a><br>'
        print("iter")
        return render_template('list.html', links=Markup(links))
    except:
        return "Ошибка"


@app.route("/<reg_num>")
def region_chart(reg_num):
    try:
        covid = CovidData()
        region_data = covid.data[int(reg_num)]
        legend = 'Выявлено заражённых'
        times = []
        values = []
        for t in region_data['histogram']:
            strdate = time.gmtime(t['ts'])
            strdate = time.strftime('%d.%m.%Y', strdate)
            times.append(strdate)
            values.append(t['value'])
        return render_template('index.html', region=region_data['name'], values=values, labels=times, legend=legend)
    except:
        return show_list()


if __name__ == "__main__":
    app.run()
