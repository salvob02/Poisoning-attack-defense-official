import zipfile
import os

def find_dirs(zip_path):
    """
    Given the path to a ZIP file, find the terminal directory (last level in the hierarchy)
    that contains (case-insensitive) 'train','test' and 'val'.

    If exactly one directory is found for 'train' and one for 'test',
    the function returns a tuple: (train_directory, test_directory).

    If there is more than one or none for either case, an exception is raised.
    """
    train_dirs = set()
    test_dirs = set()
    check_val_root = False
    check_test_root = False

    with zipfile.ZipFile(zip_path, 'r') as z:
        for item in z.namelist():
            # if the element ends with '/' is a finaally director. so it is removed the final character.
            if item.endswith('/'):
                directory = item.rstrip('/')
            else:
                # If it's a file, get the directory in where it is.
                directory = os.path.dirname(item)

            if item.startswith("__MACOSX"):
                continue
            
            # if it doesn't exist a directory (file in root) we skip it.
            if not directory:
                continue

            # I get the last component of the directory; for example, dataset/train returns only train.
            terminal_folder = os.path.basename(directory).lower()

            # Verify if terminal_folder contains 'train' or 'test' or 'val'
            if 'train' in terminal_folder:
                train_dirs.add(directory)
                continue
            if 'test' in terminal_folder:
                test_dirs.add(directory)
                check_test_root = True
                continue
            if 'val' in terminal_folder:
                check_val_root = True
                valid_dirs = set()
                valid_dirs.add(directory)

    # Verify that there is exactly one directory for each pattern.
    if len(train_dirs) != 1:
        raise ValueError(f"Expected exactly one folder containing 'train', found: {list(train_dirs)}")
    if check_test_root and len(test_dirs) > 1:
        raise ValueError(f"Expected max one folder containing 'test', found: {list(test_dirs)}")
    if check_val_root and len(valid_dirs) > 1:
        raise ValueError(f"Expected exactly zero or one folder containing 'val', found: {list(valid_dirs)}")
    

    # It Returns the directory
    if check_val_root and check_test_root:
        return list(train_dirs)[0], list(valid_dirs)[0], list(test_dirs)[0]
    
    if check_val_root and not check_test_root:
        return list(train_dirs)[0], list(valid_dirs)[0], []
    
    if not check_val_root and check_test_root:
        return list(train_dirs)[0], [], list(test_dirs)[0]


if __name__ == "__main__":
    pass






