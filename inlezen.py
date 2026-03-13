outlet_bias = {
    "NU": "Centraal",
    "Nos": "Centraal",
    "De Telegraaf": "Rechts",
    "Volkskrant": "Links",
    "AD:home": "Centraal",
    "Trouw": "Links",
    "Parool: Voorpagina": "Links",
    "Nieuws, achtergronden en onderzoeksjournalistiek - NRC": "Rechts",
    "RTL Nieuws": "Centraal",
    "Eenvandaag": "Centraal",
    "bnr - Home": "Rechts",
    "metronieuws": "Centraal",
    "Nederlands Dagblad": "Rechts"
}

rss_feeds = ['https://www.nu.nl/rss', 
             'https://www.volkskrant.nl/voorpagina/rss.xml',
             'https://www.parool.nl/voorpagina/rss.xml', 
             'https://www.ad.nl/home/rss.xml', 
             'https://www.bnr.nl/?widget=rssfeed',
             'https://www.telegraaf.nl/rss/',
             'https://feeds.feedburner.com/nrc/FmXV']

from transformers import pipeline

summarizer = pipeline(
    "text-generation",
    model="google/flan-t5-large"
)

articles = []

import feedparser
for feed_url in rss_feeds:

    feed = feedparser.parse(feed_url)

    for entry in feed.entries[:100]:  #aantal artikels die hij pakt per nieuws outlet

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

    links = 0
    rechts = 0
    centraal = 0

    print("\nSTORY", cluster_id)

    for a in items:

        source = a["source"]
        print("-", source, ":", a["title"])

        bias = outlet_bias.get(source)

        if bias == "Links":
            links += 1
        elif bias == "Rechts":
            rechts += 1
        elif bias == "Centraal":
            centraal += 1
    Aantal_artikelen = links + rechts + centraal
    Percentage_links = (links / Aantal_artikelen) * 100
    Percentage_rechts = (rechts / Aantal_artikelen) * 100  
    percentage_centraal = (centraal / Aantal_artikelen) * 100

    print("Links:", links, "| Centraal:", centraal, "| Rechts:", rechts)
    print("Percentage Links:", round(Percentage_links, 2), "% | Percentage Centraal:", round(percentage_centraal, 2), "% | Percentage Rechts:", round(Percentage_rechts, 2), "%")
    story_text = ""

    for a in items:
        story_text += a["title"] + ". " + a["text"] + "\n"
    
    prompt = "summarize the following news articles neutrally dont repeat yourself:\n" + story_text

    summary = summarizer(
    prompt,
    max_new_tokens=80,
    do_sample=False
    )
 
    print("\nSamenvatting:")
    print(summary[0]["generated_text"].replace("summarize the following news articles neutrally dont repeat yourself:\n", "").strip())

