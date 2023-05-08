from flask import *
from bs4 import BeautifulSoup
import requests
import cohere
from mtranslate import translate

app = Flask(__name__)

co = cohere.Client('UmLRVaXvGMiR9FbQxBGcy42Pp78e1GqD84uzEdTX')

@app.route("/")
def home():
    return render_template("index.html")


# def get_news():
#     category = request.form["category"]
#     url = f"https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey=040f00c6c5b94493882bf83e675f870d"
#     response = requests.get(url)
#     articles = response.json()["articles"]
#     return render_template("news.html", articles=articles)

@app.route("/get_news", methods=["POST"])
def get_news():
    category = request.form["category"]
    links = []
    for i in range(5):
        # Set the URL of the website to scrape
        url = f"https://punchng.com/topics/{category}/page/{i}"
        # Make a GET request to the website and get the HTML content
        response = requests.get(url)
        html_content = response.content
        # Use BeautifulSoup to parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find all the links to the news articles on the page
        news_links = []
        for link in soup.find_all("h1", class_="post-title"):
            links.append(link.find('a')['href'])
            # print(link.find('a')['href'])


    # for link in links:
    response = requests.get(links[0])
    html_content = response.content

    # Use BeautifulSoup to parse the HTML content
    soup = BeautifulSoup(html_content, "html.parser")

    # Find the full news content on the page and print it
    full_news = soup.find("article", class_="single-article")
    all_article = full_news.find('div', class_='post-content')
    articles = [p.text.strip() for p in all_article.find_all('p')]
    
    response = co.summarize(text=articles[0], model='summarize-xlarge', length='medium',extractiveness='medium')
    summary = response.summary
    
    yo_sentence = translate(summary, "yo")
    
    return render_template("news.html", articles=summary, yoruba=yo_sentence)


# if __name__ == "__main__":
#     app.run(debug=True)
