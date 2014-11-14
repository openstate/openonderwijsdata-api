from codebooks import Codebook
import csv
from itertools import islice

book = 'codebooks/roa/slgsd.csv'
source = '../../../data/roa/roa-data.csv'

if __name__ == '__main__':
    field_dicts = list(csv.DictReader(open(book), delimiter=';'))
    table_fields = Codebook(field_dicts, {})

    with open(source, 'r') as f:
        heads = f.readline().decode("utf-8-sig").encode("utf-8")\
            .strip().split(';')
        rows = islice((line.split(';') for line in f), 2)

    

    print heads