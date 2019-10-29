from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class ComicalibreUtilityWork():
  """ Various utility operations and option switching. """

  def __init__(self):
    pass

  def get_volume(self, md):
    return volume_from_title(md)

  def get_issue(self, md):
    return issue_from_title(md)

  def volume_from_title(self, md):
    """ Strip title string down to volume ID. """
    if (md.title.find("---") < 0): return -1
    split_title = md.title.split("---")[1]
    if (split_title.find("v") < 0): return -1
    start_index = split_title.index("v") + 1
    if (split_title.find(" ") < 0): return -1
    end_index = split_title.index(" ", start_index)
    volume_id = split_title[start_index:end_index]
    return volume_id

  def issue_from_title(self, md):
    """ Strip title string down to issue number. """
    if (md.title.find("---") < 0): return -1
    split_title = md.title.split("---")[1]
    if (split_title.find("n") < 0): return -1
    start_index = split_title.index("n") + 1
    issue = split_title[start_index:]
    return issue.lstrip("0")
