# Toggle Ghostty from VS Code with Ctrl+`

Ever wish you could use `Ctrl+`` to switch between VS Code and Ghostty, just like the built-in terminal toggle? Here's how to set it up in 3 steps.

## The Problem

VS Code's `Ctrl+`` toggles the integrated terminal. If you use Ghostty as your main terminal, there's no built-in way to toggle between the two apps with a single hotkey.

Ghostty has a `global:toggle_visibility` keybind, but it has a macOS bug where hiding Ghostty sends focus to Finder instead of the previous app.

## The Solution

We use **Hammerspoon** (a free macOS automation tool) to handle the hotkey. It remembers which app you came from and restores focus correctly.

### Step 1: Install Hammerspoon

```bash
brew install --cask hammerspoon
```

Open Hammerspoon, then grant it **Accessibility** permissions:
**System Settings > Privacy & Security > Accessibility** > add Hammerspoon and enable it.

### Step 2: Create the Hammerspoon script

Create `~/.hammerspoon/init.lua` with the following:

```lua
local previousApp = nil

hs.hotkey.bind({"ctrl"}, "`", function()
    local frontApp = hs.application.frontmostApplication()

    if frontApp and frontApp:name() == "Ghostty" then
        frontApp:hide()
        if previousApp and previousApp:isRunning() then
            previousApp:activate()
        end
    else
        previousApp = frontApp
        hs.application.launchOrFocus("Ghostty")
    end
end)
```

Reload the config from the Hammerspoon menu bar icon > **Reload Config**.

### Step 3: Unbind Ctrl+` in VS Code

Open your VS Code keybindings JSON (`Cmd+Shift+P` > "Preferences: Open Keyboard Shortcuts (JSON)") and add:

```json
{
  "key": "ctrl+`",
  "command": "-workbench.action.terminal.toggleTerminal"
}
```

This stops VS Code from capturing the keystroke so Hammerspoon can handle it.

## That's it!

Now from VS Code, press `Ctrl+`` to jump to Ghostty. Press it again to jump back to VS Code. Works from any app, not just VS Code.

### Requirements
- [Ghostty](https://ghostty.org)
- [Hammerspoon](https://www.hammerspoon.org) (free, open-source)
- macOS
