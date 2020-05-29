import requests
import re
from bs4 import BeautifulSoup


def write_file_from_wordpress(start_url, filename):
    """
    Scrapes a Wordpress page and downloads its content, chapter by chapter,
    saving all that information to the given file
    :param start_url: URL of the first chapter to scrape
    :param filename: path to output file
    """
    chapters = []
    url = start_url
    while url:
        # grab page using a normal http request
        response = requests.get(url)
        webpage_text = response.content.decode()  # implicitly UTF-8
        soup = BeautifulSoup(webpage_text, 'html.parser')
        # find title and build body out of <p> and <hr> tags
        chapter_title = soup.find(class_='entry-title').text
        chapter_body_tags = [tag for tag in soup.find(class_='entry-content').children
                             if tag.name in ('p', 'hr')
                             and not re.match(r'.*(?:Previous|Next)\s+Chapter', tag.text)
                             ]
        chapter_body = '\n\n'.join(
            '---' if tag.name == 'hr'
            else re.sub(r'</?(?:i|em)>', '*',
                        re.sub(r'</?(?:b|strong)>', '**',
                               ''.join(str(c) for c in tag.children)))
            for tag in chapter_body_tags
        )
        chapters.append({
            'title': chapter_title,
            'text': chapter_body,
        })
        print("Processed chapter:", chapter_title)
        # advance to next chapter, if possible
        next_chapter_tag = soup.find('a', string=lambda s: s and re.match(r'.*Next\s+(?:Chapter|Page)', s))
        url = next_chapter_tag and next_chapter_tag['href']
        if not url:
            print(soup.find_all('a'))
            continue

    # output to desired filename
    with open(filename, 'w') as outfile:
        outfile.write(
            '\n\n========================\n\n'.join(
                f'## {c["title"]}\n\n{c["text"]}' for c in chapters
            )
        )
