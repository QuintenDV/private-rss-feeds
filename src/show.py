import os
import json
from datetime import datetime
from email import utils
from mutagen.mp3 import MP3
from podcasts import Podcast,PODCAST_INFO

class Show:
    def __init__(self, show_name: Podcast, root_url: str):
        assert show_name in PODCAST_INFO, f"{show_name.name} not a valid podcast"

        self.resource_dir = PODCAST_INFO[show_name]['resource-dir']
        self.root_url = root_url

        # Load the metadata
        metadata_file = os.path.join(self.resource_dir, "metadata.json")
        with open(metadata_file) as ins:
            self.metadata = json.load(ins)

        self.metadata['image'] = os.path.join(root_url, self.metadata['image'])
        self.metadata['default-episode-image'] = os.path.join(root_url, self.metadata['default-episode-image'])

    def _get_episode_list(self):
        episodes_path = os.path.join(self.resource_dir, "episode-list.json")
        with open(episodes_path) as ins:
            episodes = json.load(ins)
        return episodes

    def _get_episodes_template(self):
        episodes_template = os.path.join(self.resource_dir, "episode-template.xml")
        with open(episodes_template) as ins:
            episodes_template = ins.read()
        return episodes_template

    def _generate_episode_xml(self, episode, template):
        #  Description, summary and subtitle are the same
        episode["summary"]  = episode["description"]
        episode["subtitle"] = episode["description"]

        # link, keywords and the default image are taken from the show's metadata
        episode["link"]     = self.metadata['link']
        episode["keywords"] = self.metadata["keywords"]
        episode["default-episode-image"] = self.metadata["default-episode-image"]

        # Generate the local filepath for the mp3
        filepath = os.path.join(self.resource_dir, 'mp3s', f'{episode["episode"]}-{episode["title"].replace(" ", "_")}.mp3')
        # Get get file size and episode length from the filepath
        episode["file-size"] = os.stat(filepath).st_size
        episode["duration"]  = MP3(filepath).info.length

        # Create the url to the mp3 file
        episode["file_path"] = os.path.join(self.root_url, filepath)

        # Check if a pubDate is specified in the episde metadata
        if 'pub-date' in episode:
            pub_date = datetime.strptime(episode["pub-date"], '%d/%m/%Y')
            episode["pub-date"] = utils.format_datetime(pub_date)
        # Otherwise use the pubDate from the show's metadata
        else:
            episode["pub-date"] = self.metadata['pub-date']

        # Generate a title for the episode
        episode["title"] = f'{episode["episode"]} - {episode["title"]}'

        return template % episode

    def generate_all_episodes_xml(self):
        template = self._get_episodes_template()
        episodes = self._get_episode_list()
        xml_list = [
            self._generate_episode_xml(episode, template)
            for episode in episodes
            ]
        return '\n'.join(xml_list)

    def generate_metadata_xml(self):
        template_path = os.path.join(self.resource_dir, "metadata-template.xml")
        with open(template_path) as ins:
            return ins.read() % self.metadata

    def generate_complete_show_xml(self):
        meta = self.generate_metadata_xml()
        episodes = self.generate_all_episodes_xml()
        return f'{meta}\n\n{episodes}'