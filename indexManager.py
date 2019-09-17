import os
import json

class IndexManager:
    def __init__(self):
        self.index = json.load(open('index.txt', 'r'))
        self.home_path = os.getcwd()
        self.actual_cell = None

        self.name = None
        self.dir_ = None
        self.files = None
        self.tree = None

    def save(self):
        print("Saving index database")
        os.chdir(self.home_path) #Return to home path
        with open('index.txt', 'w') as output:
            json.dump(self.index, output)

    def define_folder(self, name, dir_, tree):
        self.name = name
        self.dir_ = dir_
        self.tree = tree
        self.files = []

    def create_folder(self, parent_folders):
        if self.actual_cell == None:
            self.actual_cell = self.index["folders"]

        cell = self.select_cell(self.actual_cell, parent_folders)
        cell.append({"name": self.name, "dir": self.dir_, "tree": self.tree, "files": self.files, "folders": []})

        self.actual_cell = cell

        #print(self.index)

    #TODO: Optimize and clean code
    def select_cell(self, starting_cell, parent_folders):
        cell = self.index["folders"]
        #If we are not in the wanted cell
        if parent_folders != []:
            for i, parent_folder in enumerate(parent_folders): #Go through the parent folders
                for folder_cell in cell: #Go trough the folders inside the folder we're searching
                    if folder_cell["name"] == parent_folder: #If the folder we are looking for is the atual one
                        #if i < (len(parent_folders) - 1):
                        cell = folder_cell['folders'] #Select folder
        #print(cell)
        return cell

index_manager = IndexManager()