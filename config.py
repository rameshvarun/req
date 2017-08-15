import yaml

from pathlib import Path

config = yaml.load(open(Path.home() / '.readq'))
DATA_FOLDER = Path(config['data_folder'])
MERCURY_API_KEY = config['mercury_api_key']
