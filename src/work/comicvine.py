from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import json
import urllib2

from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.comicalibre.ui.config import prefs
from dateutil.parser import parse

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class ComicalibreVineWork():
  """ Control the interaction with Comic Vine API. """

  BASE_URL = "https://comicvine.gamespot.com/api/"

  def __init__(self):
    """ Initialize data attributes for process. """
    self.api_key = prefs["comic_vine_api_key"]

  def build_url(self, resource, params):
    """ Build the url based on the base, resource and parameters. """
    url = self.BASE_URL + resource + "?api_key=" + self.api_key
    for param in params:
      url = url + "&" + param + "=" + params[param]
    return url

  def get_metadata(self, md, volume_id, issue):
    """ Main process to get metadata from Comic Vine and add to Calibre. """
    issue_id = self.get_issue_id(volume_id, issue)
    self.add_issue_data(md, issue_id)
    self.add_volume_data(md, volume_id)
    md.set("#comicvineissueid", issue_id)

  def add_volume_data(self, md, volume_id):
    """ Find and add found volume data to the metadata object. """
    params = {
      "format": "json",
      "field_list": "name,publisher,start_year"
    }
    url = self.build_url("volume/4050-" + volume_id, params)
    response = urllib2.urlopen(url)
    result = response.read()
    data = json.loads(result.decode("utf-8"))
    volume_name = data["results"]["name"]
    start_year = data["results"]["start_year"]
    publisher = data["results"]["publisher"]["name"]
    series_name = volume_name + " (" + start_year + ")"
    md.set("publisher", publisher)
    md.set("series", series_name)
    md.set("#comicvinevolumeid", volume_id)

  def add_issue_data(self, md, issue_id):
    """ Find and add found issue data to the metadata object. """
    params = {
      "format": "json",
      "field_list": "cover_date," +
                    "description," +
                    "person_credits," +
                    "character_credits," +
                    "story_arc_credits," +
                    "site_detail_url"
    }
    url = self.build_url("issue/4000-" + str(issue_id), params)
    response = urllib2.urlopen(url)
    result = response.read()
    data = json.loads(result.decode("utf-8"))
    char_data = data["results"]["character_credits"]
    characters = []
    for char in char_data:
      characters.append(char["name"])
    story_data = data["results"]["story_arc_credits"]
    stories = []
    for story in story_data:
      stories.append(story["name"])
    creator_data = data["results"]["person_credits"]
    creators = []
    authors = []
    for creator in creator_data:
      creator_role = creator["role"]
      creators.append(creator["name"])
      if (creator_role.find("writer") >= 0):
        authors.append(creator["name"])
    if (len(authors) <= 0): authors.append("Unknown")

    cvurl = data["results"]["site_detail_url"]
    cvhtml = "<p>Learn more at <a href='" + cvurl + "'>Comic Vine</a>.</p>"

    md.set("#characters", characters)
    md.set("#storyarcs", stories)
    md.set("#creators", creators)
    md.set("authors", authors)
    md.set("pubdate", parse(data["results"]["cover_date"]))
    md.set("comments", data["results"]["description"] + cvhtml)

  def get_issue_id(self, volume_id, issue):
    """ Get issue ID from Comic Vine. """
    params = {
      "format": "json",
      "limit": "1",
      "field_list": "id",
      "filter": "volume:" + volume_id + ",issue_number:" + issue.lstrip("0")
    }
    url = self.build_url("issues/", params)
    response = urllib2.urlopen(url)
    result = response.read()
    data = json.loads(result.decode("utf-8"))
    return data["results"][0]["id"]
