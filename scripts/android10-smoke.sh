#!/usr/bin/env bash
set -euo pipefail
mkdir -p smoke-results
apk=$(find app/build/outputs/apk/fdroid/staging -name '*.apk' -type f)
test -f "$apk"
adb install -r "$apk"
adb logcat -c
adb shell am start -W -n dev.citali.keygo.staging/de.davis.keygo.app.presentation.MainActivity | tee smoke-results/launch.txt
sleep 15
adb logcat -d > smoke-results/logcat.txt
adb shell pidof dev.citali.keygo.staging | tee smoke-results/pid.txt
test -s smoke-results/pid.txt
! grep -E 'FATAL EXCEPTION|Fatal signal|UnsatisfiedLinkError' smoke-results/logcat.txt
adb shell uiautomator dump /sdcard/keygo-window.xml
adb pull /sdcard/keygo-window.xml smoke-results/window.xml
grep -q 'package="dev.citali.keygo.staging"' smoke-results/window.xml
adb exec-out screencap -p > smoke-results/android10.png
printf 'API29 staging launch passed. This is not an end-to-end vault test.\n' | tee smoke-results/RESULT.txt
