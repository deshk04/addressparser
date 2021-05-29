"""
  Author:
  Create date:
  Description:    ADDR custom exception


  Date                Description(of Changes)
                             Created
"""
import logging

"""
Global ADDRas exception and warning classes.
"""

class ADDRMandatoryFieldMissing(Exception):
    """Mandatory field does not exist"""
    logging.debug("some required fields are missing")


class ADDRUnknownError(Exception):
    """Api (e.g. google) Unknown Error"""
    logging.debug("Unknown Error")


class ADDRZeroResults(Exception):
    """Api resulted in no output"""
    logging.debug("Zero Result returned")


class ADDROverQueryLimit(Exception):
    """Google Api Query Limit"""
    logging.debug("Api Query Limit Reached")


class ADDRRequestDenied(Exception):
    """Google Api Request Denied"""
    logging.debug("Api Request Denied")


class ADDRInvalidRequest(Exception):
    """Google Api Invalid Request"""
    logging.debug("Api Invalid Request")


class ADDRNotFound(Exception):
    """Request return not found"""
    logging.debug("Api Request Not found")


class ADDRDBQueryError(Exception):
    """Database query had issue"""
    logging.debug("Database query problem")


class ADDRDBConnError(Exception):
    """Database query had issue"""
    logging.debug("Database connection problem")


class ADDRMultipleObjectsReturned(Exception):
    """Database query had issue"""
    logging.debug("Multiple Objects Returned")

class ADDRSOAPConnectionError(Exception):
    """SOAP Connection had issue"""
    logging.debug("SOAP connection Error")

class ADDRSOAPException(Exception):
    """SOAP Connection had issue"""
    logging.debug("SOAP Exception")

class ADDRSOAPInvalidConnection(Exception):
    """SOAP Connection had issue"""
    logging.debug("SOAP Invalid Connection")

class ADDRSOAPServiceError(Exception):
    """SOAP Service had issue"""
    logging.debug("SOAP Service Error")


class ADDRSOAPServiceDataError(Exception):
    """SOAP Service had issue"""
    logging.debug("SOAP Service Data Error")
