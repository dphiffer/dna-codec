"""
#########################################################################
Author: Shalin Shah
Project: DNA Cloud
Graduate Mentor: Dixita Limbachya
Mentor: Prof. Manish K Gupta
Date: 28 July 2013
Website: www.guptalab.org/dnacloud
This module contains method which are not yet used but could be used in future to ensure parellel processing.
#########################################################################
"""

#This method can be used in future when a complete parellel process is available to encode and decode to and from DNA.At present thi file is not used.
def file_block(fp, number_of_blocks, block):
    '''
    A generator that splits a file into blocks and iterates
    over the lines of one of the blocks.
 
    '''
    assert 0 <= block and block < number_of_blocks
    assert 0 < number_of_blocks
 
    fp.seek(0,2)
    file_size = fp.tell()
 
    ini = file_size * block / number_of_blocks
    end = file_size * (1 + block) / number_of_blocks
 
    if ini <= 0:
        fp.seek(0)
    else:
        fp.seek(ini-1)
        fp.readline()
 
    while fp.tell() < end:
        yield fp.readline()

import os
import sys
#PATH = os.path.dirname(os.path.abspath(__file__))
PATH =  sys.path[0]
#print PATH , "chunks"
""" 
if __name__ == '__main__':
    fp = open(PATH + '/../icons/DNAicon.png','r')
    number_of_chunks = 3
    for chunk_number in range(number_of_chunks):
        print chunk_number, 100 * '='
        for line in file_block(fp, number_of_chunks, chunk_number):
         break
"""         
