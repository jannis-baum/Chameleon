from voluptuous.schema_builder import Required, Schema

color_schema = { Required('dark'): str, Required('light'): str }

config_schema = Schema({
    Required('kitty'): {
        Required('destinations'): color_schema,
        'header': str
    },

    Required('vim'): {
        Required('destination'): str,
        'header': str,
        Required('colors'): [{
            Required('groups'): [str],
            'deco': str,
            'fg': color_schema,
            'bg': color_schema,
            'ul': color_schema
        }]
    },

    'text-mate': {
        Required('destination'): str,
        Required('author'): str,
        Required('name'): str,
        'global': {
            'fg': str,
            'bg': str,
            'caret': str,
            'invisibles': str,
            'line-hl': str,
            'selection': str
        },
        'groups': [{
            Required('scopes'): [str],
            Required('vim'): str
        }]
    }
})
