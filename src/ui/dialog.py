from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from calibre_plugins.comicalibre.ui.config import prefs
from calibre_plugins.comicalibre.work.main import ComicalibreWork
from PyQt5.Qt import (QDialog, QHBoxLayout, QLabel, QLineEdit, QProgressBar,
                      QPushButton, QVBoxLayout)

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class ComicalibreDialog(QDialog):
  """ The main dialog for users to enter options before starting. """

  def __init__(self, gui, icon, do_user_config):
    """ Initialize the gui dialog. """
    QDialog.__init__(self, gui)
    self.gui = gui
    self.icon = icon
    self.do_user_config = do_user_config
    self.db = gui.current_db
    self.create_gui()

  def start_process(self):
    """ Starts the processing worker and progress bar. """
    prefs["comic_vine_api_key"] = self.api_msg.text()
    prefs["tags_to_add"] = self.tags_msg.text()
    self.worker = ComicalibreWork(self.gui)
    self.worker.process(self.progress_bar)
    # TODO Disable start button

  def create_gui(self):
    """ Layout arrangement for the dialog and its input widgets. """
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

    # Create a start button to kick off the processing.
    self.start_button = QPushButton("Start", self)
    self.start_button.clicked.connect(self.start_process)
    self.layout.addWidget(self.start_button)

    # Create progress bar.
    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setMinimumWidth(485)
    self.layout.addWidget(self.progress_bar)

    self.setWindowTitle("Comicalibre")
    self.setWindowIcon(self.icon)
    self.resize(self.sizeHint())
