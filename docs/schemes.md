# How write your definition file

The file that defines all your color schemes is written in [`yaml`
syntax](https://yaml.org). Here are some ways you can learn about how to write
your scheme definition:

- Check below for an explanation of the scheme definition
- See @jannis-baum's color scheme
  [`jellyfish`](https://github.com/jannis-baum/dotfiles/blob/d994b4affa0b70e735b5d1239b3704ba04e46b32/lib/color-schemes/jellyfish.yaml)
  as an example
- Check the (easily readable) [color scheme validation code](../lib/config.py)
- Just try it out! Your definition is validated and you will get helpful error
  messages in case there's any problem

## Reused types

- `TrueColor`: A string starting in a `#` followed by 1, 2, 3, or 6
  hexadecimal characters:
  - 1 character `#x` will resolve to the gray-scale color `#xxxxxx`
  - 2 characters `#xy` will resolve to the gray-scale color `#xyxyxy`
  - 3 characters `#xyz` will resolve to the color `#xxyyzz`
  - 6 characters are left as they are
- `ColorDefinition`:
  - A dictionary with `dark: true-color, light: true-color` **OR**
  - the given name of another `ColorDefinition` which will result in that color
    **OR**
  - the name of a `highlight-definition` item, e.g. `myHighlight.fg` (see below)
- `HighlightDefinition`: A dictionary with
  - `set: String | [String]` which defines the target(s), e.g. Vim Highlight
    Groups or whatever name you want to give your `HighlightDefinition`
    **AND**
    - `from: String` a reference to another `HighlightDefinition` you want to
      reuse (i.e. one of the values you used in `set` there) **OR**
    - any combination of the keys `fg`, `bg`, `ul` with a `ColorDefinition` as a
      value and the key `deco` with a `String` as a value, e.g. `bold`

## Schema

- optional: `colors:`, which is a dictionary with names you want to give a
  color as keys and `ColorDefinition`s as values
- optional: `highlights:`, which is an array of `HighlightDefinition`s that you
  can reuse later
- required `kitty:`
  ```yaml
  kitty:
    destinations: # required
      dark: String # where to save the dark color theme
      light: String # where to save the light color theme
    header: String # optional
  ```
  - The header will be added to the top of both of your color schemes, which is
    useful to customize things like your kitty background color
  - In the header, you can use
    - `{{ ColorDefinition }}` which will be replaced by the dark/light version
      of the color for the themes, e.g.  `myVimHighlight.fg` or `myColor`
    - `TrueColor|||TrueColor` where the first color will be used in the dark and
      the second in the light mode version
- required `vim:`
  ```yaml
  vim:
    destination: String # required, where to save your color scheme
    header: String # optional
    highlight: array of HighlightDefinition # required
  ```
  - any `HighlightDefinition`s you create here can also be referenced by the Vim
    Highlight group(s) that you `set`
- optional `custom:` (an array)
  ```yaml
  custom:
    - destination: String # required, where to save your custom scheme
      content: String # required
  ```
  - in `content`, `{{ ColorDefinition }}` will be populated with referenced
    256-color, e.g.  `myVimHighlight.fg` or `myColor`
- optional `text-mate:`
  ```yaml
  text-mate: {
    destination: String, # required, where to save your color scheme
    author: str, # required, probably your name
    name: str, # required, name of your color scheme
    global: # optional, same as in TextMate scheme definition
        foreground: str,
        background: str,
        caret: str,
        invisibles: str,
        lineHighlight: str,
        selection: str
    highlight: array of HighlightDefinition # optional, same as in Vim above
  ```
