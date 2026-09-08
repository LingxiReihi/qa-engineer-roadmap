import requests

resp = requests.get('https://apis.tianapi.com/guonei/index?key=apikey&num=10')
if resp.status_code == 200:
    data_model = resp.json()
    for news in data_model['result']['newslist']:
        print(news['title'])
        print(news['url'])
        print('-' * 60)
