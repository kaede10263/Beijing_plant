import scrapy
from ..items import PlantCrawlerItem

class QuotesSpider(scrapy.Spider):
    name = "plant_spyder"
    start_urls = [
            'http://tai2.ntu.edu.tw/PlantInfo.php',
        ]

    def parse(self, response):
        chunWei = "D:/GDbackup/PROJECT/tree/Beijing_plant/taiwan_plant.csv"
        allen = ""
        search = []
        count = 0
        with open(chunWei) as f:
            for line in f:
                if not line.strip():
                    continue
                search.append(line.split(",")[-1])
                count += 1   
                if (count == 101):
                    break
                
        for name in search:
            yield scrapy.FormRequest.from_response(
                        response,
                        formdata={'search': name},
                        callback=self.after_search,
                        meta={"name": name},
                        dont_filter=True
                    )

    def after_search(self, response):
        plant_url = []
        name = response.meta.get('name')
        for url in response.css('td'):
            link = url.css('a::attr(href)').extract()
            if (link != []):
                plant_url.append("http://tai2.ntu.edu.tw/" + link[0].replace("name", "des"))
                break

        if (plant_url != []):
            yield scrapy.Request(plant_url[0], 
                                callback=self.get_plant_info, 
                                meta={"name": name},
                                dont_filter=True)
        else:
            yield scrapy.Request("http://tai2.ntu.edu.tw/", 
                                callback=self.get_plant_info, 
                                meta={"name": name},
                                dont_filter=True)   

    def get_plant_info(self, response):
        self.logger.info(f"Visited {response.url}")
        items = PlantCrawlerItem()
        name = response.meta.get('name').strip()

        if (response.css('h1 em::text').get() is not None):
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

            items['originalName'] = name
        
        else:
            items['scientificName'] = ""
            items['chineseName'] = ""
            items['attribute'] = ""
            items['describe'] = ""
            items['distribution'] = ""
            items['originalName'] = name

        yield items    
        
