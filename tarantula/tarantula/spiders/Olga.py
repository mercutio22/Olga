
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from tarantula.items import OlgaItem
from scrapy.http import Request

class OlgaSpider(CrawlSpider):
    """This crawler gets the physician's name and his homepage url."""
    
    name = 'Olga'
    DOWNLOAD_DELAY = 6 #para tentar evitar ser banido
    #ROBOTSTXT_OBEY = True
    #CONCURRENT_REQUESTS = 1
    FEED_URI = '/home/mercutio22/gitcode/MedicWebsites.csv'
    FEED_FORMAT = 'csv'
    USER_AGENT = "Googlebot/2.1 ( http://www.google.com/bot.html )"
    #allowed_domains = ['guiareunimedicos.med.br']
    start_urls = (
        'http://medial-saude.guiareunimedicos.med.br/index.pl?act=searc\
h&_id_=172&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0\
&q=oncologia#results/',
       'http://www.guiareunimedicos.med.br/index.pl?act=search&_id_=17\
#2&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0&q=cancer\
#ologia#results/' )
    rules = (
        Rule(SgmlLinkExtractor(allow=r"V=", restrict_xpaths='//a[text()=">"]'),
        callback='parse_next', follow=True),
        #Rule(SgmlLinkExtractor(allow=r"V=", restrict_xpaths='//div[contains(@class, "mdata")]/a/@href'),
        #callback='parse_item', follow=True),
    )

    def parse_item(self, response):

            hxs = HtmlXPathSelector(response) ###
            i = OlgaItem()
            i['name'] = hxs.select('//big/text()').extract()
            i['clinics'] = hxs.select('//h2/a/text()').extract()
            data = hxs.select('//div[contains(@class, "stab data")]')
            addresses = [ x.select('./p/text()').extract() for x in data ]
            addresses = [ ''.join(x) for x in addresses ]
            addresses = [ x.replace('Telefone(s): \r\n\r\n\r\n', '') for x in addresses ]
            addresses = [ x[2:] for x in addresses ]
            i['addresses'] = addresses
            i['phones']  = hxs.select('//span[@id]/text()').extract()
            return i
            

    def parse_next(self, response):
    
        hxs = HtmlXPathSelector(response)
        mdata = hxs.select('//div[contains(@class, "mdata")]')
        links = mdata.select('./a/@href').extract()
        #names = mdata.select('./a/text()').extract()

        for link in links:
            yield Request(link, callback=self.parse_item)

        #~ items = []
        #~ for index in range(len(names)):
            #~ i = OlgaItem()
            #~ i['name'] = names[index]
            #~ i['link'] = links[index]
            #~ items.append(i)
        #~ return items
        
