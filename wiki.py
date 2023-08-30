import wikipediaapi
import html2text

wiki = wikipediaapi.Wikipedia(
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
    "ko",
    extract_format=wikipediaapi.ExtractFormat.HTML,
)
page = wiki.page("이순신")
html = html2text.html2text(page.text)
with open(f"{page.title}.md", "w") as f:
    f.write(html)
