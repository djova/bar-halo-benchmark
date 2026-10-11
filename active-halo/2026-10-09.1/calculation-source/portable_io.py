"""Portable checksum closure and atomic output; standard library only.

This class implements the scientific functions' check/write/stop interface.
It does not replace an external execution admission or filesystem monitor.
"""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import time


SCIENTIFIC_SHA256 = {
    "scientific/independent_orbits.py": "bfa312a372fb046133a15ce7f08f636dbd8510c9377d18ec948d5a8de88e130b",
    "scientific/causal_response.py": "1df0ee3707926eb756bfe5c8a827461f0ad1a8a44f1bfe7ba44d00bf83808996",
    "scientific/volterra.py": "0b05fce93f8fdf615f5b298addce01bb6950a24d97c5435f7f0cf86de2e54fb1",
}


def verify_package(directory, expected_manifest_sha256=None):
    """Verify every packaged input before any scientific module is imported."""
    directory = Path(directory).resolve(strict=True)
    manifest_path = directory/"checksums.json"
    if manifest_path.resolve() != manifest_path:
        raise ValueError("Regular contained checksum manifest required")
    manifest_bytes = manifest_path.read_bytes()
    manifest_sha = hashlib.sha256(manifest_bytes).hexdigest()
    if expected_manifest_sha256 is not None and manifest_sha != expected_manifest_sha256:
        raise RuntimeError("Release checksum manifest differs from the requested digest")
    manifest = json.loads(manifest_bytes)
    if manifest.get("schema") != "portable-independent-cycle-checksums-v1":
        raise ValueError("Known complete package manifest required")
    rows = manifest.get("files")
    if not isinstance(rows, list) or not rows or len(rows) > 64:
        raise ValueError("Bounded explicit package file list required")
    seen = {}
    for row in rows:
        name = row["path"]
        relative = Path(name)
        if (not isinstance(name, str) or relative.is_absolute()
                or relative.as_posix() != name or ".." in relative.parts
                or name in seen or name == "checksums.json"):
            raise ValueError("Unique contained portable input path required")
        if (type(row["bytes"]) is not int or not 0 <= row["bytes"] <= 1024**2
                or not isinstance(row["sha256"], str) or len(row["sha256"]) != 64
                or any(c not in "0123456789abcdef" for c in row["sha256"])):
            raise ValueError("Exact bounded input size and SHA256 required")
        path = directory/relative
        if path.resolve(strict=True) != path or not path.is_file():
            raise ValueError("Regular contained portable input required: "+name)
        value = path.read_bytes()
        if len(value) != row["bytes"] or hashlib.sha256(value).hexdigest() != row["sha256"]:
            raise RuntimeError("Portable input changed: "+name)
        seen[name] = row
    required = {"run_cycle.py", "portable_io.py", "scientific/__init__.py",
                "inputs/population.json", "configs/gl8-preview.json",
                "configs/gl64-provisional.json", "README.md", "OUTPUTS.md"}
    if not (required | set(SCIENTIFIC_SHA256)) <= set(seen):
        raise ValueError("Complete portable source/configuration package required")
    if any(seen[name]["sha256"] != digest for name, digest in SCIENTIFIC_SHA256.items()):
        raise RuntimeError("Frozen scientific module bytes changed")
    return dict(package_sha256=manifest_sha, files=rows,
                scientific_SHA256=SCIENTIFIC_SHA256, directory=directory)


class PortableIO:
    """Fresh-output adapter; no host command, canonical drive or owner lookup."""
    def __init__(self, package, output, config, label, expected_manifest_sha256=None):
        self.package = Path(package).resolve(strict=True)
        self.expected_manifest_sha256 = expected_manifest_sha256
        closure = verify_package(self.package, expected_manifest_sha256)
        self.package_sha256 = closure["package_sha256"]
        self.inputs = closure["files"]
        proposed = Path(output).absolute()
        parent = proposed.parent.resolve(strict=True)
        self.path = parent/proposed.name
        if self.path.exists() or self.path.is_symlink():
            raise FileExistsError("A fresh output directory is required")
        if self.path == self.package or self.package in self.path.parents:
            raise ValueError("Run output must be outside the immutable package")
        self.path.mkdir()
        self.output_identity = (self.path.stat().st_dev, self.path.stat().st_ino)
        self.stop = [False]
        self.started_CPU = time.process_time()
        self.started_wall = time.monotonic()
        self.last_input_check = -float("inf")
        self.last_output = None
        self.write("START.json", dict(schema="portable-independent-cycle-start-v1",
            complete=False, configuration=config, configuration_label=label,
            input_files=self.inputs, checksum_manifest_sha256=self.package_sha256,
            scientific_module_SHA256=SCIENTIFIC_SHA256,
            fresh_orbit_construction=True, saved_numerical_inputs=False,
            execution_resource_admission="External; not provided by this I/O adapter"))

    def check(self, force_inputs=False):
        now = time.monotonic()
        stat = self.path.stat()
        if ((stat.st_dev, stat.st_ino) != self.output_identity
                or self.path.resolve() != self.path):
            raise RuntimeError("Portable output identity changed")
        if self.stop[0] or (self.path/"STOP").exists():
            self.stop[0] = True
            raise InterruptedError("Portable run stop requested")
        if force_inputs or now-self.last_input_check >= 10:
            closure = verify_package(self.package, self.package_sha256)
            if closure["files"] != self.inputs:
                raise RuntimeError("Portable source closure changed")
            self.last_input_check = now

    def write(self, name, value, arrays=False, np=None):
        if not isinstance(name, str) or Path(name).name != name or name in ("", ".", "..", "STOP"):
            raise ValueError("One regular contained output name required")
        self.check()
        fd, temporary = tempfile.mkstemp(prefix="."+name+"-", dir=self.path)
        try:
            with os.fdopen(fd, "wb" if arrays else "w") as stream:
                if arrays:
                    if np is None:
                        raise ValueError("Numerical archive backend must be supplied")
                    np.savez(stream, **value)
                else:
                    json.dump(value, stream, indent=2, allow_nan=False)
                    stream.write("\n")
                stream.flush()
                os.fsync(stream.fileno())
            self.check()
            os.replace(temporary, self.path/name)
            self.last_output = name
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    def terminal(self, complete, stage, error=None):
        """Close only after output completion; a stop can prevent this receipt."""
        self.check(force_inputs=True)
        record = dict(schema="portable-independent-cycle-terminal-v1",
            complete=bool(complete), status="complete" if complete else "failed",
            final_stage=stage, inputs_unchanged=True,
            checksum_manifest_sha256=self.package_sha256,
            process_CPU_seconds=time.process_time()-self.started_CPU,
            wall_seconds=time.monotonic()-self.started_wall,
            numerical_qualification=False, last_completed_output=self.last_output)
        if error is not None:
            record.update(error_type=type(error).__name__, error=str(error))
        self.write("TERMINAL.json", record)
        return record
