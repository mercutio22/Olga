#encoding=utf-8

from scrapy.spider import BaseSpider
from  tarantula.items import TarantulaItem
import scrapy.selector
from scrapy.http import Request, HtmlResponse

class medialSpider(BaseSpider):
    """Should only get the physician's name and its URL; you can use it
    to store in a JSON file by 'doing scrapy crawl medialSpider --set
    FEED_URI=physicians.json --set FEED_FORMAT=json' """

    
    #DOWNLOAD_DELAY = 2 #slowing down the crawling speed
    name = 'medialSpider'
    #allowed_ domains = ['medial-saude.guiareunimedicos.med.br']
    start_urls = [
        'http://medial-saude.guiareunimedicos.med.br/index.pl?act=searc\
h&_id_=172&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0\
&q=oncologia#results/']
       # 'http://www.guiareunimedicos.med.br/index.pl?act=search&_id_=17\
#2&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0&q=cancer\
#ologia#results/' ]

    Titems = [] #this will hold every TarantulaItem.
    Go = True
    counter = 1
    
    def getNext(self, hxs, counter):
        """ This is a trick to know which is the current pagenumber:
        I select the html element containing the pagenumbers, extract
        the text and convert into an int.
        Returns the next results-page URL.
        hxs = Scrapy HtmlXpathSelector object
        counter = an int representing the current-results page 
        """

        path = hxs.select('//div[contains(@class, "cx-step-full-index")]')
        nextURL = path.select('./a[contains(text(), "%s")]/@href' %counter)
        nextURL = nextURL.extract()
        nextURL = nextURL[0]
        print 'próxima url', nextURL
        return HtmlResponse(nextURL)

    def record(self, links, names):
        """Gets two equal-lenght lists of Doctor names and URLs
        Returns a list of TarantulaItems"""
        
        items = []
        for i in range(len(names)):
            aranha = TarantulaItem()
            aranha['name'] = names[i]
            aranha['link'] = links[i]
            items.append(aranha)
        return items      

    def parse(self, response):
        hxs = scrapy.selector.HtmlXPathSelector(response)
        basepath = hxs.select('/html/body/div[2]/div/div[2]/div[2]/div/\
div/div/div[2]/div[2]/div[2]/div/ul/li/div/a')
        links = basepath.select('./@href').extract()
        names = basepath.select('./text()').extract()
        nextUrl = medialSpider.getNext(self, hxs, self.counter)
        #print 'proxima url', nextUrl
        Hits = '//span[contains(@class, "cx-step-total-count")]/text()'
        pages = hxs.select(Hits).extract()
        pages = float(pages[0])
        print 'Hits:',  pages
        while self.Go:
            #print currentPage, self.Go
            self.counter += 1
            currentItems = medialSpider.record(self, links, names)
            self.Titems.extend(currentItems)
            #print 'items:', self.Titems
            print 'Tipo:',  type('nextUrl')
            self.parse(nextUrl)
            if self.counter > pages:
                self.Go = False
        return self.Titems
        
        #filename = response.url.split('=')[-1].split('#')[0]
        #um bom nome ao arquivo para salvar os dados --> idéia: oque es-
        #tá entre 'results/' e o '='precedente.
        #with open(filename, 'wb')as dump:
        #    dump.write(response.body)
        
