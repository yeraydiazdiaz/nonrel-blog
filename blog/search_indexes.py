import search
from search.core import porter_stemmer
from blog.models import Post

search.register( Post, ('title', 'text', ), indexer=porter_stemmer)