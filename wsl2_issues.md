# WSL2における開発の障害や問題について記していくよ

### `snapd`が使えない問題について  
-----


https://github.com/microsoft/WSL/issues/5126

#### genieを使う
https://github.com/arkane-systems/genie

A quick way into a systemd "bottle" for WSL
WSL2でsystemdをpid 1として実行することができるよ

INSTALLATION
Ubuntuは上記のDebianのパッケージを使ってくださいとのこと

つまり
daemonize, dbus, dotnet-runtime-5.0, gawk, 
libc6, libstdc++6, policykit-1, systemd, and systemd-container.

Debian パッケージをビルドするには debhelper と dotnet-sdk-5.0 (およびオプションで pbuilder) が必要

ってことでこいつらを用意してからgenieをインストールしますと。

Ubuntuに.NET SDKまたは.NET RUNTIMEをインストールする
