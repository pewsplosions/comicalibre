from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__license__ = "GPL v3"
__copyright__ = "2019, Michael Merrill <pewsplosions@gmail.com>"
__docformat__ = "restructuredtext en"


class ComicalibreUtilityWork():
  """ Various utility operations and option switching. """

  def __init__(self):
    pass

  def get_volume(self, md, process_type):
    if process_type == 0:
      return self.volume_from_title(md)
    elif process_type == 1:
      if (md.series is not None and md.series.isnumeric()):
        return md.series
      return -1
    elif process_type == 2:
      if (md.get("#comicvinevolumeid") > 0):
        return md.get("#comicvinevolumeid")
      return -1

  def get_issue(self, md, process_type):
    if process_type == 0:
      return self.issue_from_title(md)
    elif process_type == 1:
      if (md.series_index is not None):
        return int(md.series_index)
      return -1
    elif process_type == 2:
      if (md.get("#comicvineissueid") > 0):
        return md.get("#comicvineissueid")
      return -1

  def volume_from_title(self, md):
    """ Strip title string down to volume ID. """
    if (md.title.find("---") < 0):
      return -1
    split_title = md.title.split("---")[1]
    if (split_title.find("v") < 0):
      return -1
    start_index = split_title.index("v") + 1
    if (split_title.find(" ") < 0):
      return -1
    end_index = split_title.index(" ", start_index)
    volume_id = split_title[start_index:end_index]
    return volume_id.strip()

  def issue_from_title(self, md):
    """ Strip title string down to issue number. """
    if (md.title.find("---") < 0):
      return -1
    split_title = md.title.split("---")[1]
    if (split_title.find("n") < 0):
      return -1
    start_index = split_title.index("n") + 1
    issue = split_title[start_index:]
    return issue.strip()
