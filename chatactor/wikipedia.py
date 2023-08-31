import os
import wikipediaapi
import html2text


def wikipedia2markdown(
    query: str,
    path: str = "profiles",
    region: str = "ko",
) -> bool:
    """
    Save wikipedia page as markdown file

    Args:
        query: word to search
        path: path to save
        region: region to search
    Returns: 성공 여부

    """

    wiki = wikipediaapi.Wikipedia(
        "CoolBot/0.0 (https://example.org/coolbot/; coolbot@example.org)",
        language=region,
        extract_format=wikipediaapi.ExtractFormat.HTML,
    )

    page = wiki.page(query)

    if not page.exists():
        return False

    html = html2text.html2text(page.text)

    with open(os.path.join(path, f"{query}.md"), "w") as f:
        f.write(html)

    return True
