import libs
import os

class DirectoryIndexator:
    def __init__(self, root, remove_plural=True, exclude=None):
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
                    if branch not in self.exclude:
                        #Directory must be included in reindexation
                        self.search_directory([root_name, branch])

    def search_directory(self, tree):
        #Go to the folder
        path = self.root + '\\' + '\\'.join(tree[1:]) #Since tree has root_name at the beginign, exclude as it is also contained in self.root
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
                    updated_tree = tree.append(branch)
                    self.search_directory(updated_tree)

    def clean_tree(self, raw_tree):
        tree = []

        for branch in raw_tree:
            branch.lower()
            if self.remove_plural and branch[len(branch) - 1] == 's':
                #If the last letter of the branch is an 's', remove it
                branch = list(branch) #Convert to list
                branch.pop(len(branch) - 1) #Remove s
                branch = "".join(branch) #Reconvert to string
            tree.append(branch)

        return tree

    def clean_file_name(self, raw_file_name):
        file_name = ''
        #Remove extension
        raw_file_name = raw_file_name.split('.')
        extension = raw_file_name[1]
        raw_file_name = raw_file_name[0]

        #Clean name
        #Replace '_'
        list_chars = list(raw_file_name)
        for i in range(len(list_chars)):
            if list_chars[i] == chr(95):
                list_chars[i] = ' '

        raw_file_name = "".join(list_chars)

        #Convert to camel casing
        raw_file_name_chunks = raw_file_name.split(' ')
        for i, file_name_chunk in enumerate(raw_file_name_chunks):
            if i == 0:
                file_name += file_name_chunk.lower()
            else:
                if file_name[len(file_name) - 1] == '-':
                    #If last chunk ends with '-' next letter must be lower
                    #0-hello.txt
                    file_name += file_name_chunk.lower()
                else:
                    #If last char is not and '-' and file_name_chunk len == 1 then prefix '-'
                    if len(file_name_chunk) == 1:
                        #somethingHuge-1.txt
                        file_name += '-'

                    #If last chunk ends with no '-' next letter must start with upper
                    #somethingHuge.txt
                    file_name += file_name_chunk[0].upper() + file_name_chunk[1:].lower()

            if len(file_name_chunk) == 1 and (i + 1) != len(raw_file_name_chunks):
                #If chunk is a one letter character and it is not at the end
                file_name += '-'

        #Add extension
        file_name += '.' + extension

        return file_name

    def rename_file(self, raw_tree, raw_file_name):
        #Clean tree names
        tree = self.clean_tree(raw_tree)
        file_name = self.clean_file_name(raw_file_name)
        prefix = '_'.join(tree)
        name_ = prefix + '_' + file_name
        
        os.rename(raw_file_name, name_)
