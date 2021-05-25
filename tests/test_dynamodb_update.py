import os
from awspytools import DynamoDBDataStore, ReturnValues

store = DynamoDBDataStore(os.environ["CORE_TABLE_NAME"])

OLD = "OLD"
NEW = "NEW"
ATTR_1 = "ATTR_1"
ATTR_2 = "ATTR_2"
PK = "PK"
SK = "SK"
DOCUMENT = {ATTR_1: OLD, ATTR_2: OLD}
UPDATE_PARAMS = {
    "UpdateExpression": f"SET {ATTR_1} = :new",
    "ExpressionAttributeValues": {
        ":new": {"S": NEW},
    },
}


def test_all_new():
    store.save_document(document=DOCUMENT, index=(PK, SK))
    new_document = store.update_document(
        index=(PK, SK),
        parameters=UPDATE_PARAMS,
        return_value=ReturnValues.ALL_NEW,
    )
    assert new_document == {ATTR_1: NEW, ATTR_2: OLD}


def test_updated_new():
    store.save_document(document=DOCUMENT, index=(PK, SK))
    new_document = store.update_document(
        index=(PK, SK),
        parameters=UPDATE_PARAMS,
        return_value=ReturnValues.UPDATED_NEW,
    )
    assert new_document == {ATTR_1: NEW}


def test_all_old():
    store.save_document(document=DOCUMENT, index=(PK, SK))
    new_document = store.update_document(
        index=(PK, SK),
        parameters=UPDATE_PARAMS,
        return_value=ReturnValues.ALL_OLD,
    )
    assert new_document == DOCUMENT


def test_updated_old():
    store.save_document(document=DOCUMENT, index=(PK, SK))
    new_document = store.update_document(
        index=(PK, SK),
        parameters=UPDATE_PARAMS,
        return_value=ReturnValues.UPDATED_OLD,
    )
    assert new_document == {ATTR_1: OLD}


def test_none():
    store.save_document(document=DOCUMENT, index=(PK, SK))
    new_document = store.update_document(
        index=(PK, SK),
        parameters=UPDATE_PARAMS,
        return_value=ReturnValues.NONE,
    )
    assert new_document is None


def test_return_index():
    store.save_document(document=DOCUMENT, index=(PK, SK))
    new_document = store.update_document(
        index=(PK, SK),
        parameters=UPDATE_PARAMS,
        return_value=ReturnValues.ALL_OLD,
        return_index=True,
    )
    assert new_document == {**DOCUMENT, PK: PK, SK: SK}
