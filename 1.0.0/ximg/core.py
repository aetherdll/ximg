import os
import struct
import importlib
import pkgutil
from ximg import plugins

class XImg:
    _FORMAT_REGISTRY = {}

    @classmethod
    def register_format(cls, name):
        """Decorator to register format builder plugins dynamically."""
        def decorator(func):
            cls._FORMAT_REGISTRY[name.lower()] = func
            return func
        return decorator

    @classmethod
    def load_plugins(cls):
        """Automatically discovers and imports all plugins in the plugins package."""
        if not cls._FORMAT_REGISTRY:
            package = plugins
            for _, modname, _ in pkgutil.iter_modules(package.__path__):
                importlib.import_module(f"{package.__name__}.{modname}")

    @classmethod
    def create_image(cls, output_path, file_list, format_type="fat12"):
        """Creates an image using the registered plugin for the specified format."""
        cls.load_plugins()
        format_type = format_type.lower()
        
        if format_type not in cls._FORMAT_REGISTRY:
            raise ValueError(f"Unsupported format: '{format_type}'. Available formats: {list(cls._FORMAT_REGISTRY.keys())}")
        
        builder_function = cls._FORMAT_REGISTRY[format_type]
        builder_function(output_path, file_list)

    @staticmethod
    def extract_image(img_path, output_dir="extracted_files"):
        """Extracts files from a FAT-compatible disk image."""
        if not os.path.exists(img_path):
            raise FileNotFoundError(f"Image file not found: {img_path}")

        os.makedirs(output_dir, exist_ok=True)
        with open(img_path, "rb") as f:
            disk_data = f.read()

        if len(disk_data) > 512 and disk_data[510:512] == b"\x55\xAA":
            root_dir_offset = 19 * 512
            data_start_offset = 33 * 512
            cluster_size = 512

            print(f"[*] Extracting files from disk image...")
            for i in range(224):
                entry_offset = root_dir_offset + (i * 32)
                name_bytes = disk_data[entry_offset:entry_offset+8]
                ext_bytes = disk_data[entry_offset+8:entry_offset+11]
                attr = disk_data[entry_offset+11]

                if name_bytes[0] == 0x00:
                    break
                if name_bytes[0] == 0xE5 or attr == 0x0F or (attr & 0x08):
                    continue

                name = name_bytes.decode("ascii", errors="ignore").strip()
                ext = ext_bytes.decode("ascii", errors="ignore").strip()
                filename = f"{name}.{ext}" if ext else name

                start_cluster = struct.unpack_from("<H", disk_data, entry_offset + 26)[0]
                file_size = struct.unpack_from("<I", disk_data, entry_offset + 28)[0]

                cluster_offset = data_start_offset + (start_cluster - 2) * cluster_size
                file_content = disk_data[cluster_offset:cluster_offset+file_size]

                out_file_path = os.path.join(output_dir, filename)
                with open(out_file_path, "wb") as out_f:
                    out_f.write(file_content)

                print(f"    [Extracted] {filename} ({file_size} bytes)")
            print(f"[+] Extraction completed to '{output_dir}'.")
        else:
            print("[-] Standard FAT boot signature not found. Extraction skipped.")