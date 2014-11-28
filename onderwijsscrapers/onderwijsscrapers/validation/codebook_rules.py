from colander import MappingSchema
from onderwijsscrapers.codebooks import Codebook
import os
import csv

class CodebookSchema(MappingSchema):
    """
    A Codebook Schema needs a 'books' dict with books & names,
    and an 'id_fields' stack for nesting
    """
    def __init__(self, *args, **kwargs):
        for name, book in books.items():
            book = os.path.normpath(os.path.join(os.path.dirname(
                os.path.abspath(__file__)),
                '../codebooks/'+book
            ))
            field_dicts = list(csv.DictReader(open(book), delimiter=';'))
            codebook = Codebook(name, field_dicts, {})
            codebook.add_to_validation(self)
        
        MappingSchema.__init__(self, *args, **kwargs)