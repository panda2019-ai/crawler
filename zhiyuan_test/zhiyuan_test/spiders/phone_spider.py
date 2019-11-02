import scrapy

# https://www.jihaoba.com/escrow/

class PhoneSpider(scrapy.Spider):
    name = 'phone'
    start_urls = [
        'https://www.jihaoba.com/escrow/'
    ]

    def parse(self, response):
        for ul in response.xpath('//div[@class="numbershow"]/ul'):
            phone = ul.xpath('li[contains(@class, "number")]/a/@href').re("\\d{11}")[0]
            price = ul.xpath('li[@class="price"]/span/text()').extract_first()[1:]
            if price.endswith('万'):
                price = int(float(price[:-1])*10000)
            else:
                price = int(price)

            yield {
                "phone": phone,
                "price": price
            }
        
        next = "https://www.jihaoba.com" + response.xpath('//a[@class="m-pages-next"]/@href').extract_first()
        yield scrapy.Request(next)