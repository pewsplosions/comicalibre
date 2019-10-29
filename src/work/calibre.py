from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class ComicalibreCalibreWork():
  """ Control the interaction with calibre GUI and DB. """

  def __init__(self, gui):
    """ Initialize GUI and DB. """
    self.gui = gui
    self.db = gui.current_db.new_api

  def get_selected_books(self):
    """ Get selected books as a map of book id to row. """
    rows = self.gui.library_view.selectionModel().selectedRows()
    if not rows or len(rows) == 0:
      return error_dialog(self.gui, _L['Cannot update metadata'],
                            _L['No books selected'], show=True)
    return map(self.gui.library_view.model().id, rows)

  def get_current_metadata(self, book):
    """ Get the metadata object of a book from the current database. """
    return self.db.get_metadata(book)

  def save_metadata(self, book, md):
    """ Save metadata to a book in the database. """
    self.db.set_metadata(book, md)
