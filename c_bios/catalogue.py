"""What this plugin offers, and the evidence for each entry.

Every claim below was checked against the archive itself on 2026-07-30 --
downloaded, opened, and read -- rather than against a wiki or a memory.

## The rule

**Clean-room and openly licensed, or it is not here.** C-BIOS is a
from-scratch MSX BIOS, not a dump of a Microsoft or Panasonic chip. Its
own documentation opens by calling it "a substitute BIOS which is can be
used for running MSX emulators" [sic].

## The licence, read out of the archive

`cbios-0.29a/doc/cbios.txt` carries the full text. It is a two-clause BSD
licence over nine copyright holders (BouKiCHi, Reikan, Maarten ter
Huurne, Albert Beevendorp, Patrick van Arkel, Manuel Bilderbeek, Joost
Yervante Damad, Jussi Pitkanen, Eric Boon), 2002-2011, and the clause
that matters here is the first line of the grant:

    Redistribution and use in source and binary forms, with or without
    modification, are permitted provided that the following conditions
    are met

Binary redistribution is permitted outright. That is the whole question
for a plugin that installs binaries, and it is answered in the archive
being installed rather than by a badge on a hosting page.

## Why this is not read off GitHub

`open-bios` excluded C-BIOS on the grounds that `cbios/cbios` "publishes
no built `.rom` files. Source only." That is **true of the GitHub
repository** -- it has tags but no releases, and no built ROMs in the
tree. It was never true of the project: SourceForge has shipped built
ROMs the whole time, and `cbios-0.29a.zip` carries 19 of them.

The lesson is the one `open-bios` already learned from SameBoy's
NOASSERTION: where a project publishes is a separate question from
whether it publishes, and the answer to the second one is not on GitHub.

## Why the catalogue is static

`list()` makes no network request, for the reasons `open_bios/catalogue`
gives: firmware is bytes an emulator *executes*, so an operator should
get the release this plugin says it verified, and a catalogue that costs
nothing is one people run.
"""

from dataclasses import dataclass

#: The release this plugin was verified against. C-BIOS moves rarely --
#: 0.29a is the current release on SourceForge -- and the version is part
#: of the download path, so it is pinned rather than discovered.
CBIOS_VERSION = "0.29a"

#: The directory the release sits in, which is **not** the release name.
#: SourceForge files the point release `0.29a` under `0.29`, so deriving
#: one from the other produces a 404 -- which is what it did, until an
#: end-to-end install said so. Two constants, because they are two facts.
CBIOS_DIR = "0.29"

#: Measured 2026-07-30: this URL answers 200 and 269,374 bytes, after two
#: redirects onto a mirror chosen per request. See `manifest.toml` for why
#: that makes a wildcard host unavoidable.
ARCHIVE_URL = (
    "https://sourceforge.net/projects/cbios/files/cbios/"
    f"{CBIOS_DIR}/cbios-{CBIOS_VERSION}.zip/download"
)
ARCHIVE_FILENAME = f"cbios-{CBIOS_VERSION}.zip"
ARCHIVE_BYTES = 269374

#: Regions the archive ships a main ROM for. The empty string is the
#: international build, which is the file with no suffix at all.
#:
#: A region is operator configuration that becomes part of a **member
#: name**, so it is checked against this table before it is used. It is
#: never interpolated from a free string -- the same rule `open-bios`
#: applies to `sameboy_release`, for the same reason.
REGIONS: dict[str, str] = {
    "": "international",
    "eu": "Europe",
    "jp": "Japan",
    "br": "Brazil",
}

DEFAULT_REGION = ""


@dataclass(frozen=True)
class Source:
    """One installable firmware item, before it becomes a FirmwareArtifact."""

    firmware_id: str
    name: str
    #: This plugin's system name. `platforms.platform_for` turns it into a
    #: library platform slug, or refuses.
    system: str
    description: str
    #: The main BIOS ROM, without its region suffix or extension. The
    #: region is appended by `firmware.py` after validation.
    main_stem: str
    #: Members that do not vary by region -- the sub ROM and the logo.
    fixed_members: tuple[str, ...]


#: MSX2+ is absent on purpose. `platforms.py` says why at length: no
#: plugin in this repository maps it, so there is no slug to file it
#: under, and its four ROMs are in the archive already if that changes.
SOURCES: tuple[Source, ...] = (
    Source(
        firmware_id="cbios-msx1",
        name="C-BIOS for MSX1",
        system="MSX",
        description=(
            "Clean-room MSX1 BIOS and logo ROM. Runs cartridge images; it "
            "carries no BASIC, which is the one thing an operator should "
            "know before installing it."
        ),
        main_stem="cbios_main_msx1",
        fixed_members=("cbios_logo_msx1.rom",),
    ),
    Source(
        firmware_id="cbios-msx2",
        name="C-BIOS for MSX2",
        system="MSX2",
        description=(
            "Clean-room MSX2 BIOS, sub ROM and logo ROM. The sub ROM is "
            "not optional on MSX2 -- an emulator wants both halves."
        ),
        main_stem="cbios_main_msx2",
        fixed_members=("cbios_sub.rom", "cbios_logo_msx2.rom"),
    ),
)


def find(firmware_id: str) -> Source:
    """The source with this id, or `KeyError` naming what is here.

    `plan()` looks an item up rather than trusting the artifact handed
    back to it: that artifact left this process, and believing its fields
    would mean building a member name out of a value that made a round
    trip through somewhere else.
    """
    for source in SOURCES:
        if source.firmware_id == firmware_id:
            return source
    known = ", ".join(s.firmware_id for s in SOURCES)
    raise KeyError(f"no firmware {firmware_id!r} here; this plugin has {known}")


def main_member(source: Source, region: str) -> str:
    """The main ROM member for `source` in `region`.

    The international build has no suffix; every other region appends
    `_<region>`. Region has already been checked against `REGIONS` by the
    caller -- this function does not validate, so that there is one place
    that does.
    """
    if not region:
        return f"{source.main_stem}.rom"
    return f"{source.main_stem}_{region}.rom"
