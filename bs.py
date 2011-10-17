#!/usr/bin/env python
#encoding=utf8

""" Cada médico está contido em uma tag html do tipo 
    <li class="dsimple ">. Usamos esta tag para separar os médicos.
    A totalidade dos dados dos médicos estão contidos em uma tag 
    <div class="mdata">.
    O nome está na primeira tag <a> após a tag mencionada acima.
    Campo de atuação e localidade estão contidos em uma tag 
    <div class="comp">.
    Para entender veja o código fonte html.
    """

from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import re
import time
import pickle 

onco = u'http://medial-saude.guiareunimedicos.med.br/index.pl?act=sear\
ch&_id_=172&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=\
0&q=oncologia#results'

cancer = u'http://www.guiareunimedicos.med.br/index.pl?act=search&_id_=\
172&_ev_=Submit&_formSearchSubmit=%3Adefault%3A&type=0&country=0&q=canc\
erologia#results'

def fetch_html(url):
    """gets html source code from url. Handles HTTP 503s"""

    req = urllib2.Request(url)
    count = 0
    html = None
    maxwait = 15
    while not html:
        try: html = urllib2.urlopen(req)
        except urllib2.HTTPError, e:
            print e
            print 'Will try again a sec from now'
            count += 1
            if count < maxwait:
                time.sleep(count)
            else: time.sleep(maxwait)
            html = None
        else:
            return html    

#print fetch_html(onco)
    
def get_bottomURLs(url, pickle_saved):
    """The search results are scattered among several urls listed at the
    bottom of the html source. 
    (the numbers at the bottom of the web page -- inside a tag of the 
    sort <div class="cx-step-full-index">) 
    This function fetches them and return as list.
    pickle_saved: a pickle dumped dictionary of the form resultpage
    -link number: url"""
    
    html = fetch_html(url)     
    filtro = SoupStrainer('div', attrs={'class': 'cx-step-full-index'})
    soup = BeautifulSoup(html.read(), filtro)
    data = soup('a')
    with open(pickle_saved,'rb') as saved_data:
        urls = pickle.load(saved_data)
    for i in data:
        #print len(urls)
        url = i['href']
        number = i.text
        if number not in urls:
            urls[number] = 
    with open(pickle_saved, 'wb') as savedata:
        pickle.dump(urls, savedata)
    return urls
            
def get_allURLs(baseSearchURL):
    """"Gets the URLs containing the remaining data from the search"""
    
    html = fetch_html(baseSearchURL)
    filtro = SoupStrainer('span', attrs={'class': 'cx-step-total-count'})
    data = BeautifulSoup(html.read(), filtro)
    hits = float(data.text)
    print 'hits:', hits
    if hits.is_integer:
        urlNumber = int(hits/10) #because 10 hits are displayed per page
    else:
        urlNumber= int(hits/10 + 1)
    urls = get_bottomURLs(baseSearchURL, 'pickle_saved')
    while len(urls) < urlNumber:
        #keep appending the last url listed at the bottom links 
        nextURL = get_bottomURLs(urls[len(urls)])
        print 'nextURL', nextURL
        urls.append(nextURL)
        print 'counted urls', len(urls)
    return urls     
   
def get_medics(url):
    """ pega os trechos de código html de uma url de resultados de busca 
    na página www.guiareunimedicos.med.br contendo informações dos médi-
    cos.
    Retorna uma lista com objetos BeautifulSoup contendo dados corres-
    pondentes a cada médico"""
    
    html = fetch_html(url)
    soup = BeautifulSoup(html.read())
    #first BS object to append to:
    medicdata = soup.findAll('li', attrs={'class': re.compile('dsimple')}) 
    for url in urls[1:]:
        html = urllib.urlopen(url)
        soup = BeautifulSoup(html.read())
        medicdata += soup.findAll('li', attrs={'class': re.compile('dsimple')})
    return medicdata
    
def get_name(medic):
    """Pega um objeto BS com dados do médico e extrai seu nome."""
    
    mdata = medic.find('div', attrs={'class': 'mdata'})
    # o nome está no primeiro tag <a> dentro de mdata:
    nome = mdata.findNext('a') 
    return nome.text
    
def get_phone(medic):
    """Pega um objeto BS com dados do médico e retorna uma lista de seus
     telefones"""
     
    spantag = medic.findAll('span')
    telefones = [ i.text for i in spantag ]
    return telefones
    
def get_moredata(medic):
    """ Retorna dados de especialização e localidade, nesta ordem."""
    
    data = medic.find('div', attrs={'class': 'comp'})
    field = data.contents[0]
    place = data.contents[2]
    return field, place
    
def debug(BaseSearchURL):
    """Meramente para testes, mostra resultados em stdout"""
    
    urls = get_allURLs(BaseSearchURL)
    medicos = get_medics(urls)
    for medico in medicos:
        nome = get_name(medico)
        telefone = get_phone(medico)
        campo, local = get_moredata(medico)
        print '-----------'
        print nome, campo, local, ', '.join(telefone)
    print len(medicos)


urls = get_allURLs(onco)
print len(urls)

#debug(onco)



    

