# Independently signed KeyGo builds

- Application ID: `dev.citali.keygo`; upstream Kotlin namespaces remain unchanged.
- Version: `2.2.0-fork.1`, code 1. Increment the code before future app updates.
- Release flavor: F-Droid (upstream open-source flavor), ARM64 (`arm64-v8a`) only.
- minSdk 26 remains unchanged, so Android 10/API29 is included. Target/compile SDK
  remain upstream values; lowering target SDK is not a compatibility fix.
- No vault crypto, storage, backup or authentication implementation changes.
- This is not signed by the original developer. It cannot read the original app’s
  sandbox or automatically migrate its vault. Use the app’s supported export/import
  if needed; keep a verified backup and never uninstall your only copy of a vault.
- The inherited Play Store publisher is restricted to the original repository.

## CI and signing

Pushes to `main` and manual runs execute Rust tests, Android unit tests, lint,
release assembly, signature/manifest/ABI verification and an Android 10 emulator
launch smoke test using an extra x86_64 staging build. The release APK stays ARM64.
The smoke test is not a full vault/autofill/security audit or a physical ARM64 test.
PRs run checks without signing secrets or release permissions.
Only successful main builds publish a prerelease plus SHA256 and verification
artifacts. Keep the newest five published prereleases; stable releases and drafts
are never pruned. Repository variables/secrets contain no vault data.

Release secrets: `SIGNING_KEY_BASE64`, `KEYSTORE_PASSWORD`, `KEY_ALIAS`, `KEY_PASSWORD`.
The dedicated PKCS12 keystore is decoded only under runner temporary storage and
removed even on failure. Keep the private backup offline; losing it prevents
updates to installed builds. Never commit a keystore or log its passwords.

Local unsigned build: `./gradlew :app:assembleFdroidRelease`.
For emulator development use `-Pkeygo.abis=arm64-v8a,x86_64`; ARM64 is retained
because upstream UniFFI binding generation reads the ARM64 library.
