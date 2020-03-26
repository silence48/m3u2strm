import logger
import pickle


#--------------------------------------------------
# Create class 'blue print'
#--------------------------------------------------

class PythonClass(object):
    
  def __init__(self, name='default', *args, **kw):             # initializer - automatically runs when class gets created
    self.name = name 
    print('extra args', args)
    print('extra kw', kw)
  def new_method(self):
    print('Hello', self.name)

#--------------------------------------------------
# Create instance(s) of class
#--------------------------------------------------

first_instance = PythonClass('Python', 1,2,3,4, keyword1='string', keyword2 =4 )

first_instance.new_method()
