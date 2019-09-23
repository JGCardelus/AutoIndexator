import os
import multiprocessing as mp

from indexManager import index_manager

class Search_Result:
    def __init__(self, files, folders):
        self.files = files
        self.folders = folders

    def print_all(self):
        print("Found files:")
        print(self.files)
        print("Found folders:")
        print(self.folders)

class Searcher:
    def __init__(self):
        self.index = index_manager.index["folders"]
        self.selection = self.index.copy() #Selection is full index at first

    def clean_input(self, raw_input):
        input_str = raw_input.lower()
        input_ = input_str.split('_')
        return input_

    def spatial_reduction(self, branch, selection):
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
                recurred_cells = self.spatial_reduction(branch, folder_cell["folders"])
                cells += recurred_cells

        #Send cells up to now to continue program
        return cells

    def folder_search(self, branch, selection):
        selection_cells = self.spatial_reduction(branch, selection)
        cells = []
        
        for folder_cell in selection_cells:
            cells.append([folder_cell["name"], folder_cell["dir"]])

        if len(cells) == 0:
            cells = None

        return cells

    def file_search(self, file_name, selection):
        cells = []

        for folder_cell in selection:
            for file_ in folder_cell["files"]:
                if len(file_name) == len(file_):
                    if file_name == file_.lower():
                        cells.append((folder_cell["name"] + '_' + file_, folder_cell["dir"]))
                elif len(file_name) < len(file_):
                    file_check_list = list(file_.lower())
                    file_name_list = list(file_name)

                    if file_name_list == file_check_list[0:len(file_name_list)]:
                        cells.append(folder_cell["name"] + '_' + file_, folder_cell["dir"])

            #TODO: Optimize
            if len(folder_cell["folders"]) > 0:
                # Search for folders with same name inside those folder
                # If sub-folders exist
                recurred_cells = self.file_search(file_name, folder_cell["folders"])
                if recurred_cells != None:
                    cells.append(recurred_cells)

        if len(cells) == 0:
            cells = None

        return cells

    def isfile(self, input_):
        search_result = self.search(input_)
        if search_result.files != None:
            return True
        else:
            return False

    def isdir(self, input_):
        search_result = self.search(input_)
        if search_result.folders != None:
            return True
        else:
            return False

    def search(self, input_):
        self.selection = self.index.copy()
        tree = self.clean_input(input_)
        result = None

        if len(tree) > 1:
            for i, branch in enumerate(tree):
                if (i + 1) < len(tree):
                    folder_cells = self.spatial_reduction(branch, self.selection)
                    self.selection = folder_cells
                else:
                    folders = self.folder_search(branch, self.selection)
                    files = self.file_search(branch, self.selection)
                    
                    result = Search_Result(files, folders)
        else:
            folders = self.folder_search(tree[0], self.selection)
            files = self.file_search(tree[0], self.selection)

            result = Search_Result(files, folders)

        return result

searcher = Searcher()