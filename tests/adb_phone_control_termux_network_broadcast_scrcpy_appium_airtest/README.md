device discovery, termux daemon, remote unlock

unlock requires screenshot and input events.

https://technastic.com/unlock-android-phone-pin-pattern-adb/

click ok after input password:

https://stackoverflow.com/questions/29072501/how-to-unlock-android-phone-through-adb

scrcpy client

https://github.com/leng-yue/py-scrcpy-client
https://leng-yue.github.io/py-scrcpy-client/guide.html#bind-events

you want to use android emulator on macos m1?

https://github.com/google/android-emulator-m1-preview/releases/tag/0.3

check android screen lock/unlock state

https://android.stackexchange.com/questions/191086/adb-commands-to-get-screen-state-and-locked-state

Bonjour/Avahi/Zeroconf

logic: if the kill switch is off, when no physical input events happens, or not focused on scrcpy window with keyboard/mouse input events on pc for some time, allow to interact with the phone.

get physical events:

warning: this command could be offline for a short period of time after using the scrcpy. must automatically reconnect if the device is not offline.

```bash
adb -s 192.168.10.3:5555 shell getevent
```

to get focused window:

to get input events on macos:

input events on linux: