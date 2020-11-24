from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import os

from calibre_plugins.comicalibre.ui.config import prefs
from calibre_plugins.comicalibre.work.main import ComicalibreWork
from PyQt5.Qt import (QCheckBox, QDialog, QFrame, QGroupBox, QHBoxLayout,
                      QLabel, QLineEdit, QProgressBar, QPushButton,
                      QScrollArea, QVBoxLayout)

__license__ = "GPL v3"
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

  def start_process(self, process_type):
    """ Starts the processing worker and progress bar. """
    prefs["comic_vine_api_key"] = self.api_msg.text()
    prefs["tags_to_add"] = self.tags_msg.text()
    self.worker = ComicalibreWork(self.gui)
    self.result_text.setText("Processing...")
    self.title_start.setEnabled(False)
    self.series_start.setEnabled(False)
    self.ids_start.setEnabled(False)
    keep_tags = self.keep_tags_cb.isChecked()
    errors = self.worker.process(self.progress_bar, process_type, keep_tags)
    self.title_start.setEnabled(True)
    self.series_start.setEnabled(True)
    self.ids_start.setEnabled(True)
    results = "Finished!" + os.linesep
    for error in errors:
      results = results + error + os.linesep
    self.result_text.setText(results)

  def title_process(self):
    self.start_process(0)

  def series_process(self):
    self.start_process(1)

  def ids_process(self):
    self.start_process(2)

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

    self.api_label = QLabel("Comic Vine API Key")
    self.api_label.setBuddy(self.api_msg)

    self.api_layout.addWidget(self.api_label)
    self.api_layout.addWidget(self.api_msg)

    # Create an editable box for user to input Tags to add to all books.
    self.tags_layout = QHBoxLayout()
    self.tags_msg = QLineEdit(self)
    self.tags_msg.setText(prefs["tags_to_add"])

    self.tags_label = QLabel("Tags To Add")
    self.tags_label.setBuddy(self.tags_msg)

    self.tags_layout.addWidget(self.tags_label)
    self.tags_layout.addWidget(self.tags_msg)

    # Add the fields to the main layout.
    self.layout.addLayout(self.api_layout)
    self.layout.addLayout(self.tags_layout)

    # Option to keep current tags.
    self.keep_tags_cb = QCheckBox("Keep existing tags while adding new.", self)
    self.layout.addWidget(self.keep_tags_cb)

    # Separate the buttons from the input.
    self.btn_sep = QFrame()
    self.btn_sep.setFrameShape(QFrame.HLine)
    self.btn_sep.setFrameShadow(QFrame.Sunken)
    self.layout.addWidget(self.btn_sep)

    # Create a start button to kick off the processing with title.
    self.title_start = QPushButton("Using Title - Hover For Details", self)
    self.title_start.setToolTip("This expects the title of a book to have a "
                                "specific formatted string containing volume "
                                "ID and issue#. e.g." + os.linesep + "Desired "
                                "Title --- v1234 n0124" + os.linesep + "Where "
                                "--- is required and the number after v "
                                "matches Comic Vine's volume ID. The number "
                                "after n is the issue number.")
    self.title_start.clicked.connect(self.title_process)
    self.layout.addWidget(self.title_start)

    # Create a start button to kick off the processing with series.
    self.series_start = QPushButton("Using Series - Hover For Details", self)
    self.series_start.setToolTip("This expects the series name to match the "
                                 "Comic Vine volume ID and the series number "
                                 "equals issue number.")
    self.series_start.clicked.connect(self.series_process)
    self.layout.addWidget(self.series_start)

    # Create a start button to kick off the processing with CV IDs.
    self.ids_start = QPushButton("Using IDs - Hover For Details", self)
    self.ids_start.setToolTip("This expects two custom columns with lookup "
                              "comicvineissueid and comicvinevolumeid. "
                              "These must match Comic Vine's IDs for the "
                              "issue and the volume.")
    self.ids_start.clicked.connect(self.ids_process)
    self.layout.addWidget(self.ids_start)

    # Separate the progress and results.
    self.result_sep = QFrame()
    self.result_sep.setFrameShape(QFrame.HLine)
    self.result_sep.setFrameShadow(QFrame.Sunken)
    self.layout.addWidget(self.result_sep)

    # Create progress bar.
    self.progress_bar = QProgressBar()
    self.progress_bar.setRange(0, 100)
    self.progress_bar.setMinimumWidth(485)
    self.layout.addWidget(self.progress_bar)

    # Create results text area.
    self.result_box = QGroupBox()
    self.result_box.setTitle("Results")
    self.result_text = QLabel("Run Comicalibre to see results.")
    self.result_scroll = QScrollArea()
    self.result_scroll.setWidget(self.result_text)
    self.result_scroll.setWidgetResizable(True)
    self.result_layout = QVBoxLayout()
    self.result_layout.addWidget(self.result_scroll)
    self.result_box.setLayout(self.result_layout)
    self.layout.addWidget(self.result_box)

    self.setWindowTitle("Comicalibre")
    self.setWindowIcon(self.icon)
    self.resize(self.sizeHint())
