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

    for entry in feed.entries[:50]:  #aantal artikels die hij pakt per nieuws outlet

        data = {
            "title": entry.title,
            "source": feed.feed.title,
            "date": entry.get("published", ""),
            "text": entry.get("summary", ""),
            "url": entry.link
        }

        articles.append(data)

texts = [
article["title"] + " " + article["text"]
for article in articles
]

from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(texts)

from sklearn.cluster import DBSCAN
clustering = DBSCAN(
    eps=0.25,        # gevoeligheid van clusters
    min_samples=2,
    metric="cosine"
).fit(embeddings)
labels = clustering.labels_

clusters = {}

for label, article in zip(labels, articles):

    if label == -1:
        continue

    clusters.setdefault(label, []).append(article)

for cluster_id, items in clusters.items():

    print("\nSTORY", cluster_id)

    for a in items:
        print("-", a["source"], ":", a["title"])


