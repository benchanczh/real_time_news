import requests
import yaml
import hashlib

from json import loads, dumps

with open('../config/config.yml', 'r') as config_file:
    config = yaml.load(config_file)

NEWS_API_ENDPOINT = 'https://newsapi.org/v2/'
NEWS_API_KEY = config['api_key']
ARTICLES_API = 'top-headlines'
BBC_NEWS = 'bbc-news'
BBC_SPORT = 'bbc-sport'
CNN = 'cnn'

DEFAULT_SOURCES = [CNN, BBC_NEWS, BBC_SPORT]
SORT_BY_TOP = 'top'

def build_url(end_point=NEWS_API_ENDPOINT, api_name=ARTICLES_API):
    return end_point + api_name

def get_news_from_source(sources=DEFAULT_SOURCES, sort_by=SORT_BY_TOP):
    articles = []

    for source in sources:
        payload = {
            'sources': source,
            # 'country': 'us',
            'apiKey': NEWS_API_KEY,
            'sort_by': sort_by
        }

        response = requests.get(build_url(), params=payload)
        result_json = loads(response.content)

        if (result_json is not None and result_json['status'] == 'ok'):
            articles.extend(result_json['articles'])

    with open('../output/news_list.txt', 'w') as outfile:
        for item in articles:
            outfile.write('%s\n' % item)

    return articles

# def digest_news():
#     news_list = get_news_from_source()

#     for news in news_list:
#         news_digest = hashlib.md5(news['title'].encode('utf-8')).digest()
#         with open('news_digest.txt', 'a') as outfile:
#             for item in news_digest:
#                 outfile.write('%s\n' % item)


if __name__ == "__main__":
    a = get_news_from_source()
    print(dumps(a))