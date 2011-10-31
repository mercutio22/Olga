
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from tarantula.items import OlgaItem
from random import uniform

class OlgaSpider(CrawlSpider):
    name = 'Olga'
    DOWNLOAD_DELAY = 60 #para tentar evitar ser banido
    ROBOTSTXT_OBEY = True
    CONCURRENT_REQUESTS = 1
    USER_AGENT = "Googlebot/2.1 ( http://www.google.com/bot.html )"
#    FEED_URI = 'MedicWebSites.csv'
#    FEED_FORMAT = 'csv'
    #allowed_domains = ['guiareunimedicos.med.br']
    #handle_httpstatus_list = [503]
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
        Rule(SgmlLinkExtractor(allow=r"V=", restrict_xpaths='//a[text()=">"]'),
        callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        hxs = HtmlXPathSelector(response)
        mdata = hxs.select('//div[contains(@class, "mdata")]')
        links = mdata.select('./a/@href').extract()
        names = mdata.select('./a/text()').extract()
        
        items = []
        for index in range(len(names)):
            i = OlgaItem()
            i['name'] = names[index]
            i['link'] = links[index]
            items.append(i)
        return items
