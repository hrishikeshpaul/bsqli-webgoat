import pickle

def test():
   print( pickle.load( open('states/test.pkl', 'rb')))
    # pickle.dump('hello', open('states/test.pkl', 'wb'))