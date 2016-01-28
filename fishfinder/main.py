import gevent.monkey
gevent.monkey.patch_all()
import gevent
from gevent.queue import Queue

from itertools import product
import random 
import string


class FishFinder:
  def __init__(self, min_length=2, incl_nums=False, exclude = [], randomize=False):
    
    # parameters for search generation
    self.min_length = min_length 
    self.incl_nums = incl_nums
    self.randomize = randomize

    # Initialized list of good 
    # search terms and exclusion set.   
    self.exclude = set(list(exclude))
    self.to_search = []
    self.search_terms = []

    # generate possible characters 
    self.characters = list(set(string.letters.lower()))
    if self.incl_nums:
      self.characters += [str(x) for x in range(0, 10)]

  def setup(self):
    """
    method to run before search/test loop
    """
    return True

  def search(self, query):
    """
    Define how to perform the search 
    and return the content
    """
    return True

  def test(self, result, query):
    """
    Define how to test the search results 
    and return:
    0 - "No Results"
    1 - "Passed"
    2 - "Too many Results"
    """
    return True

  def _gen_queries(self):
    """
    Create search strings. This function 
    will be influence by what's in our 
    exclusion set and our minimum min_length
    of numbers 
    """
    if len(self.to_search) == 0:
      possibilities = product(*[self.characters for _ in range(0, self.min_length)])
    else:
      possibilities = product(self.to_search, self.characters)

    queries = ("".join(q) for q in possibilities if "".join(q) not in self.exclude)

    if self.randomize:
      return random.shuffle(list(queries))

    else:
      return queries

  def run(self, num_workers=10):
    # recursively generate queries and 
    # test them, keeping track of ones 
    # that have already passed so we don't 
    # replicate labor

    # setup any global configs
    self.setup()
    
    # Redursively search until all tests 
    # pass
    while True:
      
      # setup Queue for this iteration
      tasks = Queue()
      
      # list of tests for this iteration
      tests = []

      # generate queries for this iteration
      queries = self._gen_queries()

      # update list of terms to search
      self.to_search = []
      
      # put the queries in the queue
      def boss():
        # generate queries
        for q in queries:
          
          # put it in the queue
          tasks.put_nowait(q)

      # retrieve the queries 
      def worker():
        while not tasks.empty():
          q = tasks.get()
          result = self.search(q)
          test = self.test(result, q)
          
          if test == 0:
            tests.append(True)

          elif test == 1:
            self.search_terms.append(q)
            tests.append(True)

          elif test == 2:
            self.to_search.append(q)
            tests.append(False)

          gevent.sleep(0.001)


      def run_step():
        gevent.spawn(boss).join()
        gevent.joinall([gevent.spawn(worker) for w in xrange(num_workers)])
        
      # run this step.
      run_step()
      
      # check if all tests pass
      if all(tests):
        break

    return self.search_terms
