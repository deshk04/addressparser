"""
  Author:         
  Create date:    
  Description:    PDM custom exception


  Date                Description(of Changes)
                             Created
"""
import logging

"""
Global PDMas exception and warning classes.
"""

class PDMMandatoryFieldMissing(Exception):
    """Mandatory field does not exist"""
    logging.debug("some required fields are missing")


class PDMUnknownError(Exception):
    """Api (e.g. google) Unknown Error"""
    logging.debug("Unknown Error")


class PDMZeroResults(Exception):
    """Api resulted in no output"""
    logging.debug("Zero Result returned")


class PDMOverQueryLimit(Exception):
    """Google Api Query Limit"""
    logging.debug("Api Query Limit Reached")


class PDMRequestDenied(Exception):
    """Google Api Request Denied"""
    logging.debug("Api Request Denied")


class PDMInvalidRequest(Exception):
    """Google Api Invalid Request"""
    logging.debug("Api Invalid Request")


class PDMNotFound(Exception):
    """Request return not found"""
    logging.debug("Api Request Not found")


class PDMDBQueryError(Exception):
    """Database query had issue"""
    logging.debug("Database query problem")


class PDMDBConnError(Exception):
    """Database query had issue"""
    logging.debug("Database connection problem")


class PDMMultipleObjectsReturned(Exception):
    """Database query had issue"""
    logging.debug("Multiple Objects Returned")

class PDMSOAPConnectionError(Exception):
    """SOAP Connection had issue"""
    logging.debug("SOAP connection Error")

class PDMSOAPException(Exception):
    """SOAP Connection had issue"""
    logging.debug("SOAP Exception")

class PDMSOAPInvalidConnection(Exception):
    """SOAP Connection had issue"""
    logging.debug("SOAP Invalid Connection")

class PDMSOAPServiceError(Exception):
    """SOAP Service had issue"""
    logging.debug("SOAP Service Error")


class PDMSOAPServiceDataError(Exception):
    """SOAP Service had issue"""
    logging.debug("SOAP Service Data Error")
