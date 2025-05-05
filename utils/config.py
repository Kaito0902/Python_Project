
import configparser
import os

config = configparser.ConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

DB_CONFIG   = config['database']
MODEL_PATH  = config['model']['model_path']
THRESHOLDS  = {
    'Gioi':        float(config['grading']['threshold_gioi']),
    'Kha':         float(config['grading']['threshold_kha']),
    'Trung binh':  float(config['grading']['threshold_trung_binh']),
}
