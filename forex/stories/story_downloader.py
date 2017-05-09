import pprint

import feedparser

class Downloader:

    feed_urls = (
        'http://www.nytimes.com/services/xml/rss/nyt/GlobalBusiness.xml',
        'http://newsrss.bbc.co.uk/rss/newsonline_world_edition/business/rss.xml',
    )

    def iterate_stories(self):
        for url in self.feed_urls:
            s = feedparser.parse(url)
            for entry in s.entries:
                entry['feed_url'] = url
                yield entry;


if __name__ == '__main__':

    downloader = Downloader()

    for story in downloader.iterate_stories():

        print(story.title)
        print(story.description)
        print(story.link)
        print(story.published_parsed)
        print()
