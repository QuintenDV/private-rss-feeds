# Private RSS Feeds

> This project contains python code to generate xml files for private podcast feeds.

I am a huge fan of <a href="https://www.dancarlin.com/" target="_blank">Dan Carlin</a>'s <a href="https://www.dancarlin.com/hardcore-history-series/" target="_blank">Hardcore History</a> podcast. Up until a few months ago, I've been listening to the podcast through the public RSS feed. This only provides access to the most recent episodes (which are free). The older episodes can be bought on Dan's <a href="https://www.dancarlin.com/hardcore-history-series/" target="_blank">website</a> as mp3 files. The podcast app that I'm using does not work well with manually downloaded mp3 files so I decided to host a private RSS feed on my home network.

A quick google search brought me to a <a href="https://www.reddit.com/r/dancarlin/comments/3s2kgb/show_rdancarlin_get_a_podcast_feed_with_all_the/">reddit post</a> of another Hardcore History fan who had the same problem and had already created a solution for it. That post linked to a <a href="https://github.com/avar/private-dan-carlin-hardcore-history-podcast-feed">repository</a> that contains a perl script and a list of episodes with a limited amount of metadata. I forked that repo, converted the code to python and made it a bit more reusable.

[![Badges](https://www.dancarlin.com/wp-content/uploads/2014/07/HH-current-239x239.jpg)](https://www.dancarlin.com/hardcore-history-series/)

## Requirements
* Python3
* The requirements listed in `requirements.txt`
* The mp3 files for the podcast you want to host

## Usage

The metadata for the show in general can be found in `resources/podcasts/hardcore-history/metadata.json`.
The metadata for each episode can be found in `resources/podcasts/hardcore-history/episode-list.json`.

Each episode has 4 attributes, as shown in the example below.
```json
[{
    "pub-date": "26/07/2006",
    "episode": "01",
    "title": "Alexander versus Hitler",
    "description": "Dan compares the way the modern world sees Adolf Hitler with the way history views Alexander the Great and wonders if the two men weren’t more alike than different."
}, ... ]
```
In order to run the script you will need to put the audio files in the correct location with the correct filenames. The `src/podcasts.py` file contains the location of the resource files for each podcast. (Currently there is only one podcast: Hardcore History)

The filenames of the audio files are based on the metadata given in the `episode-list.json` file:
`{{episode}}-{{title}}` where each space in the title is replaced by an underscore in the filename. E.g.
```01-Alexander_versus_Hitler.mp3```

To generate the xml, run the following command:

```bash
python src/generate-feed.py
	--show_name HARDCORE_HISTORY
    --root_url http://podcast.example.com
```

The output of this command can be found in `example/HARDCORE_HISTORY_feed.xml`.