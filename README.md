# indexer

## Dependencies:
- python 3.6+
- aria2

## Clone and Usage

```shell
git clone https://github.com/7aman/indexer
cd indexer

# indexer get a index URL and prepares a text file (aria.list) of files to download by aria2
python3 indexer.py URL

#
aria2c -i aria.list -c -j1 --file-allocation=none
    # -c : continue
    # -j : max concurrent downloads
    # --file-allocation=falloc for NTFS and ext4
    # --file-allocation=none for not pre-allocating
```
