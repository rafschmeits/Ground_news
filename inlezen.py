data_set_nieuwsoutlets = [['nu.nl', 'https://www.nu.nl/', 'Centraal'], 
['Nos', 'https://nos.nl/', 'Centraal'], 
['Telegraaf', 'https://www.telegraaf.nl/', 'Rechts'],
['Volkskrant', 'https://www.volkskrant.nl/', 'Links'],
['AD', 'https://www.ad.nl/', 'Centraal'],
['Trouw', 'https://www.trouw.nl/', 'Links'],
['Parool', 'https://www.parool.nl/', 'Links'],
['NRC', 'https://www.nrc.nl/', 'Rechts'],
['RTL Nieuws', 'https://www.rtl.nl/', 'Centraal'],
['Eenvandaag', 'https://eenvandaag.avrotros.nl/', 'Centraal'],
['BNR', 'https://www.bnr.nl/', 'Rechts'],
['metronieuws', 'https://www.metronieuws.nl/', 'Centraal'],
['Nederlands Dagblad', 'https://www.nd.nl/', 'Rechts']]



rss_feeds = ['https://www.nu.nl/rss', 
             'https://www.volkskrant.nl/voorpagina/rss.xml',
             'https://www.parool.nl/voorpagina/rss.xml', 
             'https://www.ad.nl/home/rss.xml', 
             'https://www.bnr.nl/?widget=rssfeed']

articles = []

import feedparser
for feed_url in rss_feeds:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:5]:

        data = {
            "title": entry.title,
            "source": feed.feed.title,
            "date": entry.get("published", ""),
            "text": entry.get("summary", ""),
            "url": entry.link
        }

        articles.append(data)

print(articles)