"""
  Description:    Proxy modules for django orm
"""

from django.db import models

from adr.models import AddressDetails, GooglePlaces
from adr.models import DimAddrAbbrWords, DimAddrCommonwords, DimAddrPatch
from adr.models import DimAddrPobox, DimAddressType, DimCommonWords
from adr.models import DimGnafPostcode, DimGnafStreets, DimNameAbbr
from adr.models import DimPobox, DimWordDictionary
from adr.models import StagingInputData, StagingProcessedAddress

from core.models.modelmanager import ModelManager


class AddressDetailsProxy(AddressDetails):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(AddressDetails, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class GooglePlacesDetailsProxy(GooglePlaces):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(GooglePlaces, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimAddrAbbrWordsProxy(DimAddrAbbrWords):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimAddrAbbrWords, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimAddrCommonwordsProxy(DimAddrCommonwords):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimAddrCommonwords, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimAddrPatchProxy(DimAddrPatch):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimAddrPatch, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimAddrPoboxProxy(DimAddrPobox):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimAddrPobox, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'


class DimAddressTypeProxy(DimAddressType):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimAddressType, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimCommonWordsProxy(DimCommonWords):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimCommonWords, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'


class DimGnafPostcodeProxy(DimGnafPostcode):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimGnafPostcode, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimGnafStreetsProxy(DimGnafStreets):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimGnafStreets, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimNameAbbrProxy(DimNameAbbr):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimNameAbbr, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'


class DimPoboxProxy(DimPobox):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimPobox, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class DimWordDictionaryProxy(DimWordDictionary):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(DimWordDictionary, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'


class StagingInputDataProxy(StagingInputData):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(StagingInputData, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'

class StagingProcessedAddressProxy(StagingProcessedAddress):
    objects = ModelManager()

    def __init__(self, *args, **kwargs):
        super(StagingProcessedAddress, self).__init__(*args, **kwargs)

    class Meta:
        proxy = True
        app_label = 'adr'
