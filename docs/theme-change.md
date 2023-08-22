# How to make your terminal reflect system dark/light mode

This is dependent on both your OS as well as your terminal.

## On macOS with Kitty

Let's assume the destinations of your kitty color themes are
`~/.config/kitty/themes/my-theme-dark.conf` and `.../my-theme-light.conf`
respectively. Add the following to your `kitty.conf`:

```conf
include theme.conf
```

Now we will create a script that (1) sym-links the currently correct theme file to
`~/.config/kitty/theme.conf` and (2) reloads all running instances of kitty. For
this, place the following into a file `~/.config/kitty/sync-theme`

```zsh
#!/bin/zsh

kitty_dir="${0:a:h}"
theme="$kitty_dir/theme.conf"

[[ "$(defaults read -g AppleInterfaceStyle 2>/dev/null)" = "Dark" ]] \
    && target="$kitty_dir/themes/my-theme-dark.conf" \
    || target="$kitty_dir/themes/my-theme-light.conf"

rm -rf "$theme"
ln -s "$target" "$theme"

for pid in "$(ps -x | grep '/Applications/kitty.app/Contents/MacOS/kitty' | grep -v grep | awk '{ print $1 }')"; do
    kill -SIGUSR1 $pid
done
```

and make this file executable by running `chmod +x ~/.config/kitty/sync-theme`.
With this set up, you can already manually refresh kitty to the correct theme by
executing the script.

To make this happen automatically whenever the macOS theme changes, we have to
listen to the [Distributed
Notification](https://developer.apple.com/documentation/foundation/distributednotificationcenter)
`AppleInterfaceThemeChangedNotification` and call our script whenever this
notification is fired. There are lots of ways of doing this! One way is using
[Hammerspoon](http://www.hammerspoon.org), which might be convenient if you
(like me) are already using it anyways. To set up the listener with Hammerspoon,
add the following to your `~/.hammerspoon/init.lua`:

```lua
themeWatcher = hs.distributednotifications.new(function(name, object, userInfo)
    os.execute(os.getenv('HOME') .. '/.config/kitty/sync-theme')
end, dn)
themeWatcher:start()
```

That's it! Now kitty will automatically switch between dark and light mode
whenever macOS switches.
