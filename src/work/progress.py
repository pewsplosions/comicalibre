from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class ComicalibreProgressWork():
  """ Control the interaction and calculations for the progress bar. """

  def __init__(self):
    self.progress_bar = None
    self.steps_taken = 0

  def calculate_steps(self, books):
    total_books = len(books)
    self.total_steps = total_books

  def iterate(self):
    self.steps_taken = self.steps_taken + 1
    current_progress = self.steps_taken / self.total_steps * 100
    self.progress_bar.setValue(current_progress)
