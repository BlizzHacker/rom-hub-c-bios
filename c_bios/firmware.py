"""c-bios `firmware`: one archive, and exactly the ROMs asked for.

    catalogue.SOURCES -> FirmwareArtifact[]
    FirmwareArtifact  -> FetchPlan -> the HOST downloads and unpacks

The plugin never fetches anything. It names a URL and the **host** fetches
it, after checking that URL against this plugin's `network` allowlist and
re-checking every redirect hop -- which matters more here than for most
plugins, because a SourceForge download ends on a mirror chosen per
request.

Both items name the same 269 KB archive, so installing both downloads it
twice. That is deliberate, and the same call `open-bios` made for its two
SameBoy items: an operator should be able to take the MSX2 BIOS without
the MSX1 one, and coupling them to save one download would trade a
property people rely on for a saving nobody asked for.

The archive holds 107 entries and 19 ROMs. An install keeps between two
and three of them and the host discards the rest, including the licence
text and the emulator config samples -- nothing an emulator scanning a
firmware directory has to step over.
"""

from rom_hub_sdk import FetchFile, FetchPlan, FirmwareArtifact, FirmwareProvider

from . import catalogue
from .platforms import NeedsMapping, platform_for  # noqa: F401


class ConfigError(Exception):
    """A config value this plugin will not build a member name out of."""


class UnknownFirmware(Exception):
    """No such item in this plugin's catalogue."""


class Firmware(FirmwareProvider):
    def list(self) -> list[FirmwareArtifact]:
        # The region is read here as well as in `plan()` so a bad value is
        # reported by `firmware list`, before an operator picks something
        # and finds out during an install.
        region = self._region()
        return [self._artifact(source, region) for source in catalogue.SOURCES]

    def plan(self, firmware: FirmwareArtifact) -> FetchPlan:
        region = self._region()
        try:
            source = catalogue.find(firmware.firmware_id)
        except KeyError as exc:
            raise UnknownFirmware(str(exc)) from None

        return FetchPlan(
            files=[
                FetchFile(
                    url=catalogue.ARCHIVE_URL,
                    filename=catalogue.ARCHIVE_FILENAME,
                    size_bytes=catalogue.ARCHIVE_BYTES,
                )
            ],
            # The host reads the artifact's platform for a firmware
            # install, not this one; FetchPlan requires the field, so it
            # is set to the same value rather than to a placeholder that
            # would disagree with what the operator was shown.
            platform=platform_for(source.system),
        )

    # -- building the catalogue -------------------------------------------

    def _artifact(self, source, region: str) -> FirmwareArtifact:
        members = (catalogue.main_member(source, region), *source.fixed_members)
        return FirmwareArtifact(
            firmware_id=source.firmware_id,
            name=source.name,
            # Raises "needs mapping" naming the system rather than
            # guessing one.
            platform=platform_for(source.system),
            # Stated, not derived. The licence is the two-clause BSD text
            # in the archive's own `doc/cbios.txt`; see `catalogue.py`.
            license="BSD-2-Clause",
            version=catalogue.CBIOS_VERSION,
            description=(
                f"{source.description} Region: "
                f"{catalogue.REGIONS[region]}. Source: "
                f"https://cbios.sourceforge.net/"
            ),
            archive="zip",
            members=list(members),
        )

    # -- configuration -----------------------------------------------------

    def _region(self) -> str:
        raw = str(self.ctx.config.get("region") or "").strip().lower()
        if raw in catalogue.REGIONS:
            return raw
        known = ", ".join(repr(r) for r in catalogue.REGIONS)
        raise ConfigError(
            f"region {raw!r} is not one this archive ships. It becomes part "
            f"of a ROM name inside the archive, so it is checked against the "
            f"table rather than interpolated: known regions are {known}, "
            f"where '' is the international build."
        )
