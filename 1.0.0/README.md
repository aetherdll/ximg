# XImg

XImg is a lightweight, plugin-based, 100% pure Python library and command-line utility for creating and extracting disk and file system images (`.img`, `.iso`) without requiring any external system tools or dependencies.

## Supported Formats (via Plugins)

- **FAT12**: Floppy disk image simulation (fully extractable).
- **FAT32**: Large disk container simulation.
- **ISO**: ISO9660 optical media image simulation.
- **EXT4**: Linux EXT4 container structure simulation.

## Installation

Clone or download the project repository, navigate to the root directory where `pyproject.toml` is located, and install it locally in editable mode:

```bash
pip install -e .
```

To install it globally from PyPI (once published):

```bash
pip install ximg
```

## Usage

1. Creating Images
   You can specify the target format using the -f or --format flag (fat12, fat32, iso, ext4).

Create a FAT12 image:

````bash
ximg create -o img_file_name.img -f fat12 file_name.txt
```s

Create a FAT32 image:

```bash
ximg create -o img_file_name.img -f fat32 file_name.txt
````

Create an ISO image:

```bash
ximg create -o iso_file_name.iso -f iso file_name.txt
```

Create an EXT4 image:

```bash
ximg create -o img_file_name.img -f ext4 file_name.txt
```

Tip: You can rename files inside the image container using colon syntax:

```bash
ximg create -o img_file_name.img local_file.txt:documents/secret.txt
```

2. Extracting Images

To read and extract files from a compatible disk image:

```bash
ximg extract img_file_name.img -o output_dir_name
```

3. Using as a Python Library

You can also import XImg directly into your own Python projects:

```python
from ximg import XImg

# Create an image programmatically

XImg.create_image("img_file_name.img", [("file1.txt", "file2.txt")], format_type="fat32")

# Extract files programmatically

XImg.extract_image("img_file_name.img", output_dir="dir_name")
```

**Requirements**

Python 3.7+ (Fully compatible with Python 3.14).

Zero external dependencies (Pure Python core).

**License**
**Distributed under the MIT License. See LICENSE for more information.**
