import os
import multiprocessing as mp

from indexManager import index_manager

class Searcher:
    def __init__(self):
        self.index = index_manager.index["folders"]
        self.selection = self.index.copy() #Selection is full index at first

    def clean_input(self, raw_input):
        input_str = raw_input.lower()
        input_ = input_str.split('_')
        return input_

    def folder_search(self, branch, selection):
        cells = []

        for folder_cell in selection:
            folder_name = folder_cell["name"].lower()
            if folder_name == branch:
                cells.append(folder_cell)
            else:
                if len(branch) < len(folder_name):
                    branch_list = list(branch)
                    folder_name_list = list(folder_name)

                    #If input is equal to folder name but is not fisinished yet save
                    if branch_list == folder_name_list[0: len(branch_list)]:
                        cells.append(folder_cell)

            #TODO: Optimize
            if len(folder_cell["folders"]) > 0:
                # Search for folders with same name inside those folder
                # If sub-folders exist
                recurred_cells = self.folder_search(branch, folder_cell["folders"])
                cells += recurred_cells

        #Send cells up to now to continue program
        return cells

    def file_search(self, file_name, selection):
        cells = []

        for folder_cell in selection:
            for file_ in folder_cell["files"]:
                if len(file_name) == len(file_):
                    if file_name == file_.lower():
                        cells.append(('_'.join(folder_cell["tree"]) + '_' + file_, folder_cell["dir"]))
                elif len(file_name) < len(file_):
                    file_check_list = list(file_.lower())
                    file_name_list = list(file_name)

                    if file_name_list == file_check_list[0:len(file_name_list)]:
                        cells.append(('_'.join(folder_cell["tree"]) + '_' + file_, folder_cell["dir"]))

            #TODO: Optimize
            if len(folder_cell["folders"]) > 0:
                # Search for folders with same name inside those folder
                # If sub-folders exist
                recurred_cells = self.file_search(file_name, folder_cell["folders"])
                cells += recurred_cells

        return cells

    def search(self, raw_input):
        tree = self.clean_input(raw_input)

        if len(tree) > 1:
            for i, branch in enumerate(tree):
                if (i + 1) < len(tree):
                    folder_cells = self.folder_search(branch, self.selection)
                    self.selection = folder_cells
                else:
                    file_cells = self.file_search(branch, self.selection)
                    print(file_cells)

                    for file_cell in file_cells:
                        if file_cell[0] == raw_input:
                            print("File found: %s" % (file_cell[0]))
        else:
            file_cells = self.file_search(tree[1], self.selection)
            print(file_cells)

            for file_cell in file_cells:
                if file_cell[0] == raw_input:
                    print("File found: %s" % (file_cell[0]))

searcher = Searcher()
searcher.search("idxBranch_idxFile-0.docx")