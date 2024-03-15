# coding: utf8

from flask import Flask, render_template, request
from bs4 import BeautifulSoup
import requests


headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36'}
url = "https://www.petrolofisi.com.tr/akaryakit-fiyatlari"

text = ""
data = [1 ,2 ,3, 4]
app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def indexHtml():
    if request.method == "GET":
        return render_template('index.html', data = data, text="")
    if request.method == "POST":
        if request.form["ilseciniz"] == "1":
            r = requests.get(url)
            if str(r.status_code) != "200":
                text = "Bilgi alınamadı. Daha sonra tekrar deneyin."
                return render_template('index.html', data = data, text=text)
            else:
                iller = request.form.get("iller")
                ilkodu = str(iller)
                print(iller)
                if ilkodu == "":
                    text = "Tekrar deneyin."
                    return render_template('index.html', data = data, text=text)
                else:
                    soup = BeautifulSoup(r.text, "html.parser")
                    fuel = soup.find('tr', {'data-disctrict-id': ilkodu})
                    iladi = fuel["data-disctrict-name"]
                    fuelprice = fuel.find_all('span', {'class': 'with-tax'})
                    data[0] = fuelprice[0].text
                    data[1] = fuelprice[1].text
                    data[2] = fuelprice[2].text
                    data[3] = fuelprice[3].text
                    return render_template('index.html', data = data, text=iladi)
                
            
if __name__ == "__main__":
    app.run(debug=True)