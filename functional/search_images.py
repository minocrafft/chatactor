from duckduckgo_search import DDGS


def search_images(keywords, return_count=5):
    with DDGS() as ddgs:
        ddgs_images_gen = ddgs.images(
            keywords,
            region="kr-kr",
            safesearch="on",
            size=None,
            color=None,
            type_image="photo",
            layout="Tall",
            license_image=None,
        )

        return [next(ddgs_images_gen) for _ in range(return_count)]
