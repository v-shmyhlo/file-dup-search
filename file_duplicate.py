import os
import hashlib
import stat


def has_read_access(path):
    return bool(os.stat(path).st_mode & stat.S_IRGRP)


def compute_sha(path, buffer_size=65536):
    sha = hashlib.sha512()
    with open(path, 'rb') as f:
        while True:
            data = f.read(buffer_size)

            if not data:
                break

            sha.update(data)

        return sha.hexdigest()


def search_(dir, result):
    assert os.path.isdir(dir), '{} is not a directory'.format(dir)

    for path in [os.path.join(dir, path) for path in os.listdir(dir)]:
        # ignores files without read permissions
        if not has_read_access(path):
            continue

        if os.path.isdir(path):
            search_(path, result)
        else:
            sha = compute_sha(path)

            if sha in result:
                result[sha].append(path)
            else:
                result[sha] = [path]


def search(dir):
    result = {}
    search_(dir, result)

    return [result[k] for k in result if len(result[k]) > 1]


def main():
    print(*search('.'), sep='\n')


if __name__ == '__main__':
    main()
