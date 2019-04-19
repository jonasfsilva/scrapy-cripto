import scrapy
import smtplib
from scrapy.selector import Selector


class LitecoinSpider(scrapy.Spider):
    name = "litecoin"

    def start_requests(self):
        urls = [    
            'https://dolarhoje.com/bitcoin/', 
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'pagina-preco%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)

        sel = Selector(response)
        results = sel.xpath("//*[contains(@id, 'nacional')]/@value")
        litecoin_value = '' 
        for result in results:
            if result.extract():
                litecoin_value = result.extract()
                print(result.extract())

        filename = 'somentevalor-%s.html' % page
        with open(filename, 'w') as file2:
            file2.write("<h1>{0}</h1>".format(litecoin_value))

        # send_mail('texto')

# TODO tutorial de envio de email pelo gmail
# https://stackabuse.com/how-to-send-emails-with-gmail-using-python/
def send_mail(message):
    print('SEND EMAIL')
    gmail_user = 'jonasscrapy@gmail.com'  
    gmail_password = 'taki2020'
    
    sent_from = 'jonasscrapy@gmail.com'  
    to = ['ferreirajonasss@gmail.com']  
    message = 'Preço do Litecoin'  
    
    try:  
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, message)
        server.close()
    except:
        print('Something went wrong...')