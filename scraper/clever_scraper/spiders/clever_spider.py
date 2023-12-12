import scrapy

class CleverSpider(scrapy.Spider):

    name = "clever"
    start_urls = ["https://www.clever-media.ru/books/"]

    def parse(self, response):
        for link in response.css('div.card-mini__title a::attr(href)'):
            yield response.follow(link, callback=self.parse_book)
        for i in range(2, 101):
            next_page = f'https://www.clever-media.ru/books/?PAGEN_1={i}/'
            yield response.follow(next_page, callback=self.parse)

    def get_name(self, response):
        name = response.css('h1.item__heading::text').get()
        if name[-1] != '"' or name[0] != '"':
            name = '"' + name + '"'
        return name

    def get_author(self, response):
        try:
            author = response.css('div.item__params-value a::text')[1].get()
        except:
            author = '-'
        return author


    def get_raiting(self, response):
        rating = 0
        review_number = 1
        for i in range(1, 100):
            try:
                rating += int(response.css('div.rating.review__rating p::text')[i].get())
            except:
                review_number = i - 1
                break
        if (review_number == 0):
            avg_rating = 0
        else:
            avg_rating = rating / review_number
        return avg_rating, review_number

    def get_avaiability(self, response):
        available = False
        if response.css('div.item__order-btn-wrapper button::text').get().strip() == "В корзину":
            available = True
        return available


    def get_min_age(self, response):
        min_age = 0
        for i in range(15):
            try:
                if response.css('div.item__params-label::text')[i].get() == "Возраст:":
                    min_age = response.css('div.item__params-value::text')[i].get()[:-1]
            except:
                break
        if min_age != 0 and not(min_age.isdigit()):
            min_age = 0
        return min_age

    def get_ISBN(self, response):
        ISBN = ""
        for i in range(15):
            try:
                if response.css('div.params__line span::text')[i].get() == "ISBN":
                    ISBN = response.css('div.params__line div::text')[i].get().replace('-', '')
            except:
                break
        return ISBN
    def parse_book(self, response):
        name = self.get_name(response)
        author = self.get_author(response)
        avg_rating, review_number = self.get_raiting(response)
        available = self.get_avaiability(response)
        min_age = self.get_min_age(response)
        ISBN = self.get_ISBN(response)

        yield {
            'name' : name,
            'price' : response.css('div.item__actual-price span::text').get()[:-1],
            'discount' : response.css('span.badge.badge--discount::text').get()[16:-1],
            'author' : author,
            'min_age' : min_age,
            'rating' : avg_rating,
            'review_number' : review_number,
            'available' : available,
            'ISBN' : ISBN,
            'link' : response.url,
        }