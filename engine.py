import eel
import time

from indexManager import index_manager as idxman
# from indexator import indexator
from searcher import searcher

eel.init('pretty')

@eel.expose
def start_search(data):
    print("I am here")
    result = searcher.start_search([data])
    print(result[0], result[1])

@eel.expose
def search(data):
    print("I am also here")
    result = searcher.search([data])
    print(result[0], result[1])

eel.start('index.html', size=(800, 200))

#while True:
#    eel.sleep(0.5)