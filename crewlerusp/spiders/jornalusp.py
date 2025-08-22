import scrapy

class JornalUspInstitucionalSpider(scrapy.Spider):
    name = "jornalusp_institucional"
    allowed_domains = ["jornal.usp.br"]
    start_urls = ["https://jornal.usp.br/home-institucional/"]

    # contador de páginas
    page_number = 1
    max_pages = 15

    def parse(self, response):
        # Para cada notícia listada na página
        for artigo in response.css("h2.elementor-post__title a::attr(href)").getall():
            yield response.follow(artigo, self.parse_article)

        # Paginação limitada
        if self.page_number < self.max_pages:
            self.page_number += 1
            next_page = f"https://jornal.usp.br/home-institucional/page/{self.page_number}/"
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        titulo = response.css("h1::text").get()
        conteudo = " ".join(response.css("p::text").getall())

        # Palavras-chave
        palavras = ["USPproClima", "Patrícia Iglecias",  "USP ProClima", "Jorge Tenório", "Fernanda Brando", "Edimilson Freitas", "Ildo Sauer", "Tamara Gomesthh"]

        for palavra in palavras:
            if palavra.lower() in (titulo or "").lower() or palavra.lower() in (conteudo or "").lower():
                yield {
                    "titulo": titulo.strip() if titulo else None,
                    "url": response.url,
                    "palavra_encontrada": palavra,
                }
