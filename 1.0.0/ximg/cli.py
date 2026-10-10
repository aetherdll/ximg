import argparse
from ximg.core import XImg

def main():
    parser = argparse.ArgumentParser(description="XImg: Plugin-Based Multi-Format Disk Image Utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a disk or system image")
    create_parser.add_argument("-o", "--output", required=True, help="Output image file path")
    create_parser.add_argument("-f", "--format", default="fat12", help="Filesystem format type (e.g. fat12, fat32, iso, ext4)")
    create_parser.add_argument("files", nargs="+", help="Files to pack (Format: real_path or real_path:img_name)")

    # Extract command
    extract_parser = subparsers.add_parser("extract", help="Extract files from an image")
    extract_parser.add_argument("image", help="Path to the image file")
    extract_parser.add_argument("-o", "--output-dir", default="extracted_files", help="Target directory")

    args = parser.parse_args()

    if args.command == "create":
        file_list = []
        for file_arg in args.files:
            if ":" in file_arg:
                real_path, img_name = file_arg.split(":", 1)
            else:
                real_path, img_name = file_arg, file_arg
            file_list.append((real_path, img_name))
        
        XImg.create_image(args.output, file_list, format_type=args.format)

    elif args.command == "extract":
        XImg.extract_image(args.image, args.output_dir)

if __name__ == "__main__":
    main()