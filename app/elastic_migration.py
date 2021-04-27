from elasticsearch import Elasticsearch
from app.core.settings import settings

es = Elasticsearch([settings.ELASTICSEARCH_URL])

response = es.search(index="books")["hits"]["hits"]
for i in response:
    print(i["_source"])

index_settings = {
    "settings": {
        "analysis": {
            "filter": {
                "autocomplete_filter": {"type": "ngram", "min_gram": 1, "max_gram": 10}
            },
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "autocomplete_filter"],
                }
            },
        },
        "index.max_ngram_diff": 10,
    },
    "mappings": {
        "properties": {
            "author": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "standard",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
            "id": {"type": "long"},
            "name": {
                "type": "text",
                "analyzer": "autocomplete",
                "search_analyzer": "standard",
                "fields": {"keyword": {"type": "keyword", "ignore_above": 256}},
            },
        }
    },
}

es.indices.delete("books")
es.indices.create("books", body=index_settings)

for book in response:
    es.index(index="books", body=book["_source"])
