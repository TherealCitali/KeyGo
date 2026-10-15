"""Fail closed on wrong package, Android minimum or native ABI packaging."""
import re
import sys
import zipfile
from pathlib import Path
apk, manifest = map(Path, sys.argv[1:])
text = manifest.read_text()
assert "package: name='dev.citali.keygo'" in text, 'Wrong application ID'
assert int(re.search(r"(?:minSdkVersion|sdkVersion):'(\d+)'", text)[1]) <= 29, 'Android 10 excluded'
with zipfile.ZipFile(apk) as z:
    native = [n for n in z.namelist() if n.startswith('lib/') and n.endswith('.so')]
    assert native and {n.split('/')[1] for n in native} == {'arm64-v8a'}, native
    assert 'lib/arm64-v8a/libkeygo_bindings.so' in native, 'Rust crypto library missing'
    assert any('jnidispatch' in n for n in native), 'JNA bridge missing'
print('Verified separate application ID, Android 10 minimum compatibility, ARM64-only Rust + JNA')
