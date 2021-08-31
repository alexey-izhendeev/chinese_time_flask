from flask import Flask, render_template, request, url_for, redirect
from calculations import solartime, positioner, solar_to_chinese
import ephem

app = Flask(__name__)


@app.route('/', methods=('GET', 'POST'))
def start_page():
    if request.method == 'POST':
        latitude = request.form['lat']
        longitude = request.form['long']

        return redirect(url_for('result_page', latitude=latitude, longitude=longitude))
    return render_template('start_page.html')


@app.route('/result_page/<latitude>/<longitude>')
def result_page(latitude, longitude):
    pos = ephem.Observer()  # ephem object
    pos.lat = str(latitude)  # latitude
    pos.long = str(longitude)  # longitude
    solar = solartime(pos)  # solartime
    chin = solar_to_chinese(solartime(pos))  # chinese time
    tim = positioner(str(latitude), str(longitude))
    return render_template('result_page.html', solar=solar, chin=chin, tim=tim)


if (__name__ =="__main__"):
    app.run(debug=True)
