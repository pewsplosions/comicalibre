from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from calibre.utils.config import JSONConfig
from PyQt5.Qt import QHBoxLayout, QLabel, QLineEdit, QVBoxLayout, QWidget

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

prefs = JSONConfig("plugins/comicalibre")
prefs.defaults["comic_vine_api_key"] = ""
prefs.defaults["tags_to_add"] = ""

class ConfigWidget(QWidget):
  """ GUI for configuration of default user input values. """

  def __init__(self):
    """ Initialize the GUI elements for the config dialog. """
    QWidget.__init__(self)

    self.layout = QVBoxLayout()
    self.layout.setSpacing(20)
    self.setLayout(self.layout)

    # Create an editable box for user to input Comic Vine API Key.
    self.api_layout = QHBoxLayout()
    self.api_msg = QLineEdit(self)
    self.api_msg.setFixedWidth(350)
    self.api_msg.setText(prefs["comic_vine_api_key"])

    self.api_label = QLabel("Comic Vine API Key:")
    self.api_label.setBuddy(self.api_msg)

    self.api_layout.addWidget(self.api_label)
    self.api_layout.addWidget(self.api_msg)

    # Create an editable box for user to input Tags to add to all books.
    self.tags_layout = QHBoxLayout()
    self.tags_msg = QLineEdit(self)
    self.tags_msg.setText(prefs["tags_to_add"])

    self.tags_label = QLabel("Tags To Add:")
    self.tags_label.setBuddy(self.tags_msg)

    self.tags_layout.addWidget(self.tags_label)
    self.tags_layout.addWidget(self.tags_msg)

    # Add the fields to the main layout.
    self.layout.addLayout(self.api_layout)
    self.layout.addLayout(self.tags_layout)

  def save_settings(self):
    """ Save user input to the default configuration. """
    prefs["comic_vine_api_key"] = self.api_msg.text()
    prefs["tags_to_add"] = self.tags_msg.text()
