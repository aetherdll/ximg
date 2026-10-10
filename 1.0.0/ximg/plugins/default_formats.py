import os
import struct
from ximg.core import XImg

@XImg.register_format("fat12")
def create_fat12(output_path, file_list):
    disk_size = 1474560  # 1.44 MB Floppy
    disk_data = bytearray(disk_size)

    disk_data[0:3] = b"\xEB\x3C\x90"
    disk_data[3:11] = b"MSDOS5.0"
    struct.pack_into("<H", disk_data, 11, 512)
    disk_data[13] = 1
    struct.pack_into("<H", disk_data, 14, 1)
    disk_data[16] = 2
    struct.pack_into("<H", disk_data, 17, 224)
    struct.pack_into("<H", disk_data, 19, 2880)
    disk_data[21] = 0xF0
    struct.pack_into("<H", disk_data, 22, 9)
    struct.pack_into("<H", disk_data, 24, 18)
    struct.pack_into("<H", disk_data, 26, 2)
    disk_data[510:512] = b"\x55\xAA"

    fat_start = 512
    disk_data[fat_start:fat_start+3] = b"\xF0\xFF\xFF"

    root_dir_offset = 19 * 512
    data_start_offset = 33 * 512
    current_data_offset = data_start_offset
    current_cluster = 2

    for index, (real_path, img_name) in enumerate(file_list):
        if not os.path.exists(real_path):
            raise FileNotFoundError(f"File not found: {real_path}")
        
        with open(real_path, "rb") as f:
            file_content = f.read()
        
        file_size = len(file_content)
        base_name = os.path.basename(img_name).upper()
        name_part, ext_part = (base_name.split(".", 1) + [""])[:2]
        
        name_padded = name_part[:8].ljust(8).encode("ascii", errors="ignore")
        ext_padded = ext_part[:3].ljust(3).encode("ascii", errors="ignore")
        
        entry_offset = root_dir_offset + (index * 32)
        disk_data[entry_offset:entry_offset+8] = name_padded
        disk_data[entry_offset+8:entry_offset+11] = ext_padded
        disk_data[entry_offset+11] = 0x20
        
        struct.pack_into("<H", disk_data, entry_offset + 26, current_cluster)
        struct.pack_into("<I", disk_data, entry_offset + 28, file_size)

        disk_data[current_data_offset:current_data_offset+file_size] = file_content
        
        fat_offset = fat_start + int(current_cluster * 1.5)
        disk_data[fat_offset] = 0xFF
        disk_data[fat_offset + 1] = 0x0F

        current_data_offset += ((file_size + 511) // 512) * 512
        current_cluster += 1

    with open(output_path, "wb") as out_f:
        out_f.write(disk_data)
    print(f"[+] FAT12 disk image created successfully: {output_path}")

@XImg.register_format("fat32")
def create_fat32(output_path, file_list):
    disk_size = 20 * 1024 * 1024
    disk_data = bytearray(disk_size)
    disk_data[0:3] = b"\xEB\x58\x90"
    disk_data[3:11] = b"MSWIN4.1"
    struct.pack_into("<H", disk_data, 11, 512)
    disk_data[510:512] = b"\x55\xAA"

    current_offset = 64 * 512
    for real_path, img_name in file_list:
        if not os.path.exists(real_path):
            raise FileNotFoundError(f"File not found: {real_path}")
        with open(real_path, "rb") as f:
            content = f.read()
        disk_data[current_offset:current_offset+len(content)] = content
        current_offset += len(content)

    with open(output_path, "wb") as out_f:
        out_f.write(disk_data)
    print(f"[+] FAT32 disk image created successfully: {output_path}")

@XImg.register_format("iso")
def create_iso(output_path, file_list):
    iso_size = 2 * 1024 * 1024
    iso_data = bytearray(iso_size)
    pvd_offset = 16 * 512
    iso_data[pvd_offset] = 0x01
    iso_data[pvd_offset+1:pvd_offset+6] = b"CD001"

    data_offset = 20 * 2048
    for real_path, img_name in file_list:
        if not os.path.exists(real_path):
            raise FileNotFoundError(f"File not found: {real_path}")
        with open(real_path, "rb") as f:
            content = f.read()
        iso_data[data_offset:data_offset+len(content)] = content
        data_offset += len(content)

    with open(output_path, "wb") as out_f:
        out_f.write(iso_data)
    print(f"[+] ISO9660 image created successfully: {output_path}")

@XImg.register_format("ext4")
def create_ext4(output_path, file_list):
    ext4_size = 10 * 1024 * 1024
    ext4_data = bytearray(ext4_size)
    struct.pack_into("<H", ext4_data, 1080, 0xEF53)

    data_offset = 4096
    for real_path, img_name in file_list:
        if not os.path.exists(real_path):
            raise FileNotFoundError(f"File not found: {real_path}")
        with open(real_path, "rb") as f:
            content = f.read()
        ext4_data[data_offset:data_offset+len(content)] = content
        data_offset += len(content)

    with open(output_path, "wb") as out_f:
        out_f.write(ext4_data)
    print(f"[+] EXT4 container image created successfully: {output_path}")