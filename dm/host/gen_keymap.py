#!/usr/bin/env python3
"""The Mac keyboard map (dm/host/keymap.tsv) into dm/host/gen/keymap.h, which front_mac.m includes.

Run by dm/host/Makefile (gen/keymap.h) as: python3 gen_keymap.py keymap.tsv gen/keymap.h
The header is written only when it changed, so an unchanged map does not rebuild the host.
"""
import sys
from pathlib import Path

BUTTONS = ['A', 'B', 'X', 'Y', 'LS', 'RS', 'L', 'R', 'ZL', 'ZR', 'Plus', 'Minus', 'Left', 'Up', 'Right', 'Down']
LEFT = ['LLeft', 'LUp', 'LDown', 'LRight']
RIGHT = ['RLeft', 'RUp', 'RRight', 'RDown']
MODS = ('shift', 'option', 'control', 'command')


def main(argv):
    src, out = Path(argv[1]), Path(argv[2])
    rows = {}
    for line in src.read_text(encoding='utf-8').splitlines():
        s = line.strip()
        if not s or s.startswith('#'):
            continue
        f = [x.strip() for x in s.split('\t')]
        if len(f) < 2 or len(f) > 3:
            raise SystemExit(f'{src}: a row takes "control<TAB>keycode<TAB>[modifier]": {line!r}')
        control, code = f[0], f[1]
        mod = f[2] if len(f) > 2 else ''
        if control in rows:
            raise SystemExit(f'{src}: {control} is listed twice')
        try:
            kc = int(code, 0)
        except ValueError:
            raise SystemExit(f'{src}: {control}: keycode {code!r} is not a number')
        if not 0 <= kc <= 255:
            raise SystemExit(f'{src}: {control}: keycode {kc} is not 0..255')
        if mod and control not in RIGHT:
            raise SystemExit(f'{src}: {control}: a modifier is only for the right stick ({", ".join(RIGHT)})')
        rows[control] = (kc, mod)
    want = BUTTONS + LEFT + RIGHT + ['Shake']
    if missing := [c for c in want if c not in rows]:
        raise SystemExit(f'{src}: missing {", ".join(missing)}')
    if extra := [c for c in rows if c not in want]:
        raise SystemExit(f'{src}: unknown control {", ".join(extra)}')
    rmods = {rows[c][1] for c in RIGHT}
    if len(rmods) != 1:
        raise SystemExit(f'{src}: the right stick rows must agree on one modifier, got {sorted(rmods)}')
    mod = next(iter(rmods))
    if mod and mod not in MODS:
        raise SystemExit(f'{src}: unknown modifier {mod!r} (shift, option, control, command, or empty)')
    text = '\n'.join([
        '// Generated from dm/host/keymap.tsv by dm/host/gen_keymap.py. Do not edit.',
        '#ifndef GEN_KEYMAP_H',
        '#define GEN_KEYMAP_H',
        '// Buttons A B X Y LS RS L R ZL ZR Plus Minus Left Up Right Down, as macOS virtual key codes',
        f'static const unsigned short keymap_btn[16] = {{{",".join(str(rows[c][0]) for c in BUTTONS)}}};',
        '// Left stick LLeft LUp LDown LRight (WASD by default)',
        f'static const unsigned short keymap_left[4] = {{{",".join(str(rows[c][0]) for c in LEFT)}}};',
        '// Right stick RLeft RUp RRight RDown, with keymap_right_mod held (the arrows with Shift by default)',
        f'static const unsigned short keymap_right[4] = {{{",".join(str(rows[c][0]) for c in RIGHT)}}};',
        f'static const char keymap_right_mod[] = "{mod}";',
        '// Shake the controller',
        f'static const unsigned short keymap_shake = {rows["Shake"][0]};',
        '#endif',
        '',
    ])
    if out.is_file() and out.read_text(encoding='utf-8') == text:
        return 0
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix('.h.tmp')
    tmp.write_text(text, encoding='utf-8')
    tmp.replace(out)
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
