import aiohttp
from bs4 import BeautifulSoup
import time
import json
import asyncio

f = {
    "quotes": []
}


async def parser(url):
    
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as r:
            res = await r.text()
        
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
        print(f"{url} | Done")


async def main():
    tasks = []
    for x in range(1, 101):
        tasks.append(parser(f"https://www.goodreads.com/quotes?page={x}"))
    await asyncio.gather(*tasks)
    print("all fetched, writing")
    with open("quotes.json", "w") as file:
        json.dump(f, file, indent=4)


asyncio.run(main())
