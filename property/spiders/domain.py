import scrapy
from property.items import PropertyItem
from property.items import MarketTrends


class DomainSpider(scrapy.Spider):
    name = 'domain'
    allowed_domains = ['domain.com.au']
    start_urls = [
        'https://www.domain.com.au/sale/melbourne-region-vic/town-house/?excludeunderoffer=1&establishedtype=new']

    properties = []
    detail = PropertyItem()
    market_trends = MarketTrends()
    suburb_profiles = []

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.access_sublink)

    def access_sublink(self, response):
        # gather house basic data from each follow link, each page has list of houses
        # then loop every single one and access the follow link to grab the data
        for item in response.css('div.css-1mf5g4s li.css-1qp9106'):
            print("url>>>>>>", item.css('a::attr(href)').get())
            yield scrapy.Request(item.css('a::attr(href)').get(),
                                 callback=self.parse_property)

        # for paginations, if it has next page of list, then access the url from the <a href />
        next_prev_url = response.css('div.css-1t2vh5b a.css-1lkjjfg::attr(href)')
        # check current page if its first page
        if len(next_prev_url) > 1:
            yield scrapy.Request("https://www.domain.com.au" + next_prev_url[1].get(), callback=self.access_sublink)
        # check if list has next page
        elif len(next_prev_url) == 1 and next_prev_url.get().split("page=")[1] == "2":
            yield scrapy.Request("https://www.domain.com.au" + next_prev_url.get(), callback=self.access_sublink)
        # return self.properties

    def parse_property(self, response):
        # check if price data under the html span tag, then add price
        # but in some other pages, the price data is under div tag rather than span
        # check the span and div
        if response.css('div.css-s4rjyl div.css-i9gxme span.css-1w4p1vw::text').get():
            self.detail['price'] = response.css('div.css-s4rjyl div.css-i9gxme span.css-1w4p1vw::text').get()
        else:
            self.detail['price'] = response.css('div.css-s4rjyl div.css-i9gxme div.css-1texeil::text').get()
        self.detail['location'] = response.css('h1::text').get()
        room_num_array = response.css('span.css-lvv8is::text')
        self.detail['bed_num'] = room_num_array[0].get()
        self.detail['bath_num'] = room_num_array[2].get()
        self.detail['car_park_num'] = room_num_array[4].get()
        # check the square meters data, not all house data has so check if it has then add
        if "m²" in room_num_array[6].get():
            self.detail['space'] = room_num_array[6].get()

        if response.css('div.suburb-insights a::attr(href)').get():
            yield scrapy.Request("https://www.domain.com.au" + response.css('div.suburb-insights a::attr(href)').get(),
                                 callback=self.parse_suburb_profile)
        else:
            yield self.detail
        # self.properties.append(self.detail)
        # print(self.detail)

    def parse_suburb_profile(self, response):
        for trend in response.xpath('//*[@id="trends"]/div/div/div[2]/table'):
            self.market_trends['bed_num'] = trend.xpath('//*[@id="trends"]/div/div/div[2]/table/tbody[1]/tr/td['
                                                        '1]/text()').extract()[1]
            self.market_trends['property_type'] = trend.xpath('//*[@id="trends"]/div/div/div[2]/table/tbody[1]/tr/td['
                                                              '2]/text()').extract_first()
            self.market_trends['median_price'] = trend.xpath('//*[@id="trends"]/div/div/div[2]/table/tbody[1]/tr/td['
                                                             '3]/text()').extract_first()
            self.market_trends['avg_days_on_market'] = trend.xpath('//*[@id="trends"]/div/div/div[2]/table/tbody['
                                                                   '1]/tr/td[4]/text()').extract_first()
            self.market_trends['clearance_rate'] = trend.xpath('//*[@id="trends"]/div/div/div[2]/table/tbody['
                                                               '1]/tr/td[5]/text()').extract_first()
            self.market_trends['sold_this_year'] = trend.xpath('//*[@id="trends"]/div/div/div[2]/table/tbody['
                                                               '1]/tr/td[6]/text()').extract_first()
        self.detail['suburb_profile'] = self.market_trends
        yield self.detail
