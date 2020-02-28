from googleads import adwords
import datetime
import hashlib
import pytz

class offlineConversionSource:

    _DT_FORMAT = '%Y%m%d %H%M%S'
    _TIMEZONE = pytz.timezone('America/New_York')  
    def __init__(self):
        print("init")

  
    def get(self):
        conversion_name = 'JimsConversionAction'  
        email_addresses = ['brookj@google.com', 'brookj@google.com']
        external_upload_id = 101010
        transaction_time_1 = (datetime.datetime.now(tz=self._TIMEZONE) - datetime.timedelta(days=7))
        offline_data = {
            'StoreSalesTransaction': {
            'userIdentifiers': [
                self._CreateUserIdentifier(identifier_type='HASHED_EMAIL', value=email_addresses[0]),
                self._CreateUserIdentifier(identifier_type='STATE', value='New York')
            ],
            'transactionTime': self._GetFormattedDateTime(transaction_time_1),
            'transactionAmount': {
                'currencyCode': 'USD',
                'money': {
                    'microAmount': 200000000
                }
            },
            'conversionName': conversion_name
            }
        }

        upload_metadata = {
            'StoreSalesUploadCommonMetadata': {
                'xsi_type': 'FirstPartyUploadMetadata',
                'loyaltyRate': 1.0,
                'transactionUploadRate': 1.0,
            }
        }
        upload_type = 'STORE_SALES_UPLOAD_FIRST_PARTY'
        offline_data_upload = {
            'externalUploadId': external_upload_id,
            'offlineDataList': [],
            
            'uploadType': upload_type,
            'uploadMetadata': upload_metadata
        }
        count = 0
        for count in range(50):
            offline_data_upload['offlineDataList'].append(offline_data)

        operation = {
            'operator': 'ADD',
            'operand': offline_data_upload
        }
        return operation


    def _GetFormattedDateTime(self, dt):
        """Formats the given datetime and timezone for use with AdWords.

        Args:
            dt: a datetime instance.

        Returns:
            A str representation of the datetime in the correct format for AdWords.
        """

        return '%s %s' % (datetime.datetime.strftime(dt, self._DT_FORMAT), self._TIMEZONE.zone)
    
    def _CreateUserIdentifier(self, identifier_type=None, value=None):
        """Creates a user identifier from the specified type and value.

        Args:
            identifier_type: a str specifying the type of user identifier.
            value: a str value of the identifier; to be hashed using SHA-256 if needed.

        Returns:
            A dict specifying a user identifier, with a value hashed using SHA-256 if
            needed.
        """
        _HASHED_IDENTIFIER_TYPES = ('HASHED_EMAIL', 'HASHED_FIRST_NAME',
                            'HASHED_LAST_NAME', 'HASHED_PHONE')
        if identifier_type in _HASHED_IDENTIFIER_TYPES:
            # If the user identifier type is a hashed type, normalize and hash the
            # value.
            value = value.encode('utf-8')
            value = hashlib.sha256(value.strip().lower()).hexdigest()

        user_identifier = {
            'userIdentifierType': identifier_type,
            'value': value
        }

        return user_identifier