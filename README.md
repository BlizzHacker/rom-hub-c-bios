# C-BIOS plugin for ROM Hub

A project of the [Move Weight Foundation](https://foundation.moveweight.com), an
Oklahoma non-profit corporation with 501(c)(3) status pending.

Implements the RPP v1 `firmware` capability: **C-BIOS**, a clean-room MSX
BIOS, downloaded into the Hub's configured firmware directory and — where
the library server can hold firmware — filed there too.

Nothing here is a dump of a retail chip. C-BIOS is a from-scratch
reimplementation whose own documentation calls it "a substitute BIOS which
is can be used for running MSX emulators", and **its licence permits binary
redistribution outright**.

| Capability | Source | Does |
|---|---|---|
| `firmware` | `sourceforge.net/projects/cbios/…/cbios-0.29a.zip` | names a zip; the **Hub** fetches it and keeps the declared members |

## Install

    rom-hub plugin install c-bios
    rom-hub firmware list c-bios
    rom-hub firmware install c-bios cbios-msx1

Files land in `$ROM_HUB_HOME/var/firmware/c-bios/`, or wherever
`ROM_HUB_FIRMWARE_DIR` points — point it at the `Machines/` or `system/`
directory openMSX or blueMSX already reads and there is nothing to copy
afterwards. That is the Hub's decision, not this plugin's: a plugin
returns a filename and never a path.

## What it offers

| `firmware` | Platform | Licence | Files |
|---|---|---|---|
| `cbios-msx1` | `msx` | BSD-2-Clause | `cbios_main_msx1.rom`, `cbios_logo_msx1.rom` |
| `cbios-msx2` | `msx2` | BSD-2-Clause | `cbios_main_msx2.rom`, `cbios_sub.rom`, `cbios_logo_msx2.rom` |

The main ROM varies by `region`; the sub and logo ROMs do not.

**C-BIOS carries no BASIC.** It runs cartridge images, which is what a ROM
library holds, and it will not give you a BASIC prompt. That is a property
of the project rather than a gap in this plugin, and it is the one thing
worth knowing before installing it.

Both items name the same 269 KB archive, so installing both downloads it
twice. Each item is independent on purpose — you should be able to take
the MSX2 BIOS without the MSX1 one.

## Licence, and where it was read

**BSD 2-clause.** `cbios-0.29a/doc/cbios.txt`, inside the archive this
plugin installs, carries the full text over nine copyright holders
(2002–2011). The clause that matters:

> Redistribution and use in source and binary forms, with or without
> modification, are permitted provided that the following conditions are
> met

Binary redistribution is permitted outright, which is the whole question
for a plugin that installs binaries. It was read out of the archive being
installed rather than off a badge on a hosting page.

### Why `open-bios` said this did not exist

`open-bios` lists C-BIOS among the items it left out, on the grounds that
`cbios/cbios` "publishes no built `.rom` files. Source only."

That is **true of the GitHub repository** — it carries tags but no
releases, and no built ROMs in the tree. It was never true of the project.
SourceForge has shipped built ROMs all along, and `cbios-0.29a.zip`
contains 19 of them.

Where a project publishes is a separate question from whether it
publishes, and the answer to the second one is not always on GitHub.

## Why MSX2+ is not here

The archive contains `cbios_main_msx2+.rom` and its three regional
variants, correctly licensed, and they are deliberately not offered.

**No plugin in this repository maps MSX2+ to a platform.** Five plugins
map MSX — `hasheous`, `libretro-database`, `libretro-thumbnails`,
`openvgdb`, `retroachievements` — and four of them also map MSX2. None
goes further. There is no slug to file MSX2+ under, and every available
choice is wrong: `msx2` would put it where an MSX2 machine would try to
run it, and inventing `msx2plus` would name a platform nobody's library
has.

This is the call `open-bios` made about SameBoy's Super Game Boy boot
ROMs, for the same reason. When a library platform for MSX2+ exists this
is a two-line change, and the ROMs are already inside the archive being
downloaded.

## Config

| Key | Type | Default | Meaning |
|---|---|---|---|
| `region` | `str` | `""` | which regional main ROM to install |

Known values are `""` (international), `"eu"`, `"jp"` and `"br"`. The
regional builds differ in character set and keyboard layout, not in
whether they run, so the international build is right unless you know you
want otherwise.

The value becomes part of a **member name inside the archive**, so it is
checked against the table in `c_bios/catalogue.py` before it is used and
never interpolated raw. An unknown region is refused by name, at
`firmware list`, before an install can pick it up.

No credentials. The host is public and unauthenticated, and this plugin
sends nothing at all — it makes no request of its own. The Hub makes one
GET per install.

## Network

`sourceforge.net`, `downloads.sourceforge.net`, `*.dl.sourceforge.net`.

The wildcard is not laziness. A SourceForge download redirects twice and
**the final hop is a mirror chosen per request**: two observations of the
identical URL on 2026-07-30 finished on `cfhcable.dl.sourceforge.net` and
on `pilotfiber.dl.sourceforge.net`. There is no enumerable set of hosts to
write down.

It is also as narrow as it can be — `netpolicy.url_allowed` treats a `*.`
prefix as one or more leading labels and never the bare domain, so this
grants `<mirror>.dl.sourceforge.net` and grants neither `sourceforge.net`
itself nor a lookalike like `dl.sourceforge.net.example.com`.
`archive-org` declares `*.archive.org` on the same basis.

## Platforms

`c_bios/platforms.py` maps this plugin's system names to library platform
slugs by exact match, with **no fallback**. A system that is not in the
table raises "needs mapping" and names itself, and the catalogue refuses
to be built.

| System | Platform slug |
|---|---|
| MSX | `msx` |
| MSX2 | `msx2` |

Those two slugs were read off the five plugins in this repository that
already map MSX, not chosen. Agreeing with them costs nothing; disagreeing
would file C-BIOS somewhere no other plugin looks.

## Terms

Redistributable by its own project's licence, stated above with the
evidence beside it. The Hub cannot verify any of this — a dumped BIOS and
a reimplemented one look identical on the wire — so it is a rule about
what this catalogue may contain, enforced by review of
`c_bios/catalogue.py`.

## Licence

MIT (this plugin's own code). The firmware it installs is BSD-2-Clause,
carried by the C-BIOS project and printed by `rom-hub firmware list`.
