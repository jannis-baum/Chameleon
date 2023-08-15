from voluptuous import Any
from voluptuous.schema_builder import Required, Schema

color_schema = { Required('dark'): str, Required('light'): str }
hl_schema = Any(
    {
        Required('set'): Any(str, [str]),
        'fg': color_schema,
        'bg': color_schema,
        'deco': str,
        'ul': color_schema
    },
    {
        Required('set'): Any(str, [str]),
        Required('from'): str
    }
)

config_schema = Schema({
    Required('kitty'): {
        Required('destinations'): color_schema,
        'header': str
    },

    Required('vim'): {
        Required('destination'): str,
        'header': str,
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
