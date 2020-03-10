import scrapy
from ..items import PlantCrawlerItem

class QuotesSpider(scrapy.Spider):
    name = "plant_spyder"
    start_urls = [
            'http://tai2.ntu.edu.tw/PlantInfo.php',
        ]

    def parse(self, response):
        search = []
        count = 0
        with open(r"E:\Download\plant_crawler-20200309T010426Z-001\plant_crawler\plant_crawler\spiders\taiwan_plant.csv") as f:
            for line in f:
                if not line.strip():
                    continue
                search.append(line.split(",")[-1])
                count += 1   
                if (count == 10):
                    break
                
        for name in search:
            yield scrapy.FormRequest.from_response(
                        response,
                        formdata={'search': name},
                        callback=self.after_search,
                        dont_filter=True
                    )

    def after_search(self, response):
        plant_url = []
        for url in response.css('td'):
            link = url.css('a::attr(href)').extract()
            if (link != []):
                plant_url.append("http://tai2.ntu.edu.tw/" + link[0].replace("name", "des"))
                break

        if (plant_url != []):
            return scrapy.Request(plant_url[0], callback=self.get_plant_info)

    def get_plant_info(self, response):
        self.logger.info("Visited %s", response.url)
        items = PlantCrawlerItem()
        
        scientificName = " ".join((response.css('h1 em::text').get().strip().replace("\xa0", " ")
                                , response.css('h1::text')[1].get().strip().replace("\xa0", "")))

        if (len(response.css('h1 em::text').getall()) > 1):
            scientificName = " ".join((scientificName
                                    , response.css('h1 em::text')[1].get().strip().replace("\xa0", " ")
                                    , response.css('h1::text')[2].get().strip().replace("\xa0", "")))
        
        items['scientificName'] = scientificName

        chineseName = response.css('h1::text')[-2].get().strip()
        items['chineseName'] = chineseName
        
        attribute = response.css('h1 span::text').get(default='empty').strip()
        items['attribute'] = attribute

        describe = response.css("li::text").getall()
        describe = "".join(describe)
        items['describe'] = describe

        distribution = response.css("td::text").getall()
        distribution = "".join(distribution)
        items['distribution'] = distribution

        yield items    
        
