from voluptuous.schema_builder import Required, Schema

config_schema = Schema({
    Required('kitty'): {
        Required('destinations'): {
            Required('dark'): str,
            Required('light'): str
        },
        'header': str
    },

    Required('vim'): {
        Required('destination'): str,
        'header': str,
        Required('colors'): [{
            Required('groups'): [str],
            Required('dark'): str,
            Required('light'): str
        }]
    },
})
