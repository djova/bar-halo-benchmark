#!/usr/bin/env python3
"""Retrieve the unchanged official MNRAS package into the private build inputs."""
import hashlib,io,zipfile,urllib.request
from pathlib import Path
URL='https://mirrors.ctan.org/macros/latex/contrib/mnras.zip'
SHA256='9d453e272a47648b4418b76577c82c331c0a1499a2a620676d3997f5104adf82'
root=Path(__file__).resolve().parents[2]
data=urllib.request.urlopen(URL,timeout=60).read()
assert hashlib.sha256(data).hexdigest()==SHA256,'Template archive changed; review before adopting.'
with zipfile.ZipFile(io.BytesIO(data))as z:
 for name in z.namelist():
  assert not Path(name).is_absolute() and '..' not in Path(name).parts
 z.extractall(root/'research/publication/mnras/vendor')
print('MNRAS 3.2 archive verified and extracted.')
