import re
import requests
from abc import ABC
from lxml import html
import json
from urllib.parse import urlparse

# BScraper as in Bibly scrapper
class BScraper(ABC):
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.83 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Host": "www.nhc.gov.cn",
        }
        self.server_url = "http://127.0.0.1:8000/"

    def process(self):
        for url in self.start_urls_names:
            self.current_url = url
            self.get_articles()
            self.get_article_contents()


class NHCScraper(BScraper):

    def __init__(self, cookie):
        super().__init__()
        self.headers["Cookie"] = cookie
        
        # you should use a few urls inorder to test it out because we are not using a headless browser
        # the request will fail if you don't have a strong internet.
        self.start_urls_names = [
            "http://www.nhc.gov.cn/wjw/gfxwjj/list",
            "http://www.nhc.gov.cn/wjw/zcfg/list",
            "http://www.nhc.gov.cn/wjw/wnsj/list",
            "http://www.nhc.gov.cn/wjw/gztz/list",
            "http://www.nhc.gov.cn/wjw/zqyj/list",
            "http://www.nhc.gov.cn/wjw/zcjd/list",
            "http://www.nhc.gov.cn/gjhzs/pqt/new_list",
            "http://www.nhc.gov.cn/xcs/pqt/new_list",
            "http://www.nhc.gov.cn/rkjcyjtfzs/pqt/new_list",
            "http://www.nhc.gov.cn/zyjks/pqt/new_list",
            "http://www.nhc.gov.cn/fys/pqt/new_list",
            "http://www.nhc.gov.cn/lljks/pqt/new_list",
            "http://www.nhc.gov.cn/lljks/zcwj2/new_list",
            "http://www.nhc.gov.cn/sps/pqt/new_list",
            "http://www.nhc.gov.cn/yaozs/pqt/new_list",
            "http://www.nhc.gov.cn/qjjys/pqt/new_list",
            "http://www.nhc.gov.cn/ylyjs/new_index",
            "http://www.nhc.gov.cn/jws/pqt/new_list",
            "http://www.nhc.gov.cn/yzygj/pqt/new_list",
            "http://www.nhc.gov.cn/tigs/pqt/new_list",
            "http://www.nhc.gov.cn/fzs/pqt/new_list",
            "http://www.nhc.gov.cn/caiwusi/pqt/new_list",
            "http://www.nhc.gov.cn/guihuaxxs/zcwj2/zcwj",
            "http://www.nhc.gov.cn/renshi/pqt/new_list",
            "http://www.nhc.gov.cn/bgt/pqt/new_list",
            "http://www.nhc.gov.cn/wjw/jiany/list"
        ]
        self.current_url = self.start_urls_names[0]

    def process_articles(self, response, category_id):
        """
        Xpath will return list of articles selectors present on the start_url. 
        """
        tree = html.fromstring(response)
        _articles = tree.xpath("//div[@class='list']//ul//li")

        # Get domain of the current url like http://www.google.com
        parsed_url = urlparse(self.current_url)
        domain = f"{parsed_url.scheme}://{parsed_url.netloc}"

        # loop through the articles and extract the article title, published date and url
        for article in _articles:
            _article = {}
            resource_url = article.xpath(".//a/@href")[0]
            _article["title"] = article.xpath(".//a/text()")[0]
            _article["url"] = domain + \
                (resource_url) if resource_url.endswith(
                    ".shtml") else resource_url + 'l'
            _article["published_date"] = article.xpath(
                ".//span[last()]/text()")[0]
            _article["category"] = category_id

            # create article records for every article in the list [this is record does not contain the content]
            try:
                response = requests.post(
                    f"{self.server_url}api/articles/", data=_article)
            except:
                print("================= article record not created ==================")

    def get_article_contents(self):
        """
        This method goes to the detail page of articles and scrape the contents of the article

        - After the content is parsed it will update the article records in the database  
        """
        try:
            response = requests.get(
                f"{self.server_url}api/articles/?is_parsed=False")

            for article in response.json():
                try:
                    response = self.session.get(
                        article['url'], headers=self.headers)
                    if response.status_code == 200:
                        tree = html.fromstring(response.text)
                        _articles = tree.xpath(
                            "//div[@class='list']//div[@class='con']//p")
                        data = []
                        for li in _articles:
                            data.append(li.text_content())
                        article_id = article['id']
                        del article["id"]
                        try:
                            article["is_parsed"] = True
                            article["status"] = 2
                            article["content"] = '\n'.join(
                                [s if s != "" else "\n" for s in data])
                            requests.patch(
                                f"{self.server_url}api/articles/{article_id}/", data=article, headers=self.headers)
                            print(
                                "======= successfully scraped article content =======")
                        except Exception as ex:
                            try:
                                article["is_parsed"] = False
                                article["status"] = 1  # Failed Parsing
                                requests.patch(
                                    f"{self.server_url}api/articles/{article_id}/", data=article, headers=self.headers)
                                print(
                                    "======= success scraped article content =======")
                            except Exception as ex:
                                print("=========== content updated =====", ex)
                    else:
                        print("============= scraping content failed =======",
                              response.status_code)
                except Exception as ex:
                    print(
                        "==================== article content scraped ================", ex)

        except:
            print("====== there is something wrong the server ======")

    def process_pages(self):
        """
        Fetches every start_url with pagination and creates a category record on the database for every start_url

        Returns:
            (str, int): response text, category_id
        """

        page_responses = []
        page = 1
        category_id = None

        # For testing purposes you can update the condition to something like this while page < 2:
        while True:
                if page == 1:
                    response = self.session.get(
                        self.current_url+".shtml",
                        headers=self.headers,
                    )
                else:
                    if html.fromstring(response.text).xpath("//@div[id='page_div']"):
                        response = self.session.get(
                            self.current_url + f"_{page}.shtml",
                            headers=self.headers,
                        )

                # update session cookies
                self.session.cookies.update(response.cookies)
                
                if response.status_code == 404:
                    print("============completed============",
                        page, self.current_url)
                    break
                elif response.status_code == 412:
                    print("status 412, check the logs")
                elif response.status_code == 200:
                    print("================Page Scraped============== ",
                        page, self.current_url)
                    if not category_id:
                        tree = html.fromstring(response.text)
                        if self.current_url.endswith("/list"):
                            title = tree.xpath(
                                "//div[@class='list']//div[@class='index_title']//h3/text()")
                        elif self.current_url.endswith("/new_list"):
                            title = tree.xpath(
                                "//div[@class='index_title']//h3/text()")

                        _response = requests.post(f"{self.server_url}api/categories/",
                                                data={
                                                    "name": title
                                                })
                        category_id = _response.json()["id"]
                    page_responses.append(response.text)
                page += 1

        return (page_responses, category_id)

    def get_articles(self):
        """
        calls the articles method to store the articles in the database for every start url
        """
        articles = self.process_pages()
        category_id = articles[1]
        for data in articles[0]:
            self.process_articles(data, category_id)

    def process(self):
        """
        This main method you call to  spin off the parsing

        it will loop through all the urls and get the articles list then gets the content for the article
        -----
        """
        for url in self.start_urls_names:
            self.current_url = url
            self.get_articles()
            self.get_article_contents()
