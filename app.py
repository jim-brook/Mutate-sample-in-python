from googleads import adwords
from offline_data_source import offlineConversionSource
#import dumper

MAX_OBJECTS_PER_MUTATE = 2000
counter = 0
def start_upload():
    data_source = offlineConversionSource()
    operations = []

    adwords_client = adwords.AdWordsClient.LoadFromStorage()
    offline_data_upload_service = adwords_client.GetService('OfflineDataUploadService', version='v201809')


    # The operations param to mutate is actually a list of type OfflineDataUploadOperation. 
    # Using c#: operations = new List<OfflineDataUploadOperation>()
    # Each operations list can have up to 2,000 memebers per mutate().    
    for counter in range(MAX_OBJECTS_PER_MUTATE):
        # Get a single OfflineDataUploadOperation object that has offlineDataList size of up to 50 conversions
        operations.append(data_source.get()) # Then add it to our List<OfflineDataUploadOperation>

    # When we are done, we have 2,000 OfflineDataUploadOperation objects that have 50 conversions in each offlineDataList
    # Then call mutate() We will upload 2,000 * 50 = 100,000 conversions. This takes a minute or 2 on my dev system.
    #dumper.max_depth = 30
    #dumper.dump(operations)
    result = offline_data_upload_service.mutate(operations)


if __name__ == "__main__":
    start_upload()