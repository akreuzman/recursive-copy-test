# recursive-copy-test

Testing a few different methods to copy data recursively from one directory to another, both locally and uploading to the lab defiant server. Attempting to shorten upload time in infant post processing program.

Guessing that the upload time is largely bottlenecked by the server upload speed, but I want to check if parallel processing can reduce upload time in any meaningful way.

Trying:
1. sequential `copy` calls.
2. `copy_tree`
3. `multiprocessing.Pool`
4. `concurrent.futures`


