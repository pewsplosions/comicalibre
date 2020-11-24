from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from calibre.gui2.actions import InterfaceAction
from calibre_plugins.comicalibre.ui.dialog import ComicalibreDialog

__license__ = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"


class ComicalibreInterface(InterfaceAction):
  """ Basic interface of the plugin. Initiates values and starts dialog. """

  name = "Comicalibre"
  action_spec = ("Comicalibre", None, "Run Comicalibre...", "Ctrl+Shift+F9")

  def genesis(self):
    """ Initiate plugin. Occurs only once on startup. """
    icon = get_icons("images/icon.png")
    self.qaction.setIcon(icon)
    self.qaction.triggered.connect(self.show_dialog)

  def show_dialog(self):
    """ When the user first interacts with the plugin. Occurs on click. """
    base_plugin_object = self.interface_action_base_plugin
    do_user_config = base_plugin_object.do_user_config
    dialog = ComicalibreDialog(self.gui, self.qaction.icon(), do_user_config)
    dialog.show()

  def apply_settings(self):
    """ Occurs if config is changed. """
    from calibre_plugins.comicalibre.ui.config import prefs
    prefs  # Nothing to do with this yet. Leaving here as reminder.
