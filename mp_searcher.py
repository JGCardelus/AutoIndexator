import os
import multiprocessing as mp

import time

#PERSONAL LIBS
import sorter
from indexManager import index_manager

class Item:
    def __init__(self, fname, dir_, confidence):
        self.fname = fname
        self.dir = dir_
        self.confidence = confidence

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

class Proc:
    def __init__(self, proc, conn):
        self.proc = proc
        self.conn = conn
        self.working = False

class P_Request:
    def __init__(self, is_alive, branch, selection):
        self.is_alive = is_alive
        self.branch = branch
        self.selection = selection

        self.pid = "q_request"

class P_Result:
    def __init__(self, cells, new_requests):
        self.cells = cells
        self.new_requests = new_requests

        self.pid = "q_result"

class Searcher:
    def __init__(self):
        self.index = index_manager.index["folders"]
        self.selection = self.index.copy() #Selection is full index at first

        self.search_tree = None
        self.cores = mp.cpu_count() - 1
        self.cores_avb = 3
        self.requests = []

        self.procs = self.def_procs(False)

    def clean_input(self, raw_input):
        input_str = raw_input.lower()
        input_ = input_str.split('_')
        return input_

    def def_procs(self, equal):
        procs = []

        #Create processes
        for i in range(self.cores_avb):
            parent_conn, child_conn = mp.Pipe()
            def_proc = mp.Process(target=self.spatial_reduction, args=(child_conn, equal, i))

            new_proc = Proc(def_proc, parent_conn)
            procs.append(new_proc)

            new_proc.proc.start()

        return procs

    def del_procs(self, procs):
        for proc in procs:
            proc.conn.send(P_Request(False, None, None))
            proc.conn.poll(None)
            proc.conn.close()
            proc.proc.join()

    def mp_request_handler(self, procs, branch, selection, equal):
        cells = []       
        requests = selection
        
        is_alive = True
        working_procs = []
        while is_alive:
            chunks, working_procs, requests = self.assign_chunks(procs, working_procs, branch, requests)

            for i, proc in enumerate(working_procs):
                #If there is not a response yet, skip proc
                if proc.conn.poll() == False:
                    continue

                p_result = proc.conn.recv()

                if len(p_result.cells) > 0:
                    cells += p_result.cells
                if len(p_result.new_requests) > 0:
                    requests += p_result.new_requests

                working_procs.pop(i)
                self.cores_avb += 1

            if len(chunks) > 0:
                for chunk in chunks:
                    requests += chunk
                chunks = []

            if len(working_procs) == 0 and len(requests) == 0:
                is_alive = False

        return cells
        
    def assign_chunks(self, procs, working_procs, branch, requests):
        if self.cores_avb > 0:
            chunks = self.divide_loads(requests)
            requests
            
            for proc in procs:
                if proc not in working_procs:
                    if len(chunks) > 0:
                        p_request = P_Request(True, branch, chunks[0])
                        proc.conn.send(p_request)

                        working_procs.append(proc)
                        chunks.pop(0)
                        self.cores_avb -= 1
                    else:
                        break

            return chunks, working_procs, []
        return [], working_procs, requests

    def spatial_reduction(self, conn, equal, num):
        is_alive = True
        while is_alive:
            conn.poll(None)

            p_request = conn.recv()
            is_alive = p_request.is_alive
            branch = p_request.branch
            selection = p_request.selection

            if selection != None:
                cells = []
                new_requests = []

                for folder_cell in selection:
                    folder_name = folder_cell["name"].lower()
                    confidence = self.name_similarity(branch.lower(), folder_name, equal)
                    if confidence > 0:
                        #print("(%s) Adding %s to cells" % (num, folder_name))
                        cells.append(folder_cell)
                    
                    if len(folder_cell["folders"]) > 0:
                       # print("(%s) Sub folders in %s" % (num, folder_name))
                        new_requests += folder_cell["folders"]

                p_result = P_Result(cells, new_requests)
                conn.send(p_result)
        
        conn.send(True)

    def divide_loads(self, selection):
        chunks = []

        is_even = True
        divisor = self.cores_avb
        if self.cores_avb % 2 != 0:
            divisor -= 1
            is_even = False

        if divisor == 0:
            chunks = [selection]
            return chunks

        divisions = len(selection) // divisor
        if divisions > 0:
            for i in range(0, len(selection), divisions):
                start = i
                end = i + divisions
                if i == 0:
                    chunks.append(selection[:end])
                elif (end + 1) == len(selection) and not is_even:
                    chunks.append(selection[start:])
                    break
                elif end == len(selection) and is_even:
                    chunks.append(selection[start:])
                    break
                else:
                    chunks.append(selection[start:end])
        else:
           for element in selection:
               chunks.append([element])

        return chunks

    def folder_search(self, procs, branch, selection, equal):
        selected_cells = self.mp_request_handler(procs, branch, selection, equal)
        cells = []
        
        for folder_cell in selected_cells:
            confidence = self.name_similarity(branch.lower(), folder_cell["name"].lower(), equal)
            new_folder = Item(folder_cell["name"], folder_cell["dir"], confidence)
            cells.append(new_folder)

        if len(cells) == 0:
            cells = None

        return cells

    def file_search(self, file_name, selection, equal):
        cells = []

        for folder_cell in selection:
            for file_ in folder_cell["files"]:
                confidence = self.name_similarity(file_name.lower(), file_.lower(), equal)
                
                if confidence > 0:
                    output_file_name = file_
                    if folder_cell["idx_rules"] == True:
                        output_file_name = folder_cell["name"] + '_' + file_
                    
                    new_file = Item(output_file_name, folder_cell["dir"], confidence)
                    cells.append(new_file)
            
            if len(folder_cell["folders"]) > 0:
                recurred_cells = self.file_search(file_name, folder_cell["folders"], equal)
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
        search_result = self.start_search(input_, equal)
        if search_result.files != None:
            return True
        else:
            return False

    def isdir(self, input_, dir_=None, equal=False):
        search_result = self.start_search(input_, equal)
        isdir_ = False
        if search_result.folders != None:
            if dir_ == None:
                isdir_ = True
            else:
                for folder in search_result.folders:
                    if folder.dir == dir_:
                        isdir_ = True

        return isdir_

    def start_search(self, tree, equal=False):
        self.selection = self.index.copy()
        self.search_tree = []
        self.requests = []

        result = self.search(tree, equal)
        return result

    def search(self, tree, equal=False):
        if self.search_tree != []:
            tree.insert(0, self.search_tree[-1])
            self.search_tree.pop()

        for i, branch in enumerate(tree):
            if (i + 1) < len(tree):
                #self.requests.append([branch, self.selection, equal])
                folder_cells = self.mp_request_handler(self.procs, branch, self.selection, equal)
                self.selection = folder_cells

        self.search_tree += tree

        folders = self.folder_search(self.procs, tree[-1], self.selection, equal)
        files = self.file_search(tree[-1], self.selection, equal)

        result = Search_Result(files, folders)

        return result

if __name__ == '__main__':
    searcher = Searcher()
    start = time.time()
    result = searcher.start_search(["data_set_pages.txt"])
    result.print_()
    end = time.time() - start
    print(end)
    searcher.del_procs(searcher.procs)