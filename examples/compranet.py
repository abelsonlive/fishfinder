from requests import Session
import xlrd
from fishfinder import FishFinder
import os 

class Compranet(FishFinder):
  
  def setup(self):
    self.session = Session()
    self.session.get('http://compranet-pa.funcionpublica.gob.mx/PAAASOP/buscador.jsp')
    self.post_url = 'http://compranet-pa.funcionpublica.gob.mx/PAAASOP/DownloadArchivo'

  def write_xls(self, data, filename):
    with open(filename, 'wb') as f:
      f.write(data)
  
  def search(self, query):
    """
    Submit a search query and return results
    """
    params = {
      'ocultarParam':'0',
      'ocultarDetalle':'1',
      'cveEntFederativa':'0',
      'cveDependencia':'0',
      'concepto': query,
      'valCompraDirPyme':'1000',
      'entidadesSelect':'0',
      'dependenciasSelect':'0'
    }
    r = self.session.post(self.post_url, params = params)
    return r.content

  def test(self, result, query):
    """
    With our results, test 
    whethere the query was legitimate.
    0 = No Results
    1 = Pass 
    2 = Needs More 
    """
    xls = xlrd.open_workbook(file_contents=result)
    sheet = xls.sheet_by_index(0)
    nrows = sheet.nrows 

    if nrows == 1:
      print "%s has no results" % query
      return 0

    elif nrows < 2501:
      filename = "data/%s.xls" % query
      print "Writing %s" % filename
      self.write_xls(result, filename)
      return 1 

    else:
      print "%s has too many results" % query
      return 2

if __name__ == '__main__':
  c = Compranet()
  c.run()
