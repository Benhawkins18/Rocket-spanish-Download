from bs4 import BeautifulSoup
import re
import mechanize
import cookielib
import csv
import csv, codecs, cStringIO
import os
import urllib2
import errno

br = mechanize.Browser()
br.set_handle_robots(False)   # ignore robots
br.set_handle_refresh(False)  # can sometimes hang without this
br.addheaders =  [('User-agent', 'Firefox')]

cj = cookielib.LWPCookieJar()



def log_in(br):
    
    
    
    url = 'http://members.rocketlanguages.com/Access/'

    response = br.open(url)
    
    br.select_form(nr=0) #= "benhawkins18@gmail.com"
#    for control in br.form.controls:
#        print control
#        print "type=%s, name=%s value=%s" % (control.type, control.name, br[control.name])
#    
    br["log"] = "benhawkins18@gmail.com"
    br["pwd"] = "sadiefat18"
    

    br.submit()
    
    cj.save('cookies.txt', ignore_discard=False, ignore_expires=False)
    
def download_cards_toa_csv(br):
    print 'jere'
    url = 'http://members.rocketlanguages.com/lessons/1338#extra-vocabulary'
    response = br.open(url)
    print response.read()
    html = response.read()
    soup = BeautifulSoup(html)
    
    spanish_list = []
    english_list = []
    
    for span in soup.findAll('span',attrs={'class':"WS_5"}):
        text = str(span.contents[0])
        text = re.sub('<[^<]+?>', '',text)
        print text
        
    for span in soup.findAll('span',attrs={'class':"pls WS_5"}):
        text = str(span.contents[0]).strip()
        text = re.sub('<[^<]+?>', '',text)
        
        
class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def write_text_to_csv():
    list_of_cards = []
    file = open('cards.txt')
    
    for line in file:
        list_of_cards.append(line.strip().split('\t')[::-1])
        

    with open('Carnival 18.5.csv', 'wb') as f:
        writer = UnicodeWriter(f)
        writer.writerows(list_of_cards)
    
    print 'finished making '
    
def make_sure_path_exists(path):
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise       
def download_sounds_from_rocket_spanish():
    folder_name = 'Rocket spanish sounds'
    make_sure_path_exists(folder_name)
    lines = 87
    for i in range(1,lines+1):
        
        file_name = folder_name+'/RocketSpanish 18.3 line '+str(i)+'.mp3'
        try:
            f = open(file_name,'wb')
            f.write(urllib2.urlopen('http://c458342.r42.cf0.rackcdn.com/RS3_18.3_Conversation_line'+str(i)+'.mp3').read())
            f.close()
            print 'sound downloaded'
        except urllib2.URLError:
            print "Bad URL or timeout"
            continue
        
#write_text_to_csv()
#cj.load('cookies.txt', ignore_discard=False, ignore_expires=False)
#download_cards_toa_csv(br)
log_in(br)
download_sounds_from_rocket_spanish()