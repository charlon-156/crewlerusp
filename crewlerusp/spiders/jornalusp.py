import scrapy

class JornalUspInstitucionalSpider(scrapy.Spider):
    name = "jornalusp_institucional"
    allowed_domains = ["jornal.usp.br"]
    start_urls = ["https://jornal.usp.br/home-institucional/"]

    page_number = 1
    max_pages = 30

    def parse(self, response):
        self.logger.info(f"🔎 Listando página {self.page_number}: {response.url}")

        # Seletores de links de notícia (multiples padrões)
        artigos = response.css("h2.elementor-post__title a::attr(href)").getall()
        artigos += response.css("article a::attr(href)").getall()

        artigos = list(set(artigos))  # remove duplicados

        if not artigos:
            self.logger.warning(f"⚠️ Não encontrou artigos na página: {response.url}")

        for artigo in artigos:
            yield response.follow(artigo, self.parse_article)

        if self.page_number < self.max_pages:
            self.page_number += 1
            next_page = f"https://jornal.usp.br/home-institucional/page/{self.page_number}/"
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        self.logger.info(f"➡️ Abrindo matéria: {response.url}")

        # Tenta múltiplos seletores de título
        titulo = response.css("h1.elementor-heading-title::text").get()
        if not titulo:
            titulo = response.css("h1.entry-title::text").get()

        # Pega textos gerais do corpo
        paragrafos = response.css("div.elementor-widget-container p::text").getall()
        if not paragrafos:
            # fallback, tenta outra estrutura
            paragrafos = response.css("div.post-content p::text").getall()

        conteudo = " ".join(paragrafos).strip()

        self.logger.debug(f"Título capturado: {titulo}")
        self.logger.debug(f"Conteúdo capturado (primeiros 100 chars): {conteudo[:100]}")

        titulo_norm = (titulo or "").lower()
        conteudo_norm = (conteudo or "").lower()

        palavras = [
            "pro clima", "proclima", "usp pro clima", "usp proclima",
            "patrícia iglecias", "jorge tenório", "fernanda brando",
            "edimilson freitas", "ildo sauer", "mudanças climáticas",
            "sustentabilidade"
        ]

        encontrado = False
        for palavra in palavras:
            if palavra.lower() in titulo_norm or palavra.lower() in conteudo_norm:
                encontrado = True
                yield {
                    "titulo": titulo.strip() if titulo else None,
                    "url": response.url,
                    "palavra_encontrada": palavra,
                }
                break

        if not encontrado:
            self.logger.info(f"❌ Nenhuma palavra encontrada na matéria: {response.url}")
