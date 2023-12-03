import scrapy

class CleverSpider(scrapy.Spider):

    name = "clever"
    start_urls = ["https://www.clever-media.ru/books/"]

    def parse(self, response):
        for link in response.css('div.card-mini__title a::attr(href)'):
            yield response.follow(link, callback=self.parse_book)
        for i in range(2, 3):
            next_page = f'https://www.clever-media.ru/books/?PAGEN_1={i}/'
            yield response.follow(next_page, callback=self.parse)

    def parse_book(self, response):
        name = response.css('h1.item__heading::text').get()
        if name[-1] != '"' or name[0] != '"':
            name = '"' + name + '"'

        try:
            author = response.css('div.item__params-value a::text')[1].get()
        except:
            author = '-'

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

        available = False
        if response.css('div.item__order-btn-wrapper button::text').get().strip() == "В корзину":
            available = True

        min_age = 0
        for i in range(15):
            try:
                if response.css('div.item__params-label::text')[i].get() == "Возраст:":
                    min_age = response.css('div.item__params-value::text')[i].get()[:-1]
            except:
                break

        ISBN = ""
        for i in range(15):
            try:
                if response.css('div.params__line span::text')[i].get() == "ISBN":
                    ISBN = response.css('div.params__line div::text')[i].get().replace('-', '')
            except:
                break

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



# response.css('a::attr(data-name)').get() имя книги с главной страницы
# response.css('div.card-mini__title a::attr(href)').get() дополнение к ссылке для перехода к конкретной книге к главной
# response.css('span.card-mini__author-name a::text').get()  автор с главной
# response.css('p.card-mini__price-value::text').get() цена с главной
# response.css('p.card-mini__discount.badge.badge--discount::text').get() скидка с главной
# response.css('span.card-mini__age::text').get() возрастное ограничение с главной

# response.css('div.params__value::text')[0].get() возрастное ограничение со страницы книги (может не быть)
# response.css('h1.item__heading::text').get() название
# response.css('div.item__params-value a::text')[1].get() автор (может не быть)
# response.css('div.item__actual-price span::text').get() цена
# response.css('span.badge.badge--discount::text').get()[16:-1] скидка (может не быть, наверное)
# response.css('div.params__value::text')[1].get() кол-во страниц
# response.css('div.params__value::text')[3].get() вес
# response.css('div.params__value::text')[5].get() тип обложки
# response.css('div.params__value a::text').get() серия

# response.css('div.rating.review__rating p::text')[1]  отзыв
# response.css('div.item__order-btn-wrapper button::text').get().strip() есть ли в наличии, если есть - "В корзину"