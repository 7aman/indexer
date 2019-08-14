# indexer

indexer prepares a list of files to download from an index
```shell
python3 indexer.py URL
aria2c -i aria.list -c -j1 --file-allocation=none
    # -c : continue
    # -j : max concurrent downloads
    # --file-allocation=falloc for NTFS and ext4
    # --file-allocation=none for not pre-allocating
```