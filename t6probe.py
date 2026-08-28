#!/usr/bin/env python3
# Read-only probe for MCT Trigger 6 (0711:56xx): connector status, EDIDs, caps.
import struct
import sys

import usb.core
import usb.util

CTRL_IN = usb.util.CTRL_IN | usb.util.CTRL_TYPE_VENDOR | usb.util.CTRL_RECIPIENT_DEVICE


def ctrl_in(dev, req, wval, widx, length):
    try:
        return bytes(dev.ctrl_transfer(CTRL_IN, req, wval, widx, length, timeout=2000))
    except usb.core.USBError as e:
        return f"USB error: {e}"


def hexdump(data, prefix="    "):
    for i in range(0, len(data), 16):
        chunk = data[i:i + 16]
        print(f"{prefix}{i:04x}: {chunk.hex(' ')}")


def main():
    dev = usb.core.find(idVendor=0x0711, custom_match=lambda d: (d.idProduct & 0xFF00) == 0x5600)
    if dev is None:
        sys.exit("No Trigger 6 device found")
    print(f"Device: {dev.idVendor:04x}:{dev.idProduct:04x} bus {dev.bus} addr {dev.address}")

    print("\n== Adapter info (req 0xB0) ==")
    for idx, name, fmt in [(0, "HW platform", "u32"), (1, "Boot code ver", "u32"),
                           (2, "Image code ver", "u32"), (3, "Project code", "str"),
                           (4, "Vendor cmd ver", "u32")]:
        r = ctrl_in(dev, 0xB0, 0, idx, 16)
        if isinstance(r, str):
            print(f"  {name}: {r}")
        elif fmt == "u32":
            print(f"  {name}: 0x{struct.unpack('<I', r[:4])[0]:08x}")
        else:
            print(f"  {name}: {r.split(b'\\x00')[0].decode(errors='replace')}")

    print("\n== Video RAM (req 0x88) ==")
    r = ctrl_in(dev, 0x88, 0, 0, 1)
    print(f"  {r[0]} MB" if not isinstance(r, str) else f"  {r}")

    print("\n== Display section (req 0xB3, signature 0) ==")
    r = ctrl_in(dev, 0xB3, 0, 0, 112)
    if isinstance(r, str):
        print(f"  {r}")
    else:
        hexdump(r, "  ")
        tag, valid_size = struct.unpack_from("<II", r, 0)
        vid, pid = struct.unpack_from("<HH", r, 12)
        name = r[16:80].decode("utf-16-le", errors="replace").rstrip("\x00")
        version, dispfunc, caps1, caps2, dispintf = struct.unpack_from("<IIIII", r, 80)
        print(f"  tag={tag:#x} valid_size={valid_size} vdev={vid:04x}:{pid:04x} name={name!r}")
        print(f"  version={version} dispfunc={dispfunc:#010x}")
        for label, caps in (("Display1Caps", caps1), ("Display2Caps", caps2)):
            print(f"  {label}: link_intf={caps & 0xF} nres={(caps >> 8) & 0xFF} "
                  f"res_tbl_off={caps >> 16:#x} raw={caps:#010x}")
        print(f"  DisplayInterface raw={dispintf:#010x}: "
              f"DAC_i2c={dispintf & 3} DVO_i2c={(dispintf >> 8) & 3} "
              f"DVO_tx={(dispintf >> 12) & 0xF} DVI_i2c={(dispintf >> 16) & 3} "
              f"LVDS_i2c={(dispintf >> 24) & 3}")

    for view in (0, 1):
        print(f"\n== View {view} ==")
        r = ctrl_in(dev, 0x87, view, 0, 1)
        print(f"  Connector status: {r[0] if not isinstance(r, str) else r}")
        r = ctrl_in(dev, 0x84, view, 0, 4)
        if not isinstance(r, str):
            print(f"  Resolution table entries: {struct.unpack('<I', r)[0]}")
        else:
            print(f"  Resolution table entries: {r}")
        edid = b""
        for off in (0, 128):
            r = ctrl_in(dev, 0x80, off, view, 128)
            if isinstance(r, str):
                print(f"  EDID read @{off}: {r}")
                break
            edid += r
        if edid:
            good_hdr = edid[:8] == b"\x00\xff\xff\xff\xff\xff\xff\x00"
            csum = (-sum(edid[:128])) & 0xFF == 0
            print(f"  EDID block0: header {'OK' if good_hdr else 'BAD'}, "
                  f"checksum {'OK' if csum else 'BAD'}")
            hexdump(edid[:128], "  ")


if __name__ == "__main__":
    main()
