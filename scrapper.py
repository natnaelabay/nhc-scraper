import requests
from bs4 import BeautifulSoup
from abc import abstractmethod, ABC
from lxml import etree


class Scrapper(ABC):
    
    @property
    @abstractmethod
    def fields(self):
        raise NotImplementedError()
    
    @property
    @abstractmethod
    def start_urls_names(self):
        raise NotImplementedError()

    def run(self):
        print("executing")
        return True

    def _export_csv(self):
        print("workasdasd")
        return True

    def _export_to_database(self):
        print("workasdasd")

class Implemented(Scrapper):
    start_urls_names = {
        #'http://www.csrc.gov.cn/pub/newsite/zjhxwfb/xwdd': '证监会要闻'
        'http://www.csrc.gov.cn/csrc/c100028/common_xq_list.shtml': '证监会要闻',
        'http://www.csrc.gov.cn/csrc/c100029/common_list.shtml': '新闻发布会',
        'http://www.csrc.gov.cn/csrc/c100039/common_list.shtml': '政策解读'
    }
    fields = [
        "time_zone",
        "resource_type",
        
    ]
    def __init__(self):
        print("worked")


    def work(self):
        url = "http://www.nhc.gov.cn/wjw/gfxwjj/list.shtml"

        try:
            response = requests.get(url,proxies={
                "http": "127.0.0.1"
            })
            response.raise_for_status()  # Check for HTTP request errors
        except requests.exceptions.RequestException as e:
            print("Error:", e)
            return

        soup = BeautifulSoup(response.text, "html.parser")
        dom = etree.HTML(str(soup))
        
        # Use XPath to select elements
        data = dom.xpath("//div[@class='list']//ul/li")

        for item in data:
            print(item.text)

Implemented().work()