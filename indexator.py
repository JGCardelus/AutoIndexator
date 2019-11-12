import libs
import cleaner
import os

#PERSONAL LIBS
from indexManager import index_manager as idxman
from searcher import searcher

class DirectoryIndexator:
    def __init__(self, root, idx_rules=False, remove_plural=True, exclude=[]):
        self.root = root
        self.remove_plural = remove_plural
        self.exclude = exclude

        self.idx_rules = idx_rules

    def start(self):
        root_name = self.init_sequence()
        if root_name == None:
            print("Error in init_sequence.")
            return

        self.recursive_directory_idx([root_name], False)

        idxman.save()

    def start_reindexation(self):
        root_name = self.init_sequence()
        self.idx_rules = True

        if root_name == None:
            print("Error in init_sequence.")
            return

        self.recursive_directory_idx([root_name], True)

        idxman.save()

    def init_sequence(self):
        #Check that root exists
        if not os.path.isdir(self.root):
            print("Root path does not exist")
            return

        #Go to directory
        root = self.root
        libs.go(root)

        #Get root name
        root_path = root.split('\\')
        root_name = root_path[len(root_path) - 1]

        if searcher.isdir([root_name], self.root, True):
            print("Folder already indexed.")
            return

        idxman.reset()

        return root_name

    def recursive_directory_idx(self, tree, reindex):
        self.define_folder(tree)

        #Search directory for folders and files
        for root, branches, files in os.walk('.'):
            #Change file names in root folder
            for file_name in files:
                if reindex:
                    self.reindex_file(tree, file_name)
                else:
                    self.save_file(tree, file_name)

            self.create_folder(tree)

            #Check that the directory name is not in the exlude parameter
            for branch in branches:
                if branch not in self.exclude and branch != None:
                    #Add branch name to the tree
                    updated_tree = tree.copy()
                    updated_tree.append(branch)
                    self.recursive_directory_idx(updated_tree, reindex)

    def define_folder(self, tree):
        path = self.root
        if len(tree) > 1:
            path = self.root + '\\' + '\\'.join(tree[1:]) #Since tree has root_name at the begining, exclude as it is also contained in self.root
        
        libs.go(path)

        #Define branch in index manager
        idxman.define_folder(tree[-1], path, self.idx_rules)

    def create_folder(self, tree):
        #Save branch
        if len(tree) == 1:
            idxman.create_folder([], self.exclude)
        else:
            parent_folders = tree[:-1]
            idxman.create_folder(parent_folders)

    def save_file(self, raw_tree, raw_file_name):
        file_name = raw_file_name

        if self.idx_rules:
            file_name = self.rename_file(raw_tree, raw_file_name)

        idxman.add_file(file_name)

    def rename_file(self, raw_tree, raw_file_name):
        #File might be already indexed
        raw_chunks = raw_file_name.split('_')
        original_file_name = raw_chunks[-1] #prefix_prefix_name.extension
        
        #Clean tree names
        prefix = cleaner.clean_tree(raw_tree, self.remove_plural)
        file_name = cleaner.clean_name(raw_file_name)
        #If file is not indexed, this is name to save
        name_ = prefix + '_' + file_name

        #If file is already indexed, this is target name
        target_name = prefix + '_' + original_file_name
        
        if target_name != raw_file_name:
            #It hasn't been indexed
            os.rename(raw_file_name, name_)
            #Save name in idxman
            return file_name
        else:
            return original_file_name

    def reindex_file(self, raw_tree, raw_file_name):
        raw_chunks = raw_file_name.split('_')
        file_name = raw_chunks[-1] #prefix_prefix_name.extension
        
        #Clean tree names
        prefix = cleaner.clean_tree(raw_tree, self.remove_plural)
        #If file is not indexed, this is name to save
        name_ = prefix + '_' + file_name

         #It hasn't been indexed
        os.rename(raw_file_name, name_)
        #Save name in idxman
        idxman.add_file(file_name)


home_dir = "C:\\Users\\jgcar\\OneDrive - Universidad Pontificia Comillas"
# home_dir_2 = "C:\\Users\\jgcar\\Desktop\\Coding"
indexator = DirectoryIndexator(home_dir, exclude=["Notebooks", "Colegio"], idx_rules=True, remove_plural=False)
indexator.start_reindexation()
# indexator = DirectoryIndexator(home_dir_2, True)
# indexator.start()