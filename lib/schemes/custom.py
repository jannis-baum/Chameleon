from lib.data import Scheme
from lib.schemes.all import format_colordefs, save_to

def gen_custom(config: dict, scheme: Scheme):
    content = format_colordefs(config['content'], scheme)
    save_to(config['destination'], content)
