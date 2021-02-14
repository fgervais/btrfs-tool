import btrfs


def subvolumes_inside(fs, parent_tree):
    min_key = btrfs.ctree.Key(parent_tree, btrfs.ctree.ROOT_REF_KEY, 0)
    max_key = btrfs.ctree.Key(parent_tree, btrfs.ctree.ROOT_REF_KEY + 1, 0) - 1
    for header, data in btrfs.ioctl.search_v2(fs.fd, 1, min_key, max_key):
        ref = btrfs.ctree.RootRef(header, data)
        path = (btrfs.ioctl.ino_lookup(fs.fd, ref.parent_tree, ref.dirid).name_bytes +
                ref.name).decode()
        yield ref.tree, path


def print_subvolumes_inside(fs, parent_tree=btrfs.ctree.FS_TREE_OBJECTID, parent_path=""):
    for tree, path in subvolumes_inside(fs, parent_tree):
        sub_path = "{}/{}".format(parent_path, path)
        print("ID {} parent {} path {}".format(tree, parent_tree, sub_path))
        print_subvolumes_inside(fs, tree, sub_path)


with btrfs.FileSystem('/home/fgervais/btrfs') as fs:
    # for subvol in fs.subvolumes():
    #     path = (btrfs.ioctl.ino_lookup(fs.fd, ref.parent_tree, ref.dirid).name_bytes +
    #             ref.name).decode()
    #     print(type(subvol))
    #     break

    print_subvolumes_inside(fs)
