import scrapy

class JornalUspInstitucionalSpider(scrapy.Spider):
    name = "jornalusp_institucional"
    allowed_domains = ["jornal.usp.br"]
    start_urls = ["https://jornal.usp.br/home-institucional/"]

    # paginação
    page_number = 1
    max_pages = 15

    def parse(self, response):
        """Coleta os links das notícias listadas"""
        artigos = response.css("h2.elementor-post__title a::attr(href)").getall()

        for artigo in artigos:
            yield response.follow(artigo, self.parse_article)

        # Paginação para próximas páginas
        if self.page_number < self.max_pages:
            self.page_number += 1
            next_page = f"https://jornal.usp.br/home-institucional/page/{self.page_number}/"
            yield response.follow(next_page, callback=self.parse)

    def parse_article(self, response):
        """Extrai título, texto e procura palavras-chave"""
        # Título compatível com variações
        titulo = response.css("h1.elementor-heading-title::text").get() \
            or response.css("h1::text").get()

        # Pega parágrafos do corpo
        paragrafos = response.css("div.elementor-widget-container p::text").getall()
        conteudo = " ".join(paragrafos).strip()

        # Normalização
        titulo_norm = (titulo or "").lower()
        conteudo_norm = (conteudo or "").lower()

        # Palavras de busca
        palavras = [
            "pro clima", "proclima", "usp pro clima", "usp proclima",
            "patrícia iglecias"
        ]

        # Procura palavras e retorna item
        for palavra in palavras:
            if palavra.lower() in titulo_norm or palavra.lower() in conteudo_norm:
                yield {
                    "titulo": titulo.strip() if titulo else None,
                    "url": response.url,
                    "palavra_encontrada": palavra,
                }
                break  # evita duplicados
