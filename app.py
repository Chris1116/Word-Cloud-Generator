from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
from wordcloud import WordCloud, STOPWORDS
import numpy as np
from PIL import Image
import io
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/result', methods=['POST'])
def result():
    url = request.form['url']
    shape = request.form['shape']
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    stopwords = set(STOPWORDS)

    mask_image_path = None
    if shape in ['news', 'twitter', 'github', 'message']:
        mask_image_path = f'static/{shape}.png'

    if mask_image_path:
        mask_image = Image.open(mask_image_path)
        resized_mask_image = mask_image.resize((1200, 800), Image.ANTIALIAS)
        mask = np.array(resized_mask_image)
    else:
        mask = None

    wordcloud = WordCloud(stopwords=stopwords, background_color='white', width=1200, height=800, mask=mask).generate(text)

    if shape in ['news', 'twitter', 'github', 'message']:
        output_filename = f'static/{shape.capitalize()}Cloud.png'
        wordcloud.to_file(output_filename)

    return render_template('result.html', shape=shape, os=os)

if __name__ == '__main__':
    app.run(debug=True)