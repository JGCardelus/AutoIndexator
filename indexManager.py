import os
import json
import libs

#PERSONAL LIBS
import sorter

class IndexManager:
    def __init__(self):
        self.index = json.load(open('index.txt', 'r'))
        self.home_path = os.getcwd()
        self.actual_cell = None

        self.name = None
        self.dir_ = None
        self.files = None
        self.exclude = None
        self.idx_rules = None

        self.last_tree = None

    def reset(self):
        libs.go(self.home_path)

        self.actual_cell = None

        self.name = None
        self.dir_ = None
        self.files = None
        self.exclude = None
        self.idx_rules = None

        self.last_tree = None
    
    #TODO: Optimize
    def save(self):
        print("Saving index database")
        libs.go(self.home_path) #Return to home path
        with open('index.txt', 'w') as output:
            json.dump(self.index, output)

    def define_folder(self, name, dir_, idx_rules):
        self.name = name
        self.dir_ = dir_
        self.files = []
        self.idx_rules = idx_rules

    def create_folder(self, parent_branches, exclude = None):
        cell = self.get_parent_cell(parent_branches)

        new_cell = {"name": self.name, "dir": self.dir_, "idx_rules": self.idx_rules, "files": self.files, "folders": []}
        if exclude != None:
            new_cell["exclude"] = exclude

        cell["folders"].append(new_cell)
        
        self.last_tree = parent_branches
        self.actual_cell = cell

    def add_file(self, new_file):
        self.files.append(new_file)

    def get_parent_cell(self, parent_branches):
        #If we are starting indexation, select the whole db as the actual cell
        if self.actual_cell == None or self.last_tree == None:
            self.actual_cell = self.index
            self.last_tree = parent_branches

        cell = self.actual_cell
        if len(self.last_tree) != len(parent_branches):
            #Search new cell
            cell = self.select_cell(self.actual_cell, parent_branches)

        return cell

    def hierarchical_search(self, cell, branches):
        for i, branch in enumerate(branches): #Go through the parent folders
            for folder in cell: #Go trough the folders inside the folder we're searching
                if folder["name"] == branch: #If the folder we are looking for is the atual one
                    if (1 + i) == len(branches):
                        cell = folder
                    else:
                        cell = folder["folders"]
                    break
        
        return cell

    def fwd_step_search(self, cell, branch):
        for folder in cell["folders"]: #Go trough the folders inside the folder we're searching
            if folder["name"] == branch: #If the folder we are looking for is the atual one
                cell = folder
                break 
        
        return cell

    def select_cell(self, starting_cell, parent_branches):
        cell = starting_cell
        if len(parent_branches) > len(self.last_tree):
            cell = self.fwd_step_search(cell, parent_branches[-1])
        elif len(parent_branches) < len(self.last_tree):
            #The cell we are looking for is outside the cell we are in, so search from the beginning
            cell = self.index["folders"]
            cell = self.hierarchical_search(cell, parent_branches)

        return cell

    def delete_folder(self, branches):
        cell = self.index["folders"]
        if len(branches) > 1:
            cell = self.hierarchical_search(cell, branches[:-1])["folders"]
        for i, folder in enumerate(cell):
            if folder["name"] == branches[-1]:
                cell.pop(i)
                break

    def delete_file(self, branches, file_to_delete):
        cell = self.hierarchical_search(self.index["folders"], branches)["files"]
        for i, file_name in enumerate(cell):
            if file_name == file_to_delete:
                cell.pop(i)
                break

index_manager = IndexManager()