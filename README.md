fishfinder
======
_Recursively search a service for all possibilities until the optimal set is found_

## About

Many sites like [North Carolina's Corprate Registry](https://www.secretary.state.nc.us/corporations/CSearch.aspx) allow you to search for records but limit the results to a set number (i.e. no more than 500).  Thus, in order to find the full list of results, you need to search through many combinations of letters and numbers. `fishfinder` provides an abstract framework for performing such tasks by generating all possible search queries of a certain length (say two letters), returning the results, and testing the results to determine which queries to add to the set. All searches are performed via `gevent` for concurrency. 

## Install
```
mkvirtualenv fishfinder
git clone https://github.com/bibliotech/fishfinder.git
pip install -e fishfinder/
```

## Usage 

`fishfinder` is agnostic to the methods you need to perform a search and test its results. To create your own fishfinder, simply inherit from the `FishFinder` class and overwrite the methods `setup`, `search`, and `test`. You can see a real-world example in `examples/compranet.py`.

```python
from fishfinder import FishFinder 

class MyFinder(FishFinder):
  def __init__(self):
    FishFinder.__init__(self, min_length=2, incl_numbers=False, exclude=['a'])

  def setup(self):
    # This will run before the search / test loop starts 
    pass

  
  def search(self, query):
    # this takes a query and returns something to test
    pass

  def test(self, result, query):
    """
    With our results, test 
    whether the query was legitimate.
    You also have access to the query in this method.

    This method should return one of three numbers:
    0 = No Reusults
    1 = Pass 
    2 = Needs More 
    """

if __name__ == '__main__':
  f = MyFinder()
  # set the number of concurrent 
  # workers in `run`
  f.run(num_workers=5)