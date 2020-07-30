import os
import argparse
from podcasts import Podcast
from show import Show
from mutagen.mp3 import MP3

"""
Create an rss feed xml for a podcast
"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate the xml for a private podcast feed')
    parser.add_argument('--show_name',
                        help=f'The name of the podcast.',
                        choices=[p.name for p in Podcast],
                        required=True)
    parser.add_argument('--root_url',
                        help=f"The url that will be used to access the podcast feed. This is where the feed.xml file and the resources directory will be located. E.g. 'podcast.mydomain.com'",
                        required=True)

    args = parser.parse_args()
    # Convert input parameter to Podcasts Enum
    show_name = Podcast[ args.show_name ]
    root_url = args.root_url

    # Generate the xml for this podcast
    show = Show(show_name, root_url)
    show_xml = show.generate_complete_show_xml()

    # Load the general podcast template and fill in the show_xml
    with open('resources/outer-podcast-template.xml') as ins:
        podcast_template = ins.read()
    complete_xml = podcast_template % {'content': show_xml}

    # Write result to file
    output_file = f'target/{args.show_name}_feed.xml'
    os.makedirs('target', exist_ok=True)
    with open(output_file, 'w') as ostr:
        ostr.write(complete_xml)
