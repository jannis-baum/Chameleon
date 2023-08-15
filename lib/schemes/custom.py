from lib.data import Scheme
from lib.schemes.all import format_colordefs

def custom_out(custom_config: dict, scheme: Scheme):
    return format_colordefs(custom_config['content'], scheme)
