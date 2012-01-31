# coding=gbk
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from WebCrawler.items import ProductItem
from scrapy.http.request import Request
from scrapy import log


class SiteSpider(BaseSpider):
    
    name = "360buy"
    #allowed_domains = "360buy.com"
    start_urls = [
        "http://www.360buy.com/products/670-677-683.html"
    ]
    
    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        links = hxs.select('//div[contains(@class, "m clearfix")]/div/a[not(@class)]/text()').extract()
        maxIndex = int(links[len(links)-1])
        pagelinks = []
        for l in range(maxIndex):
            pagelinks.append("http://www.360buy.com/products/670-677-683-0-0-0-0-0-0-0-1-1-" + str(l+1) + ".html")
        return [ Request(url, callback=self.parseItem) for url in pagelinks ]
        
    
    def parseItem(self, response):
        hxs = HtmlXPathSelector(response)
        productItems = hxs.select('//div[contains(@id, "plist")]/ul/li')
        items = []
        for product in productItems:
            pitem = ProductItem()
            pitem['sku'] = product.select('@sku').extract()[0]
            pitem['title'] = product.select('div[contains(@class, "p-name")]/a/text()').extract()[0]
            pitem['price'] = product.select('div[contains(@class, "p-price")]/img/@src').extract()[0]
            pitem['href'] = product.select('div[contains(@class, "p-name")]/a/@href').extract()[0]
            if len(product.select('div[contains(@class, "p-img")]/a/img/@src2').extract()) == 1:
                pitem['image'] = product.select('div[contains(@class, "p-img")]/a/img/@src2').extract()[0]
            else:
                pitem['image'] = product.select('div[contains(@class, "p-img")]/a/img/@src').extract()[0]
            pitem['evaluate'] = product.select('div[contains(@class, "extra")]/span[contains(@class, "evaluate")]/a/text()').extract()[0]
            pitem['reputation'] = product.select('div[contains(@class, "extra")]/span[contains(@class, "reputation")]/text()').extract()[0]
            items.append(pitem)
        return items
        