"""

    search_indexes.py
    
    Setup required indexes to allow the search module to perform searches on the Post model.

"""

import search
from search.core import porter_stemmer
from blog.models import Post

# Create indexes on title and text fields.
search.register( Post, ('title', 'text', ), indexer=porter_stemmer)