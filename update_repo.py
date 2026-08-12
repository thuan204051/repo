#!/usr/bin/env python3
import bz2, gzip, hashlib, os, subprocess
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DEBS = ROOT / "debs"

def digest(data, algorithm):
    h = hashlib.new(algorithm); h.update(data); return h.hexdigest()

def control_for(deb):
    output = subprocess.check_output(["dpkg-deb", "-f", str(deb)], text=True).strip()
    data = deb.read_bytes()
    fields = [output,
        f"Filename: debs/{deb.name}",
        f"Size: {len(data)}",
        f"MD5sum: {digest(data, 'md5')}",
        f"SHA1: {digest(data, 'sha1')}",
        f"SHA256: {digest(data, 'sha256')}"]
    return "\n".join(fields)

debs = sorted(DEBS.glob("*.deb"))
if not debs:
    raise SystemExit("No .deb files found in debs/")
packages = ("\n\n".join(control_for(deb) for deb in debs) + "\n").encode()
(ROOT / "Packages").write_bytes(packages)
(ROOT / "Packages.gz").write_bytes(gzip.compress(packages, compresslevel=9, mtime=0))
(ROOT / "Packages.bz2").write_bytes(bz2.compress(packages, compresslevel=9))

release_files = ["Packages", "Packages.gz", "Packages.bz2"]
header = [
    "Origin: @thuanazura",
    "Label: @thuanazura Repo",
    "Suite: stable",
    "Version: 1.0",
    "Codename: ios",
    "Architectures: iphoneos-arm",
    "Components: main",
    "Description: PixelCore and VivoFlip tweaks for jailbroken iOS 7-9",
    f"Date: {format_datetime(datetime.now(timezone.utc), usegmt=True)}",
]
for title, algo in (("MD5Sum", "md5"), ("SHA1", "sha1"), ("SHA256", "sha256")):
    header.append(f"{title}:")
    for name in release_files:
        data = (ROOT / name).read_bytes()
        header.append(f" {digest(data, algo)} {len(data):16d} {name}")
(ROOT / "Release").write_text("\n".join(header) + "\n", encoding="utf-8")
print(f"Generated repository metadata for {len(debs)} packages.")
