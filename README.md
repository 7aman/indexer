# indexer

## Dependencies:
- python 3.6+
- aria2

## Clone and Usage

```shell
git clone https://github.com/7aman/indexer
cd indexer

# indexer gets an index URL and creates a list of files (aria.list) from that index
python3 indexer.py URL

#
aria2c -i aria.list -c -j1 --file-allocation=none
    # -c : continue
    # -j : max concurrent downloads
    # --file-allocation=falloc for NTFS and ext4
    # --file-allocation=none for not pre-allocating
```
