from carg_io.implementations import MyContainer
import argparse
import sys
from pathlib import Path

# parser = argparse.ArgumentParser()
# parser.add_argument("file")

# args = parser.parse_args()

# target_file = Path(args.file)
target_file = sys.argv[1]

# if not target_file.exists():
#     print("The target file doesn't exist")
#     raise SystemExit(1)

print(target_file)
target_file = target_file.replace('\\\\', '\\')
cont = MyContainer.load(target_file)
cont.file_ui()

# python "C:\opener.py" file %1