"""

    indexes.py
    
    Runs autodiscover from django-autoload for dbindexer and search modules.

"""

from dbindexer import autodiscover
autodiscover()

# search for "search_indexes.py" in all installed apps
import search
search.autodiscover()