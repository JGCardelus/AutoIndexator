import os
import multiprocessing as mp
import time

#PERSONAL LIBS
import sorter
from indexManager import index_manager as idxman

class Item:
    def __init__(self, fname, dir_, confidence):
        self.fname = fname
        self.dir = dir_
        self.confidence = confidence

        self.search_tree = None

    def print_(self):
        print(self.fname, self.dir, self.confidence)

class Search_Result:
    def __init__(self, files, folders):
        self.files = files
        self.folders = folders

    def print_(self):
        if self.files != None:
            print("Found files:")
            for file_ in self.files:
                file_.print_()
        else:
            print("Found files: None")
        if self.folders != None:
            print("Found folders:")
            for folder in self.folders:
                folder.print_()
        else:
            print("Found folders: None")

class Searcher:
    def __init__(self):
        self.index = idxman.index["folders"]
        self.selection = self.index.copy() #Selection is full index at first

    def clean_input(self, raw_input):
        input_str = raw_input.lower()
        input_ = input_str.split('_')
        return input_

    def spatial_reduction(self, branch, selection, equal=False):
        cells = []

        for folder_cell in selection:
            folder_name = folder_cell["name"].lower()
            confidence = self.name_similarity(branch.lower(), folder_name, equal)
            if confidence > 0:
                cells.append(folder_cell)
            
            if len(folder_cell["folders"]) > 0:
                recurred_cells = self.spatial_reduction(branch, folder_cell["folders"])
                cells += recurred_cells

        #Send cells up to now to continue program
        return cells

    def folder_search(self, branch, selection, equal=False):
        selected_cells = self.spatial_reduction(branch, selection, equal)
        cells = []
        
        for folder_cell in selected_cells:
            confidence = self.name_similarity(branch.lower(), folder_cell["name"].lower(), equal)
            new_folder = [folder_cell["name"], folder_cell["dir"], confidence, None]
            if (len(folder_cell["folders"]) > 0):
                new_folder[3] = folder_cell["folders"]
            
            cells.append(new_folder)

        if len(cells) == 0:
            cells = None

        return cells

    def file_search(self, file_name, selection, equal=False):
        cells = []

        for folder_cell in selection:
            for file_ in folder_cell["files"]:
                confidence = self.name_similarity(file_name.lower(), file_.lower(), equal)
                
                if confidence > 0:
                    output_file_name = file_
                    if folder_cell["idx_rules"] == True:
                        output_file_name = folder_cell["name"] + '_' + file_
                    
                    new_file = [output_file_name, folder_cell["dir"], confidence]
                    cells.append(new_file)
            
            if len(folder_cell["folders"]) > 0:
                recurred_cells = self.file_search(file_name, folder_cell["folders"])
                if recurred_cells != None:
                    cells += recurred_cells

        if len(cells) == 0:
            cells = None

        return cells

    def name_similarity(self, a, b, equal):
        confidence = 0

        if a == b:
            confidence = 1
        elif not equal and len(a) < len(b):
            a = list(a)
            b = list(b)

            if a == b[:len(a)]:
                confidence = round(len(a) / len(b), 2)

        return confidence

    def isfile(self, input_, equal=False):
        files, folders = self.start_search(input_, equal)
        if files != None:
            return True
        else:
            return False

    def isdir(self, input_, dir_=None, equal=False):
        files, folders = self.start_search(input_, equal)
        isdir_ = False
        if folders != None:
            if dir_ == None:
                isdir_ = True
            else:
                for folder in folders:
                    if folder[1] == dir_:
                        isdir_ = True

        return isdir_

    def start_search(self, tree, equal=False):
        self.selection = self.index.copy()
        self.search_tree = []

        files, folders = self.search(tree, equal)
        return files, folders

    def search(self, tree, equal=False):
        if self.search_tree != []:
            tree.insert(0, self.search_tree[-1])
            self.search_tree.pop()

        for i, branch in enumerate(tree):
            if (i + 1) < len(tree):
                folder_cells = self.spatial_reduction(branch, self.selection, equal)
                self.selection = folder_cells

        self.search_tree += tree

        folders = self.folder_search(tree[-1], self.selection, equal)
        files = self.file_search(tree[-1], self.selection, equal)

        return files, folders

searcher = Searcher()
# start = time.time()
result1 = searcher.start_search(["idxBranch3"])
# result2 = searcher.start_search(["Películas"])
# result3 = searcher.start_search(["index.html"])

print(result1[0], result1[1])
# print(result2[0], result2[1])
# print(result3[0], result3[1])

# end = time.time() - start
# print(end)