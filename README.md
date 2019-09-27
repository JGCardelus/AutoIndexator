# DOYLE - File/folder search engine & auto indexator
This program is able to find files/folders that the program has saved in a database (and it should do it faster than the windows search feature). It can also index files following a set of rules that make it easier to find them and search for them: contaningFolder_camelCasedFileName.extension.

## Upcoming features
The program will feature a GUI that will make the selection of folders to indexate and the searching of files/folders very easy. The search algorithm will include multicore functionality for faster search speeds.

## TODO:
- [ ] Migrate everything to a new project
- [ ] Optimize index manager, there is redundant code
- [ ] Add file type removal to auto indexator
- [ ] Specify rules for folders in cleaner and apply them
- [ ] Optimize searcher
- [ ] Add multiprocessing to searcher
- [ ] Create program that watches the creation of new files and automatically renames them
- [ ] Create GUI