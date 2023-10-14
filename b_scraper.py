import re
import requests
from abc import abstractmethod, ABC
from lxml import html
import json

# BScraper as in Bibly scrapper


class BScraper(ABC):
    def __init__(self):
        pass

    @property
    def fields(self):
        raise NotImplementedError()

    @property
    def start_urls_names(self):
        raise NotImplementedError()

    def publish_to_api(self, url, articles):

        for index, article in enumerate(articles):
            request.post(url, data=article)
            print((index + 1))

    def _get_fields(self):
        article = {}
        for field in self.fields:
            article[field] = getattr(self, "get_" + field)()
        return article


class ChineseScraper(BScraper):
    fields = ["source_type"]
    start_urls_names = ["http://www.nhc.gov.cn/wjw/gfxwjj/list.shtml"]

    def get_menu(self):
        print("get menu called bro")

    @property
    def source(self):
        return "Health Minstry"

    def articles(self, response):
        tree = html.fromstring(response)
        _articles = tree.xpath("//div[@class='list']//li")
        data = []
        for li in _articles:
            _art = {}

            _art["title"] = li.xpath(".//a/text()")
            _art["link"] = li.xpath(".//a/@href")
            _art["release_date"] = li.xpath(".//span/text()")
            data.append(_art)

        try:
            with open("data.json", 'r') as file:
                existing_data = json.load(file)
        except FileNotFoundError:
            existing_data = []

        existing_data += data

        with open("data.json", "w") as file:
            json.dump(existing_data, file, ensure_ascii=False, indent=4)

    def content(self, response):
        tree = html.fromstring(response)
        _articles = tree.xpath("//div[@class='list']//div[@class='con']//p")
        print(_articles)
        data = []
        for li in _articles:
            data.append(li.text_content())
        with open("data.json", "a") as writer:
            writer.write(json.dumps(
                '\n'.join([s if s != "" else "\n" for s in data]), ensure_ascii=False))

    def process(self):
        for data in self.make_request():
            self.articles(data)

    def make_request(self):
        headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Cookie": "wzws_sessionid=oGUq5PaCOTBkYTRigDg5LjM5LjEwNy4xOTmBNWY3YmQz; sVoELocvxVW0S=5sAb8Ux7uUndnQ6c_7iKBn5tozkDDIupu7A3zeXSXjwEEmoGEej9eMrbLtL0qUpzgWplTmUELRGBo6axUk0_UiG; insert_cookie=96260894; yfx_c_g_u_id_10006654=_ck23101421591212331570031173025; arialoadData=true; ariawapChangeViewPort=false; yfx_f_l_v_t_10006654=f_t_1697309952206__r_t_1697309952206__v_t_1697319190707__r_c_0; sVoELocvxVW0T=5R17hhKV.cnLqqqDhWcVapaTK7fmyXu2.OMxqW.xcvZnMCtUYiICKxUp6PvF5hVP_PS64BU0UE6a72fS3SddSJh5ZuD6iLNTsg0W..UvNx0UHJ3.oMdWDFxOyoWyvEJBZGircRIgyWBpJQzFAq5rtbDXOkENn05wkE4kzLWKodlMuSBGQMiGLCufWuGcah0PYiEWBVEzS5yGXMj7B3q.5W_sID8ylR2XsLUoaj9ROY6jub4oE71veAptmDRUOoIQs4qOTSJRBZqFswB6GDhV7b1yfd5MBFVUKbUmNOEx5YRtG",
            "Accept-Encoding": "gzip, deflate, br",
            "Host": "www.nhc.gov.cn",
            "Referer": "http://www.nhc.gov.cn/wjw/gfxwjj/list.shtml"
        }
        session = requests

        data = []
        page = ""
        i = 0
        while i <= 4:
            i += 1
            if type(page) == int:
                page += 1
            response = session.get(
                f"http://www.nhc.gov.cn/wjw/gfxwjj/list_{page}.shtml",
                headers=headers)

            if page == "":
                page = 2
            if response.status_code == 404:
                print("============completed============")
            elif response.status_code == 200:
                print("================done==============")
                data.append(response.text)
            else:
                print(response.status_code)
        return data


ChineseScraper().process()
