# awspytools

##DynamoDBDataStore

This is a helper python package to make DynamoDB easier to work with.

To get started, import DynamoDBDatastore from awspytools:

```python
from awspytools import DynamoDBDataStore
``` 

Initialize a store using the Table Name:
```python
store = DynamoDBDataStore(table_name='DynamoDB Table Name')
```
By default, we assume the following hash, sort and index keys:
```python
hash_key = 'PK'
sort_key = 'SK'
GSI1_HASH_KEY = 'GSI1PK'
GSI1_SORT_KEY = 'GSI1SK'
GSI2_HASH_KEY = 'GSI2PK'
GSI2_SORT_KEY = 'GSI2SK'
```

To override these values, you may define your store as follows:
```python
store = DynamoDBDataStore(
    table_name='DynamoDB Table Name',
    hash_key='custom_hash',
    sort_key='custom_sort',
    use_default_index_keys=False
)
```

You may add custom Index keys as follows:
```python
store.add_index_key('custom gsi 1')
```
or you may add many index keys as follows:
```python
store.add_index_keys(['custom gsi 1 hash', 'custom gsi 1 sort'])
```

To get a document, do the following:
```python
result = store.get_document(index=('hash_key', 'sort_key'), return_index=True)
```
If you specify:
```python
return_index=False
```
The response object will not have the hash /sort key or GSI keys specified in the response.

To save a document, simple do:
```python
store.save_document(
    document={
        "number": 1,
        "hello": "world",
        "foo": ['bar', 'spam'],
        "foo": {
            "spam": "eggs"
        }
    },
    index=('hash_id', 'sort_id')
)
```

To get multiple documents, you need to provide a query. Note this paginates the result for you so all documents are returned!
```python
query = {
		'ExpressionAttributeNames': {'#PK': 'PK'},
		'ExpressionAttributeValues': {':PK': {'S': 'hash_key'}},
		'KeyConditionExpression': '#PK = :PK'
	}
result = store.get_documents(query)
```

To delete a document:
result = store.delete_document(index=('hash_key', 'sort_key'))

To perform a batch request, we have a wrapper for boto3's batch_write_item:
```python
batch_request = store.batch_request(
    request_items=[ 
         { 
            "DeleteRequest": {...}, #As per boto3's parameter structure
            "PutRequest": {...} #As per boto3's document structure parameter structure
         }
      ]
)
```

To perform a transaction:
```python
transaction_items = [
    {
        'Update': {
            'Key': {
                'PK': {'S': 'hash'},
                'SK': {'S': 'sort'},
            },
            'UpdateExpression': 'SET some_key = :some_value',
            'ExpressionAttributeValues': {
                ':some_value': {'S': 'hello world'},
            },
            'TableName': store.table_name
        }
    },
    {
        'Update': {
            'Key': {
                'PK': {'S': 'hash'},
                'SK': {'S': 'sort'},
            },
            'UpdateExpression': 'SET new_key = :new_value',
            'ExpressionAttributeValues': {
                ':new_value': {'S': 'hello world'},
            },
            'TableName': store.table_name
        }
    }
]
store.transaction_write(transaction_items, "some_unique_id")
```