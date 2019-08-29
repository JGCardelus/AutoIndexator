import libs
import cleaner
import os

class DirectoryIndexator:
    def __init__(self, root, remove_plural=True, exclude=[]):
        self.root = root
        self.remove_plural = remove_plural
        self.exclude = exclude

    def start(self):
        #Check that root exists
        if os.path.isdir(self.root):
            root = self.root
            #Go to directory
            libs.go(root)

            #Get root name
            root_path = root.split('\\')
            root_name = root_path[len(root_path) - 1]

            #Search directory for folders and files
            for root, branches, files in os.walk('.'):
                #Change file names in root folder
                for file_name in files:
                    self.rename_file([root_name], file_name)

                #Check that the directory name is not in the exlude parameter
                for branch in branches:
                    if branch not in self.exclude and branch != None:
                        #Directory must be included in reindexation
                        self.search_directory([root_name, branch])

    def search_directory(self, tree):
        #Go to the folder
        path = self.root + '\\' + '\\'.join(tree[1:]) #Since tree has root_name at the begining, exclude as it is also contained in self.root
        libs.go(path)

        #Search branch
        for root, branches, files in os.walk('.'):
            #Rename files
            for file_name in files:
                self.rename_file(tree, file_name)

            #If there are branches in the actual branch apply transformation
            for branch in branches:
                if branch not in self.exclude:
                    #Add branch name to the tree
                    updated_tree = tree.copy()
                    updated_tree.append(branch)
                    self.search_directory(updated_tree)

    def rename_file(self, raw_tree, raw_file_name):
        #Clean tree names
        tree = cleaner.clean_tree(raw_tree, self.remove_plural)
        file_name = cleaner.clean_name(raw_file_name)
        prefix = '_'.join(tree)
        name_ = prefix + '_' + file_name
        
        os.rename(raw_file_name, name_)

