#encoding=utf-8

from scrapy.spider import BaseSpider
from  medialSpider.items import DoctorSite
import scrapy.selector

class medialSpider(BaseSpider):
    """Should only get the physician's name and its URL; you can use it
    to store in a JSON file by 'doing scrapy crawl medialSpider --set
    FEED_URI=physicians.json --set FEED_FORMAT=json' """

    
    DOWNLOAD_DELAY = 2 #slowing down the crawling speed
    name = 'medialSpider'
    #allowed_ domains = ['medial-saude.guiareunimedicos.med.br']
    start_urls = [
        'http://medial-saude.guiareunimedicos.med.br/index.pl?act=searc\
h&_id_=172&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0\
&q=oncologia#results/',
        'http://www.guiareunimedicos.med.br/index.pl?act=search&_id_=17\
2&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0&q=cancer\
ologia#results/' ]

    def getNext():
        """ This is a trick to know which is the current pagenumber:
        I select the html element containing the pagenumbers, extract
        the text and convert into an int.
        Returns the next results-page URL.
        """
        
        element = hsx.select('/html/body/div[2]/div/div[2]/div[2]/div/d\
iv/div/div[2]/div[2]/div[2]/div[2]/div/div/div[2]')
        pagenumber = element.select('./text()').re('\d')[0]
        npage = str(int(pagenumber) + 1)
        Xpath = './a[contains(text(),"' + npage + '")]/@href'
        nextURL = element.select(Xpath).extract()
        return nextURL
        
    def parse(self, response):
        hxs = scrapy.selector.HtmlXPathSelector(response)
        basepath = hxs.select('/html/body/div[2]/div/div[2]/div[2]/div/\
div/div/div[2]/div[2]/div[2]/div/ul/li/div/a')
        links = basepath.select('./@href').extract()
        names = basepath.select('./text()').extract()        
        items = []
        for i in range(len(names)):
            DoctorSite = DoctorSite()
            DoctorSite[name] = name[i]
            DoctorSite[link] = links[i]
            items.append(DoctorSite)
        return items               
        
                
        #filename = response.url.split('=')[-1].split('#')[0]
        #um bom nome ao arquivo para salvar os dados --> idéia: oque es-
        #tá entre 'results/' e o '='precedente.
        #with open(filename, 'wb')as dump:
        #    dump.write(response.body)
        
