# to run 
# scrapy crawl imdb_spider -o movies.csv

import scrapy

class ImdbSpider(scrapy.Spider):
    name = 'imdb_spider'
    
    # starts at movie url
    start_urls = ['https://www.imdb.com/title/tt1856101/']

    def parse(self,response):
        """
        starts on a movie page and navigates to Cast & Crew page

        response - response object from scrapy

        yields a scrapy request to parse Cast & Crew page
        """
        # create url for Cast & Crew page
        full_credit_url = response.url+"fullcredits"

        # navigates to Cast & Crew page
        # calls parse_full_credits method
        yield scrapy.Request(full_credit_url,callback=self.parse_full_credits)

    def parse_full_credits(self,response):
        """
        starts on the Cast & Crew page of a movie and navigates to each actor's page

        response - response object from scrapy

        yields a scrapy request to parse each actor's page
        """
        # create list of suburls of actor pages
        actor_url_list = [a.attrib["href"] for a in response.css("td.primary_photo a")]

        # for each actor with a suburl
        for url in actor_url_list:
            # create full url
            actor_url = response.urljoin(url)
            # navigate to actor page
            # call parse_actor_page method
            yield scrapy.Request(actor_url,callback=self.parse_actor_page)

    def parse_actor_page(self,response):
        """
        Goes through an actor's credits and returns all shows/movies they appeared in

        response - response object from scrapy

        yields dictionary containing all shows/movies they appeared in
        """
        # get actor name
        actor_name = response.css('div#name-overview-widget h1.header span::text').get()
        
        # get show/movie name
        for row in response.css('div#filmography div.filmo-row'):
            movie_or_TV_name = row.css("b a::text").get()
            yield{"actor" : actor_name, "movie_or_TV_name" : movie_or_TV_name}


