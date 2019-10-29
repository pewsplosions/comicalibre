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
  bad_format = []

  def __init__(self, gui):
    self.calibre_worker = ComicalibreCalibreWork(gui)
    self.vine_worker = ComicalibreVineWork()
    self.prog_worker = ComicalibreProgressWork()
    self.util_worker = ComicalibreUtilityWork()

  def process(self, progress_bar):
    self.bad_format = []
    progress_bar.setValue(0)
    self.prog_worker.progress_bar = progress_bar

    # Get selected books.
    books = self.calibre_worker.get_selected_books()
    self.prog_worker.calculate_steps(books)

    # Loop through to get all current metadata.
    for book in books:
      md = self.calibre_worker.get_current_metadata(book)

      volume_id = self.util_worker.get_volume(md)
      if (volume_id == -1):
        self.bad_format.append(md)
        self.prog_worker.iterate()
        continue

      issue = self.util_worker.get_issue(md)
      if (issue == -1):
        self.bad_format.append(md)
        self.prog_worker.iterate()
        continue

      # Fill metadata from Comic Vine.
      self.vine_worker.get_metadata(md, volume_id, issue)

      # Add infromation that is part of the title or preferences.
      new_title = md.title.split("---")[0].strip().title()
      md.set("title", new_title)
      md.set("series_index", issue)
      md.set("languages", ["English"])
      md.set("title_sort", None) # Calibre will figure this out.
      md.set("authors_sort", None) # Calibre will figure this out.
      md.set("author_link_map", None) # Calibre will figure this out.
      md.set("#physicalcopy", False)

      new_tags = prefs["tags_to_add"].split(",")
      for tag in new_tags:
        tag = tag.strip().title()
      md.set("tags", new_tags)

      self.calibre_worker.save_metadata(book, md)
      self.prog_worker.iterate()
