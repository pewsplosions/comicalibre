from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from threading import Thread

from calibre_plugins.comicalibre.ui.config import prefs
from calibre_plugins.comicalibre.work.calibre import ComicalibreCalibreWork
from calibre_plugins.comicalibre.work.comicvine import ComicalibreVineWork
from calibre_plugins.comicalibre.work.progress import ComicalibreProgressWork
from calibre_plugins.comicalibre.work.utility import ComicalibreUtilityWork

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class ComicalibreWork(Thread): # TODO Should this be a Thread?
  """ Control the order of processing for the work being done. """
  errors = []

  def __init__(self, gui):
    self.calibre_worker = ComicalibreCalibreWork(gui)
    self.vine_worker = ComicalibreVineWork()
    self.prog_worker = ComicalibreProgressWork()
    self.util_worker = ComicalibreUtilityWork()

  def process(self, progress_bar, process_type, keep_tags):
    self.errors = []
    progress_bar.setValue(0)
    self.prog_worker.progress_bar = progress_bar

    # Get selected books.
    books = self.calibre_worker.get_selected_books()
    self.prog_worker.calculate_steps(books)

    # Loop through to get all current metadata.
    for book in books:
      md = self.calibre_worker.get_current_metadata(book)
      id_for_errors = ""
      if (md.series_index is not None):
        id_for_errors = " " + str(md.series_index)

      volume_id = self.util_worker.get_volume(md, process_type)
      if (self.volume_id_has_errors(md, volume_id, id_for_errors)): continue

      issue = self.util_worker.get_issue(md, process_type)
      if (self.issue_number_has_errors(md, issue, id_for_errors)): continue

      # Fill metadata from Comic Vine.
      try:
        self.vine_worker.get_metadata(md, volume_id, issue, process_type == 2)
      except:
        self.errors.append(md.title + id_for_errors +
          ": Unable to get info from Comic Vine with given IDs.")

      self.set_given_metadata(md, keep_tags)

      try:
        self.calibre_worker.save_metadata(book, md)
      except:
        self.errors.append(md.title + id_for_errors +
          ": Received data from Comic Vine that was unable to be saved.")

      self.prog_worker.iterate()

    return self.errors

  def volume_id_has_errors(self, md, volume_id, id_for_errors):
    if (volume_id == -1):
      self.errors.append(md.title + id_for_errors +
        ": Was unable to determine volume ID from the given input.")
      self.prog_worker.iterate()
      return True
    return False

  def issue_number_has_errors(self, md, issue, id_for_errors):
    if (issue == -1):
      self.errors.append(md.title + id_for_errors +
        ": Was unable to determine issue number from the given input.")
      self.prog_worker.iterate()
      return True
    return False

  def set_given_metadata(self, md, keep_tags):
    """ Add infromation that is part of the title or preferences. """
    new_title = md.title.split("---")[0].strip().title()
    md.set("title", new_title)
    md.set("languages", ["English"])
    md.set("title_sort", None) # Calibre will figure this out.
    md.set("authors_sort", None) # Calibre will figure this out.
    md.set("author_link_map", None) # Calibre will figure this out.
    if (md.get("#physicalcopy") is None):
      md.set("#physicalcopy", False)
    new_tags = prefs["tags_to_add"].split(",")
    for tag in new_tags:
      tag = tag.strip().title()
    if (keep_tags):
      for tag in md.tags:
        if (tag not in new_tags):
          new_tags.append(tag)
    if (new_tags is not None and len(new_tags) > 0):
      md.set("tags", new_tags)
