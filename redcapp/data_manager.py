try:
    import cdsapi
except:
    pass

from pathlib import Path

class ERA5_Manager(object):
    def __init__(self) -> None:
        self.name = 'reanalysis-era5-pressure-levels'
        self.variable = ['']
    
def install_CDS_API_key(url, key):
    '''install the CDS API key  in the file $HOME/.cdsapirc'''
    txt = f'url: {url}\nkey: {key}'
    file = Path('~/.cdsapirc').expanduser()
    with open(file,'w') as f:
        f.write(txt)
    print(f'The file "{file}" has been written as follows api key:')
    with open(file) as f:
        print(f'"{f.read()}"')
    
    
era5 = ERA5_Manager()
install_CDS_API_key(url='https://cds.climate.copernicus.eu/api/v2',
                     key='138752:fbf10968-3376-483a-8795-c26e8e1860d4')


c = cdsapi.Client()
c.retrieve()