import aiohttp
from bs4 import BeautifulSoup
import json
import asyncio

f = {
    "quotes": []
}

urls_data = {}

async def fetch_url_data(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            res = await r.text()
            print(f"Fetched | {url}")
            urls_data[url] = res


def parser(res):

    soup = BeautifulSoup(res, "html.parser")
    quotes = soup.select("div.quoteText")

    for quote in quotes:
        quot = ""
        for x in quote.descendants:
            if "―" in x.get_text(strip=True):
                break
            if x.name == "br":
                quot += "\n"
            quot += x.get_text(strip=True)
        
        quot = quot.strip().strip("“").strip("”")
        author = quote.find("span", class_="authorOrTitle").get_text(strip=True)
        book_tag = quote.find("a", class_="authorOrTitle")
        book = book_tag.get_text(strip=True) if book_tag else None

        if len(quot) > 2000:
            continue

        f["quotes"].append(
            {
                "quote": quot,
                "author": author.strip(","),
                "book": book if book is not None else None
            }
        )


async def main():
    tasks = [fetch_url_data(f"https://www.goodreads.com/quotes?page={x}") for x in range(1,101)]
    await asyncio.gather(*tasks)

    for x in range(1, 101):
        parser(urls_data[f"https://www.goodreads.com/quotes?page={x}"])

    with open("quotes.json", "w", encoding="utf-8") as file:
        json.dump(f, file, indent=4)
    
    print("All quotes have been written to 'quotes.json'")

asyncio.run(main())
