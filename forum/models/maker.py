'''
Created on 19/12/2010

@author: Vaughan
'''
from base import *

class Maker(BaseModel):
    '''
    The maker of a promise - i.e Politician
    '''
    name = models.CharField(max_length=300)
    
    def __unicode__(self):
        return self.name