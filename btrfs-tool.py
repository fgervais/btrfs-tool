import btrfs


with btrfs.FileSystem('/home/fgervais/btrfs') as fs:
    for space in fs.space_info():
        print(space)
