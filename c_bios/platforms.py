"""This plugin's system names -> a library platform slug.

Exact match, no fallback, for the reason `open_bios/platforms.py` gives:
a ROM under the wrong system is visibly wrong, and a BIOS under the wrong
system is *invisible* -- the emulator goes on reporting it has none, and
nothing anywhere says why.

The two slugs below were not chosen, they were **read off this project**.
Five plugins already map MSX and they agree: `hasheous`,
`libretro-database`, `libretro-thumbnails`, `openvgdb` and
`retroachievements` all use `msx`, and the first four also use `msx2`.
Agreeing with them costs nothing and disagreeing would file C-BIOS
somewhere no other plugin looks.

## Why MSX2+ is absent, when C-BIOS ships it

`cbios-0.29a.zip` contains `cbios_main_msx2+.rom` and its three regional
variants, and they are deliberately not offered.

**No plugin in this repository maps MSX2+ to anything.** The five listed
above stop at `msx2`. There is no slug to file it under, and the choices
available are all bad: `msx2` would put a MSX2+ BIOS under MSX2, where an
MSX2 machine would try to run it, and inventing `msx2plus` would create a
platform nobody's library has.

This is the same call `open-bios` made about SameBoy's Super Game Boy
boot ROMs -- present in the archive, correctly licensed, and left out
because a SNES peripheral has no unambiguous platform. When a library
platform for MSX2+ exists, this is a two-line change and the ROMs are
already in the archive being downloaded.
"""

#: System, as this plugin's catalogue names it -> library platform slug.
SYSTEM_PLATFORMS: dict[str, str] = {
    "MSX": "msx",
    "MSX2": "msx2",
}


class NeedsMapping(Exception):
    """A system this plugin has no platform slug for."""


def platform_for(system: str) -> str:
    """The library platform slug for `system`, or a refusal naming it.

    Called while building the catalogue, so a source added without a row
    here fails at `rom-hub firmware list` rather than shipping an item
    that cannot be filed.
    """
    try:
        return SYSTEM_PLATFORMS[system]
    except KeyError:
        known = ", ".join(sorted(SYSTEM_PLATFORMS))
        raise NeedsMapping(
            f"system {system!r} needs mapping: it is not in this plugin's "
            f"system -> platform table, which knows {known}. This plugin "
            f"will not guess a platform for firmware -- a BIOS filed under "
            f"the wrong system is invisible, not visibly wrong."
        ) from None
