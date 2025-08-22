# 🕷️ USP Monitor - Scrapy Spider 

Este projeto utiliza o framework **[Scrapy](https://scrapy.org/)** em Python para monitorar notícias da seção **Institucional** do [Jornal da USP](https://jornal.usp.br/home-institucional/). 

O crawler percorre até **15 páginas** de resultados, coleta **títulos** e **URLs** das matérias e identifica menções a palavras-chave relacionadas ao **USPproClima** e outros termos relevantes. 
## 🚀 Funcionalidades 

- Raspa notícias da seção **Institucional** do Jornal da USP 
- Percorre até **15 páginas de listagem** 
- Extrai: 
    - Título da notícia 
    - URL da notícia 
    - Palavra-chave encontrada 
- Exporta os resultados em **JSON**, **CSV** ou outros formatos suportados pelo Scrapy 
    
 ## ⚙️ Instalação 

1. Clone este repositório: 

    ``` 
    git clone https://github.com/seu-usuario/uspmonitor.git 
    cd uspmonitor 
    ``` 

2. Instale as dependências: 

    ```bash 
    pip install scrapy 
    ``` 
    
    --- 
    
    ## ▶️ Como usar 
    
    Para rodar a spider e salvar os resultados em **JSON**: 
    ```bash 
    scrapy crawl jornalusp_institucional -o resultados.json 
    ``` 
    Ou em **CSV**: 
    
    ```bash 
    scrapy crawl jornalusp_institucional -o resultados.csv 
    ``` 
    --- 

    ## 🔍 Configuração de Palavras-Chave 
    
    As palavras-chave monitoradas estão no arquivo: `uspmonitor/spiders/jornalusp_institucional.py` 
   
    ```python 
    palavras = ["USPproClima", "Patrícia Iglecias", "USP ProClima", "Jorge Tenório", "Fernanda Brando", "Edimilson Freitas", "Ildo Sauer", "Tamara Gomesth"] 
    ``` 
    
    Você pode adicionar, remover ou alterar termos conforme necessário. 
    --- 
    ## 📊 Exemplo de saída (JSON) 
    ```json 
    [ { "titulo": "USP é a melhor universidade ibero-americana pelo terceiro ano consecutivo, segundo ranking ARWU", "url": "https://jornal.usp.br/comunicados/usp-e-considerada-a-melhor-universidade-ibero-americana-pelo-terceiro-ano-consecutivo-segundo-ranking-arwu/", "palavra_encontrada": "ibero" } ] 
    ``` 
    --- 
    
    ## 📅 Limite de Páginas
    
     A spider percorre no máximo **15 páginas** da seção institucional. Esse valor pode ser ajustado na classe `JornalUspInstitucionalSpider`: ```python max_pages = 15 ``` --- 
     
     ## 🤝 Contribuindo
     
      Sinta-se à vontade para abrir **issues** ou enviar **pull requests** com melhorias.
    
     _Att. Charlon Fernandes Monteiro_