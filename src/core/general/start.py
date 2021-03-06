"""
#  Author:
#  Create date:
#  Description:    custome logger
#
#
#  Version     Date                Description(of Changes)
#  1.0                             Created
"""

import os
import logging
import sys
from datetime import datetime
from imp import reload

from core.general import settings

import pdb


def start(exceptionFlag='Y'):
    """ Logger is created based on main program name
        it should create a log filename
    """
    (dirPath, dirname) = os.path.split(os.getcwd())
    mainfile = os.path.realpath(sys.argv[0])

    dirname = mainfile.split('/')[-2]
    filename = mainfile.split('/')[-1].split('.')[0]
    """
        create log file
    """

    logfile = settings.LOG_PATH + dirname + '/'\
        + filename + '_' + datetime.now().strftime('%Y%m%d.log')

    reload(logging)
    logging.basicConfig(filename=logfile,
                        filemode='w',
                        level=settings.LOGGING_LEVEL,
                        format='%(asctime)s %(name)-12s - %(levelname)s - %(message)s')  # noqa

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    """
        set a format which is simpler for console use
    """
    formatter = logging.Formatter(
        '%(name)-12s: %(levelname)-8s %(message)s')
    """
        tell the handler to use this format
    """
    console.setFormatter(formatter)
    """
        add the handler to the root logger
    """
    logging.getLogger('').addHandler(console)

    logging.info("Starting job: " + filename)
    setup_django()


def log_excepthook(exc_Type, exc_Value, exc_traceback):
    """ Exception generated by any code should be captured
        in log, hence we hook it to _mitas_excepthook
    """
    import inspect
    import traceback

    tracelog = traceback.TracebackException(exc_Type, exc_Value, exc_traceback)

    logging.debug("Logging an uncaught exception", tracelog.stack)

    print("Job Failed!!!")
    print(stackMsg)
    logging.debug(stackMsg)


def setup_django():
    """
        setup for Django ORM
    """
    logging.debug("Setting up django")
    django_proj_path = os.getenv("DJANGOPROJECTPATH",
                                 settings.DJANGO_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "addr.settings")
    sys.path.append(django_proj_path)

    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
