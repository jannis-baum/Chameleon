from voluptuous import Any
from voluptuous.schema_builder import Required, Schema

color_schema = Any(str, { Required('dark'): str, Required('light'): str })
hl_schema_def = {
    Required('set'): Any(str, [str]),
    'fg': color_schema,
    'bg': color_schema,
    'deco': str,
    'ul': color_schema
}
hl_schema = Any(hl_schema_def, {
    Required('set'): Any(str, [str]),
    Required('from'): str
})

config_schema = Schema({
    'colors': { str: color_schema },
    'highlights': [hl_schema_def],

    Required('kitty'): {
        Required('destinations'): {
            Required('dark'): str,
            Required('light'): str
        },
        'header': str
    },

    Required('vim'): {
        Required('destination'): str,
        Required('destination_nvim'): str,
        'header': str,
        'header_nvim': str,
        Required('highlight'): [hl_schema]
    },

    'text-mate': {
        Required('destination'): str,
        Required('author'): str,
        Required('name'): str,
        'global': {
            'foreground': str,
            'background': str,
            'caret': str,
            'invisibles': str,
            'lineHighlight': str,
            'selection': str
        },
        'highlight': [hl_schema]
    },

    'custom': [{
        Required('destination'): str,
        Required('content'): str
    }]
})
