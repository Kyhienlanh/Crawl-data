import requests
from bs4 import BeautifulSoup
import pandas as pd

data = []
i = 0
for page in range(1, 31):
    if page == 1:
        url = "https://dantri.com.vn/xa-hoi.htm"
    else:
        url = f"https://dantri.com.vn/xa-hoi/trang-{page}.htm"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    main_div = soup.find('div', class_='main')
    article_list = main_div.find('div', class_='article list')
    articles = article_list.find_all('article', class_='article-item')

    for article in articles:
        title_news = article.find('a', class_="dt-text-black-mine").text.strip()
        content_title = article.find('div', class_="article-excerpt").find('a').text.strip()
        link = "https://dantri.com.vn/" + article.find('a', class_="dt-text-black-mine")['href']
        img = article.find('img')['data-src']

        print("Title:", title_news)
        print("Content:", content_title)
        print("Link:", link)
        print("Image:", img)

        article_data = {
            "Title": title_news,
            "Content": content_title,
            "Link": link,
            "Image": img
        }

        response_article = requests.get(link)
        soup_article = BeautifulSoup(response_article.content, 'html.parser')
        category_tag = soup_article.find("li", class_="dt-font-Inter dt-float-left before:dt-content-['›'] before:dt-text-xl before:dt-leading-none before:dt-text-ca0a4a8 before:dt-block before:dt-relative before:dt-float-left before:dt-mx-[5px] before:dt-my-0")
        category = category_tag.find('a').get_text() if category_tag and category_tag.find('a') else "Unknown"

        print("Category:", category)
        article_data["Category"] = category

        author_info = soup_article.find('div', class_="author-wrap")
        if author_info:
                author_img_tag = author_info.find('a', class_="author-avatar__picture")
                if author_img_tag and author_img_tag.img:
                    author_name = author_img_tag.img['alt']
                    author_image = author_img_tag.img['src']
                else:
                    author_name = "Unknown"
                    author_image = "Unknown"
                publish_time = author_info.find("time", class_='author-time').text.strip()
                author_link = "https://dantri.com.vn" + (author_img_tag["href"] if author_img_tag else "")
        else:
            author_name = "Unknown"
            author_image = "Unknown"
            publish_time = "Unknown"
            author_link = "Unknown"


        print("Author:", author_name)
        print("Author Image:", author_image)
        print("Publish Time:", publish_time)
        print("Author Link:", author_link)

        article_data["Author"] = author_name
        article_data["Author Image"] = author_image
        article_data["Publish Time"] = publish_time
        article_data["Author Link"] = author_link

        content_paragraphs = []
        article_content = soup_article.find('div', class_="singular-content")
        if article_content:
            paragraphs = article_content.find_all('p')
            for paragraph in paragraphs:
                content_paragraphs.append(paragraph.get_text().strip())
            article_text = '\n'.join(content_paragraphs)
        else:
            article_text = "Unknown"

        print("Article Content:\n", article_text)
        article_data["Article Content"] = article_text

        data.append(article_data)
        i += 1
        print("\n" + "=" * 50 + "\n")

df = pd.DataFrame(data)
df.to_csv("dantri_articles.csv", index=False)
print("so luong du lieu da crawl", i)
# xu li ngoai le
