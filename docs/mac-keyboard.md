# Mac keyboard

The Mac app maps the keyboard to the Switch controller. The default is below; edit [`dm/host/keymap.tsv`](../dm/host/keymap.tsv) to rebind, and the next Mac app build takes it (the map is compiled into the host, [`dm/host/front_mac.m`](../dm/host/front_mac.m), which the Makefile turns the table into a header for — there is no way to change the keys of an already-built app without rebuilding the host).

## Default map

| Key                 | Switch control                             |
| ------------------- | ------------------------------------------ |
| **J**               | A (confirm)                                |
| **K**               | B (back / cancel)                          |
| **U**               | X                                          |
| **I**               | Y                                          |
| **F**               | Press left stick (LS)                      |
| **G**               | Press right stick (RS)                     |
| **Q**               | L                                          |
| **E**               | R                                          |
| **Z**               | ZL                                         |
| **C**               | ZR                                         |
| **Return**          | + (Plus)                                   |
| **Tab**             | − (Minus)                                  |
| **← ↑ → ↓**         | D-pad                                      |
| **Shift + ← ↑ → ↓** | Right stick (the camera in 3D games)       |
| **W A S D**         | Left stick (W up, A left, S down, D right) |
| **Space**           | Shake the controller                       |

The left mouse button is the touchscreen. In the controller-pairing prompt, Return or J is done, Escape or K closes it.

## Rebinding

Edit [`dm/host/keymap.tsv`](../dm/host/keymap.tsv): one row per control, `control`, `keycode` and an optional `modifier`, tab-separated. The controls are

- the buttons in Switch bit order: `A B X Y LS RS L R ZL ZR Plus Minus Left Up Right Down`,
- the left stick `LLeft LUp LDown LRight`, the right stick `RLeft RUp RRight RDown`, and `Shake`.

The `keycode` is the macOS virtual key code, 0–255 (decimal or `0x` hex). The `modifier` is `shift`, `option`, `control` or `command`, and only the right stick takes one: the default maps the right stick to the arrow keys with `shift`, so the arrows are the D-pad alone and the right stick with Shift held. To give the right stick its own keys, leave the modifier empty and name four keys the D-pad does not use. `command` shortcuts go to the menu, so ⌘-keys never reach the game.

A row that is missing, listed twice, names an unknown control or a key code outside 0–255 stops the build with a message.

## Key codes

macOS virtual key codes for the common keys: `A=0 S=1 D=2 F=3 G=5 Z=6 X=7 C=8 Q=12 W=13 E=14 R=15 T=17 Y=16 U=32 I=34 O=31 P=35 J=38 K=40 L=37 Return=36 Tab=48 Space=49 Escape=53`, the arrows `123← 126↑ 124→ 125↓`, and Shift `56`/`60`. The full table is Apple's `HIToolbox/Events.h` (`kVK_ANSI_A`, `kVK_Return`, …).

## Rebuilding

The map is read when the host is built. Change [`dm/host/keymap.tsv`](../dm/host/keymap.tsv) and rebuild the host (`make -C dm/host GAME=<title ID> dmhost`), or simply run the NSP script again (`--platform mac-app`): it rebuilds the host and re-packs the app, reusing the shaders and the extracted files. To patch a finished app in place instead, copy the rebuilt `dmhost` over `Contents/MacOS/dmhost` and re-sign it ad-hoc.
