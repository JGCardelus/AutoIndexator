import libs
import cleaner
import os

from indexManager import index_manager

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

            #Define branch in index manager
            index_manager.define_folder(root_name, root)

            #Search directory for folders and files
            for root, branches, files in os.walk('.'):
                #Change file names in root folder
                for file_name in files:
                    self.rename_file([root_name], file_name)

                #Save branch
                index_manager.create_folder([])

                #Check that the directory name is not in the exlude parameter
                for branch in branches:
                    if branch not in self.exclude and branch != None:
                        #Directory must be included in reindexation
                        self.search_directory([root_name, branch])

            #Save index
            index_manager.save()

    def search_directory(self, tree):
        #Go to the folder
        path = self.root + '\\' + '\\'.join(tree[1:]) #Since tree has root_name at the begining, exclude as it is also contained in self.root
        libs.go(path)

        #Define branch in index manager
        index_manager.define_folder(tree[len(tree) - 1], path)

        #Search branch
        for root, branches, files in os.walk('.'):
            #Rename files
            for file_name in files:
                self.rename_file(tree, file_name)

            #Save brach in index manager
            #parent_folders = []
            #If last cell == last folder indexed, no need to find location again
            #if index_manager.actual_cell["name"] != tree[len(tree) - 2]: 
                #If is not, search for folder again
            parent_folders = tree[:len(tree) - 1]

            index_manager.create_folder(parent_folders)

            #If there are branches in the actual branch apply transformation
            for branch in branches:
                if branch not in self.exclude:
                    #Add branch name to the tree
                    updated_tree = tree.copy()
                    updated_tree.append(branch)
                    self.search_directory(updated_tree)

    def rename_file(self, raw_tree, raw_file_name):
        #File might be already indexed
        raw_chunks = raw_file_name.split('_')
        original_file_name = raw_chunks[len(raw_chunks) - 1] #prefix_prefix_name.extension
        
        #Clean tree names
        tree = cleaner.clean_tree(raw_tree, self.remove_plural)
        file_name = cleaner.clean_name(raw_file_name)
        prefix = '_'.join(tree)
        #If file is not indexed, this is name to savee
        name_ = prefix + '_' + file_name

        #If file is already indexed, this is target name
        target_name = prefix + '_' + original_file_name
        
        if target_name != raw_file_name:
            #It hasn't been indexed
            os.rename(raw_file_name, name_)
            #Save name in index_manager
            index_manager.files.append(name_)
        else:
            #It has been indexed
            #Save name in index_manager
            index_manager.files.append(raw_file_name)

home_dir = "C:\\Users\\jgcar\\Desktop\\idxTest"
indexator = DirectoryIndexator(home_dir)
indexator.start()