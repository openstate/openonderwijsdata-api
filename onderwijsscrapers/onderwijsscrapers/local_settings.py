import exporters
from settings import EXPORT_SETTINGS
from datetime import date

EXPORT_METHODS = { 
    # 'file': {
    #     'exporter': exporters.FileExporter,
    #     'options': {
    #         'export_dir': EXPORT_DIR,
    #         'create_tar': True,
    #         'remove_json': False
    #     }
    # },
    'elasticsearch': {
        'exporter': exporters.ElasticSearchExporter,
        'options': {
            'url': '127.0.0.1:9200',
            'index_suffix' : '2015_08_26' #date.today().strftime('%Y_%m_%d')
        }   
    }   
}

for e in EXPORT_SETTINGS:
    EXPORT_SETTINGS[e]['geocode'] = False
