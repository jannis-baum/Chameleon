# Chameleon ௹

Chameleon creates color schemes for all your terminal programs that allow you to
dynamically switch between dark and light mode - all from a single color scheme
definition file!

## How it works

You keep a single `yaml` file with lots of syntactic sugar where you define
24-bit colors for everything, each in their dark mode and light mode version.

Then, Chameleon calculates the closest matching 256-color based on the dark and
light versions you defined. This color is used for the schemes generated for all
your terminal programs, but you never have to think about this.

Finally, Chameleon generates two color schemes for your terminal: one for dark
mode and one for light mode. Here, the 256 colors are set so they reflect your
original definitions.

That's it - now you can switch your terminal color scheme, and all colors,
included the ones that are already printed, will change how you wanted them to.
This works because the 256-colors that are actually used by your programs in the
background stay at the same value, just your terminal's interpretation of them
changes.

## Supported software

If your favorite software is not yet supported, feel free to submit a pull
request!

### Terminals

Chameleon can support any terminal that lets you customize the 256 terminal
colors based on 24-bit colors. Below is a list of terminals that are already
implemented

- kitty

### Terminal programs

Chameleon can support any terminal program that lets you customize it with the
256 terminal colors. Below is a list of color shemes Chameleon can generate.

- Vim
- TextMate
- Anything else based on placeholders that Chameleon populates with the correct
  colors, e.g. for colors used in your shell

## How to use

Set up your `yaml` color scheme definition [like this](./docs/schemes.md). Then,
just run `generate <your file>` and Chameleon will automatically generate all
the color schemes and save them where you defined the destinations. That's it!

If you want your terminal to react to system dark/light mode switches, check out
[this guide](./docs/theme-change.md).
