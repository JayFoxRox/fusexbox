# This is very experimental software! Use at your own risk.
## Files might be deleted or overwritten by accident!

Tools to work on your original Xbox remotely using [FUSE](https://en.wikipedia.org/wiki/Filesystem_in_Userspace).


**Works on**

- Windows using [Dokany](http://dokan-dev.github.io/) or [WinFsp](http://www.secfs.net/winfsp/).
- macOS using [FUSE for macOS](https://osxfuse.github.io/).
- Linux and all other platforms supporting FUSE.

Your Xbox must be running a debug bios and requires xbdm.dll.


**Allows you to**

- Browse your Xbox drives and files remotely.
- Read and view files stored on your Xbox.
- Copy and write files to Xbox.
- Rename, or delete files remotely.
- Execute games remotely.


# Installation Instructions

Follow these instructions to install fusexbox:


* [Install Python 3 (includes pip)](https://www.python.org/downloads/) and run:

    ```
    pip3 install -U git+https://github.com/JayFoxRox/fusexbox.git#egg=fusexbox --process-dependency-links
    ```


On **Windows**, you also need one of the following FUSE providers:

* [Install Dokany](https://github.com/dokan-dev/dokany/wiki/Installation)
* [Install WinFsp](http://www.secfs.net/winfsp/download/)


On **macOS**, you also need one of the following FUSE providers:

* [FUSE for macOS](https://github.com/osxfuse/osxfuse/releases)


On **Linux**, no additional steps are necessary.


# Usage Instructions

## Mounting

After configuring xboxpy, you can mount your Xbox drives like this:

```
python3 fusexbox-mount <mount-point>
```

Also consult your FUSE providers manual.
If you can't solve your problem, create an issue on GitHub.


**Example:**

To mount your Xbox (IP: 192.168.0.2) to "/mnt/Xbox", you'd use:

```
export XBOX=192.168.0.2
mkdir -p /mnt/Xbox
python3 fusexbox-mount /mnt/Xbox
```

## Running games

fusexbox includes a helper script which tells fusexbox-mount, to run an XBE file.
This script is intended to be used in right-click menus in file managers.

To run an XBE file on your Xbox, use:

```
python3 fusexbox-run <file-in-fusexbox-filesystem>
```

**Example:**

To boot "F:\Games\Halo\default.xbe" you'd use:

```
python3 fusexbox-run /mnt/Xbox/F/Games/Halo/default.xbe
```


# Donate

If you like my work, a donation would be nice:

* [Patreon](https://www.patreon.com/jayfoxrox)
* [PayPal](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=x1f3o3x7x%40googlemail%2ecom&lc=GB&item_name=Jannik%20Vogel%20%28JayFoxRox%29&no_note=0&currency_code=USD&bn=PP%2dDonationsBF%3abtn_donateCC_LG%2egif%3aNonHostedGuest)

Even a small amount does help me and shows appreciation. Thank you!

---

**(C) 2018 Jannik Vogel**

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

*Contact me for other licensing options.*
