"""
Objects for reading a Hipparcos database file

based on: 
https://github.com/skyfielders/python-skyfield/blob/master/skyfield/data/hipparcos.py

Additionally allows for use of a local file

"""

import os
import gzip

# from:
# https://stackoverflow.com/questions/3703276/how-to-tell-if-a-file-is-gzip-compressed
# to determine if a file is gzip compressed
import binascii

def is_gz_file(filepath):
    """ determine if a file is gzipped using its first 2 bytes as a 
    magic number.

    A file that is like .tar.gz is not considered gzip compressed using
    this method.

    """
    with open(filepath, 'rb') as test_f:
        return binascii.hexlify(test_f.read(2)) == b'1f8b'

# use functions and constants from skyfield.data
import skyfield.data.hipparcos as sfhip

class HipparcosError(Exception):
    pass

class Hipparcos(object):

    def __init__( self,
                  filename = None,
                  url = sfhip.url ):

        self.filename = filename
        self.url = url
        
        # use a local file if it's specified
        if filename:
            try:
                # check if the file can be read
                with open(filename,'r') as f:
                    line = f.readline()
            except IOError:
                raise HipparcosError('Cannot access ' + filename + ' !')

    def parse( self, line ):
        """
        This method wraps skyfield.data.hipparcos.parse
        """
        return sfhip.parse( line )

    def open (self ):
        """
        Opens the chosen method of data access and returns a file-like
        object
        """
        # neither handle potenially gzipped files
        if self.filename:
            f = open( self.filename, 'r')
        else:
            from skyfield import api
            f = api.load.open( self.url )

        return f

    def load( self, match_function ):
        """
        similar to skyfield.data.hipparcos.load
        """
        if self.filename:
            with open( self.filename, 'r' ) as f:
                for line in f:
                    if match_function( line ):
                        yield self.parse( line )

        else:
            # WARNING: does not allow url pass through 
            return sfhip.load( match_function )            
            
    def get( self, which ):
        """
        This method modifies skyfield.data.hipparcos.get
        """
        # the skyfield version uses skyfields load command, so
        # it's modified here to use the local load method

        if isinstance(which, str):
            pattern = ('H|      %6s' % which).encode('ascii')
            for star in self.load(lambda line: line.startswith(pattern)):
                return star
        else:
            patterns = set(id.encode('ascii').rjust(6) for id in which)
            return list(self.load(lambda line: line[8:14] in patterns))
    
