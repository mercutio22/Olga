import re

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from tarantula.items import TarantulaItem

class OlgaSpider(CrawlSpider):
    name = 'Olga'
    DOWNLOAD_DELAY = 2 #para tentar evitar ser banido
    #allowed_domains = ['guiareunimedicos.med.br']
    #start_urls = ['http://www.guiareunimedicos.med.br/']
    start_urls = [
        'http://medial-saude.guiareunimedicos.med.br/index.pl?act=searc\
h&_id_=172&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0\
&q=oncologia#results/',
       'http://www.guiareunimedicos.med.br/index.pl?act=search&_id_=17\
#2&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0&q=cancer\
#ologia#results/' ]


    rules = (
        #Rule(SgmlLinkExtractor(allow=r"V=", restrict_xpaths='//div[co\
#ntains(@class, "cx-step-full-index")]'), callback='parse_item', follow=True),
        Rule(SgmlLinkExtractor(allow=r"V=", restrict_xpaths='//a[text()=">"]'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        mdata = hxs.select('//div[contains(@class, "mdata")]')
        links = mdata.select('./a/@href').extract()
        names = mdata.select('./a/text()').extract()
        
        items = []
        for index in range(len(names)):
            i = TarantulaItem()
            i['name'] = names[index]
            i['link'] = links[index]
            items.append(i)
        return items
