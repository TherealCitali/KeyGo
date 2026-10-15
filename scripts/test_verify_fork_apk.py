"""Regression tests for old/new aapt output and fail-closed package checks."""
import pathlib
import subprocess
import sys
import tempfile
import unittest
import zipfile

VERIFY = pathlib.Path(__file__).with_name('verify_fork_apk.py')

class VerifyApkTest(unittest.TestCase):
    def run_verifier(self, sdk="minSdkVersion:'26'", package='dev.citali.keygo', abi='arm64-v8a', jna=True):
        with tempfile.TemporaryDirectory() as directory:
            root = pathlib.Path(directory)
            with zipfile.ZipFile(root / 'test.apk', 'w') as apk:
                apk.writestr(f'lib/{abi}/libkeygo_bindings.so', b'test fixture')
                if jna:
                    apk.writestr(f'lib/{abi}/libjnidispatch.so', b'test fixture')
            (root / 'manifest.txt').write_text(f"package: name='{package}' versionCode='1'\n{sdk}\ntargetSdkVersion:'37'\n")
            return subprocess.run([sys.executable, str(VERIFY), str(root/'test.apk'), str(root/'manifest.txt')], capture_output=True).returncode

    def test_current_aapt(self):
        self.assertEqual(self.run_verifier(), 0)

    def test_legacy_aapt(self):
        self.assertEqual(self.run_verifier(sdk="sdkVersion:'26'"), 0)

    def test_android_10_excluded(self):
        self.assertNotEqual(self.run_verifier(sdk="minSdkVersion:'30'"), 0)

    def test_missing_minimum_not_confused_with_target(self):
        self.assertNotEqual(self.run_verifier(sdk=''), 0)

    def test_wrong_package(self):
        self.assertNotEqual(self.run_verifier(package='de.davis.passwordmanager'), 0)

    def test_wrong_abi(self):
        self.assertNotEqual(self.run_verifier(abi='x86_64'), 0)

    def test_missing_jna(self):
        self.assertNotEqual(self.run_verifier(jna=False), 0)

if __name__ == '__main__':
    unittest.main()
