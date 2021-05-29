import os
import logging
from datetime import datetime
from datetime import date

import pdb

from datetime import timedelta

from core.general import settings
from core.general import start
from core.general import Database


def main():
    """
        Main script which handles the request for abn
    """

    start()
    db_obj = Database()
    logging.debug("Database connection established")

    # tempfetchabn('25280026074')

    from core.parser.addressreference import AddressReference
    addref = AddressReference()
    status = addref.get_reference(db_obj)

# rec 1
# ---------
# address: l 2 haematology & oncology, 183 wattletree rd, malvern , 3144 , vic
# org: cabrini hospital, -37.86282776 145.03306887

# rec 2
# ---------
# address: l 3, 1 arnold st ,box hill , 3128 , vic
# org: no practice, -37.81455356 145.11955718

# rec 3
# ---------
# anastasia chrysostomou
# address: l 2, 55 flemington rd ,hotham hill , 3051 , vic
# org: dr anastasia chrysostomou -37.79960117 144.95435588

# rec 4
# ---------
# address: se 14, 529 police rd ,mulgrave , 3170 , vic
# org: melbourne heart care -37.9384362 145.2114277

    from core.parser.addressparser import AddressParser
    from core.parser.gnafhandler import GnafHandler

    addparser = AddressParser(
        address_line1='l 2, 55 flemington rd',
        address_line2='',
        suburb='hotham hill',
        postcode='3051',
        state='vic'
    )
    addparser.parse()

    if addparser.addressdetails:
        print('Searching for gnaf...')
        gnafHandler = GnafHandler()
        gnafHandler.dbObj = db_obj
        gnafHandler.addressdetails = addparser.addressdetails
        record = gnafHandler.execute()
        if record:
            addparser.addressdetails.premises_type = record.geocode_type
            addparser.addressdetails.latitude = record.latitude
            addparser.addressdetails.longitude = record.longitude
            addparser.addressdetails.parcel_id = record.legal_parcel_id
            print(str(addparser.addressdetails))
    else:
        print('Not found')

    pdb.set_trace()



if __name__ == '__main__':
    """
        start
    """
    main()
