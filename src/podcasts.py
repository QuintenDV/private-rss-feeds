from enum import Enum

# Supported podcasts are listed here

class Podcast(Enum):
    HARDCORE_HISTORY = 1

PODCAST_INFO = {
    Podcast.HARDCORE_HISTORY: {
        "resource-dir": "resources/podcasts/hardcore-history"
    }
}