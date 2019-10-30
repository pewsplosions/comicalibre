from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

from calibre.customize import InterfaceActionBase

__license__   = "GPL v3"
__copyright__ = "2019, Michael Merrill <michael@merrill.tk>"
__docformat__ = "restructuredtext en"

class Comicalibre(InterfaceActionBase):
  """ Base Comicalibre plugin class. Entry point for everything. """

  name                    = "Comicalibre"
  description             = "Gather Comic Vine metadata for comic books."
  supported_platforms     = ["windows", "osx", "linux"]
  author                  = "Michael Merrill"
  version                 = (2019, 10, 2) # Year, Month, Build within month
  minimum_calibre_version = (0, 7, 53)
  actual_plugin = "calibre_plugins.comicalibre.ui.main:ComicalibreInterface"

  def is_customizable(self):
    """ Will require user input for CV API key and other options. """
    return True

  def config_widget(self):
    """ Standard config dialog to gather user input. """
    from calibre_plugins.comicalibre.ui.config import ConfigWidget
    return ConfigWidget()

  def save_settings(self, config_widget):
    """ Standard config dialog save settings function. """
    config_widget.save_settings()
    ac = self.actual_plugin_
    if ac is not None:
      ac.apply_settings()
