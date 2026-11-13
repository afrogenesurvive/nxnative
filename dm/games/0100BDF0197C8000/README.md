# Once Upon A KATAMARI (`0100BDF0197C8000`)

Bring-up in progress — this folder is documentation only; there is **no repository profile yet** (`game.tsv`). The NSP script builds the title from a provisional profile it guesses itself, outside the repository. SDK 19.3.3. Unity IL2CPP on NVN, with CRIWARE and FMOD audio. Modules `main`, `subsdk0` (`NintendoSDK_movie`) and `sdk`. Update 1.0.2 (v65536) over the base XCI.

Verified on the Mac: the `.app` boots past the SDK's server-environment abort and renders the opening (reached frame 1200+ at 30 fps, 1920×1080, the CRI movie-decode thread running, saves committed and the pipeline prewarm completed). Not yet driven through gameplay; not in the games table.

## Building from scratch

The game files live outside the repository (`~/Documents/my_nsx_backups/once_upon_a_katamari/Once_Upon_A_KATAMARI_NSW-HR/`: `hr-bajua.xci` base, `hr-bajuav65536.nsp` update 1.0.2, `hr-bajua.nfo`). The tool venv and keys are `~/Documents/my_nsx_backups/venv` and `~/Documents/my_nsx_backups/prod.keys`.

```
~/Documents/my_nsx_backups/venv/bin/python3 scripts/build_ipa_from_nsp.py \
  ~/Documents/my_nsx_backups/once_upon_a_katamari/Once_Upon_A_KATAMARI_NSW-HR \
  -k ~/Documents/my_nsx_backups/prod.keys \
  --platform mac-app --progress lines
```

That run writes the survey (`<folder>/0100BDF0197C8000_survey/`), guesses the provisional profile (`<folder>/0100BDF0197C8000_build/profile/0100BDF0197C8000/`), rewrites `main` / `subsdk0` / `sdk`, builds the shader library for the Mac and packs the self-contained `Once Upon A KATAMARI.app`. The default platform is `ios` (a `.ipa`); `--platform mac-app` is the `.app`. The shader step needs the Mac outputs for the `.app` and the iOS ones too (`IOSOUT`) if a `.ipa` is wanted as well. The shader build is the large one: it needs several GB of free disk.

## What the provisional profile needs

`profile_guess.py` writes these keys; the next from-scratch run re-guesses them from the game's files:

| Setting | Value | Why |
|---|---|---|
| `mem_reserve` / `mem_alias` / `mem_stack` | `0x140000000` / `0x118000000` / `0x10000000` | the NPDM declares 16 MB of system resource and `main` never sets a heap: a 5 GB block with a 4.375 GB alias region, where the game maps its memory itself |
| `sys_resource` | `0x1000000` | the NPDM's 16 MB of system resource |
| `app_pool` | `0xCD500000` | the provisional check-boot pool |
| `depth_mode` | `zero` | the game calls `nvnDeviceSetDepthMode` with near = 0 in the check boot, before the pipeline bases are made |
| `shader_groups` | `/Data/=data` | the stage shaders live under RomFS `Data/` |
| `modules` | `main subsdk0 sdk` | `subsdk0` is the movie module the game's movie player needs |
| `romfs_marker` | `Data/StreamingAssets/Sound/BGM_InGame.awb` | the RomFS marker file |
| `zip_store` | `.acb:.assets:.awb:.bin:.bundle:.dat:.ress:.usm:.metallib` | the compressed asset extensions |

Build IDs: `main` `ff53171b18c7701a7c7b5e8a43366598`, `subsdk0` `385e6321fcbcb9d62f71073f66405a6a`, `sdk` `a65883c2863f42f93e0f43f2d7aba0e8`; shader chain `2afd39090b76`.

## Fixes

- **Resolved, general: the SDK's server-environment abort.** The game calls `nn::nsd::GetApplicationServerEnvironmentType`, whose SDK opens the `nsd:a` / `nsd:u` service and hardcodes an abort (`Result 0xe8d`) when it cannot. The host takes the getter over to return 0 (retail) — see [The application's server environment](../../../docs/reference/services.md#the-applications-server-environment). This is a host hook in `dm/host/hle_offline.c`, not a profile key, so a from-scratch build of this title picks it up as long as that file has it.

## Open

- Two `[RED]` NVN unimplemented no-ops the game calls during the opening (the host ignores them): `nvnCommandBufferSetConservativeRasterDilate` and `nvnCommandBufferSetSubpixelPrecisionBias`.
- Only the boot and the opening minute have been checked; gameplay, saves across sessions and the remaining scenes are untested.
