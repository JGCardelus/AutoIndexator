from searcher import Searcher
import multiprocessing as mp

class Test:
    def lol(self):
        q = mp.Queue()
        b = mp.Process(target=self.hello, args=(5, q))
        b.start()
        print(q.get())
        
        print(b.is_alive())
        b.Process.target = self.hello
        b.args((5, q))
        b.run()
        print(q.get())

    def hello(self, a, q):
        b = []
        for i in range(5):
            b.append({"name": i * a})
        q.put(b)

if __name__ == '__main__':
    searcher = Searcher()
    searcher.mp_request_handler("idxBranch7", searcher.index.copy(), False)
    #searcher.cores_avb = 0
    #print(searcher.divide_loads([0,1,2,3,4,7,8,9,10,11,12]))