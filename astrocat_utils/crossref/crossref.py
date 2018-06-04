"""
cross reference utility for catalogs

based on the tables found here:
http://cdsarc.u-strasbg.fr/viz-bin/Cat?IV/27A
"""

import os,sys
import numpy as np
from astropy import units as u
from astropy.coordinates import Angle

def int_or_none( x ):
    return int(x) if len(x.strip())>0 else None
            
class CrossRefError(Exception):
    pass

class CrossRef(object):
    """
    Cross-Reference class
    loads a series of cross reference tables on 
    initialization and can return cross-refernce
    info.
    """

    cross_ref_dir = None

    # names of the files
    table_names = { 'catalog' : 'catalog.dat',
                    'table1' : 'table1.dat',
                    'table2' : 'table2.dat',
                    'table3' : 'table3.dat',
                    'refs' : 'refs.dat' }

    # dictionary holding file objects to each table
    table_f = {}

    def __init__( self, cross_ref_dir ):
        """
        Input must be a directory containing the cross reference tables:
        catalog.dat
        table1.dat
        table2.dat
        table3.dat
        refs.dat
        """
        
        self.cross_ref_dir = cross_ref_dir

        # generate full paths to the needed tables and make sure
        # they exist
        for k,v in self.table_names.items():
            _fname = os.path.sep.join( [ cross_ref_dir, v ] )
            try:
                self.table_f[ k ] = open( _fname, 'r' )
            except IOError:
                raise CrossRefError('File ' +
                                    _fname +
                                    ' could not be opened.')
                
    def get_proper_name( self, proper_name ):
        """
        given a proper name, return the data from table3.dat
        case sensitive
        """
        # reset file pointer to beginning in case it's not there 
        self.table_f[ 'table3' ].seek(0)

        # there may be more than one match, return list of all
        r = [] 

        for line in self.table_f[ 'table3' ]:
            # the same proper name may appear more than once
            if proper_name in line[21:76]:
                r.append( self.parse_table3( line ) )

        return r

    def parse_catalog( self, line ):
        """
        parse a line from the catalog.dat file
        """
        ra = Angle( [ int( line[38:40] ),
                      int( line[40:42] ),
                      float( line[42:47] ) ],
                    unit = 'hourangle' )

        de = Angle( [ int( line[48:51] ),
                      int( line[51:53] ),
                      float( line[53:57] ) ],
                    unit = u.deg )
                                 
        r = { 'henry draper' : int_or_none( line[0:6] ),
              'durchmusterung id' : line[7:19],
              'boss general' : int_or_none( line[20:25] ),
              'bright star' : int_or_none( line[26:30] ),
              'hipparcos' : int_or_none( line[31:37] ),
              'ra' : ra,
              'de' : de,
              'magnitude' : float( line[58:63] ),
              'flamsteed' : int_or_none( line[64:67] ),
              'bayer' : line[68:73].strip(),
              'constellation' : line[74:77].strip() }
        return r
              

    def parse_table3( self, line ):
        """
        parse a single line from table3 and return the parts

        Example line, multiple proper names are separated by ; 
        105452   1 alf   Crv Alchiba; Al Minliar al Ghurab; Al Chiba                  2   
        """
        r = { 'henry draper' : int( line[0:6] ),
              'bayer-flamsteed' : line[7:20].strip(),
              'proper name' : line[21:76].strip().split(';'),
              'refs' : line[77:100].strip().split(',') }
        return r
        
    def __del__( self ):
        """
        for garbage collection, close any open file instances
        """
        for k,v in self.table_f:
            try:
                v.close()
            except IOError:
                # probably not open of already closed
                pass
                
