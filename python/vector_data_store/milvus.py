from pymilvus import MilvusClient,DataType

client = MilvusClient(
    uri="http://localhost:19530",
    token="root:Milvus"
)

# # create database
# client.create_database(
#     db_name="my_database_1"
# )
#
# use database
client.use_database(
    db_name="my_database_1"
)
#
# # drop database
# client.drop_database(
#     db_name="my_database_2"
# )

# List all existing databases
dbs = client.list_databases()
print(dbs)

# Check database details
details = client.describe_database(
    db_name="default"
)
print(details)

# # update properties
# status = client.alter_database_properties(
#     db_name="my_database_1",
#     properties={
#         "database.max.collections": 10,
#          "database.replica.number": 1
#     }
# )
# print(status)
#
# # del properties
# status = client.drop_database_properties(
#     db_name="my_database_1",
#     property_keys=[
#         "database.max.collections"
#     ]
# )
# print(status)

# # 3.1. Create schema
# schema = MilvusClient.create_schema(
#     auto_id=False,
#     enable_dynamic_field=True,
# )
#
# # 3.2. Add fields to schema
# schema.add_field(field_name="my_id", datatype=DataType.INT64, is_primary=True)
# schema.add_field(field_name="my_vector", datatype=DataType.FLOAT_VECTOR, dim=5)
# schema.add_field(field_name="my_varchar", datatype=DataType.VARCHAR, max_length=512)
#
# # 3.3. Prepare index parameters
# index_params = client.prepare_index_params()
#
# # 3.4. Add indexes
# index_params.add_index(
#     field_name="my_id",
#     index_type="AUTOINDEX"
# )
# index_params.add_index(
#     field_name="my_vector",
#     index_type="AUTOINDEX",
#     metric_type="COSINE"
# )
#
# # 3.5. Create a collection with the index loaded simultaneously
# client.create_collection(
#     collection_name="customized_setup_1",
#     schema=schema,
#     index_params=index_params
# )
# res = client.get_load_state(
#     collection_name="customized_setup_1"
# )
#
# # list collection
# res = client.list_collections()
# print(res)

# # describe collection
# res = client.describe_collection(
#     collection_name="customized_setup_1"
# )
# print(res)

# # update collection
# client.rename_collection(
#     old_name="customized_setup_1",
#     new_name="customized_setup_2"
# )

# # set collection properties
# client.alter_collection_properties(
#     collection_name="customized_setup_1",
#     properties={"collection.ttl.seconds": 60}
# )
# # delete collection properties
# client.drop_collection_properties(
#     collection_name="my_collection",
#     property_keys=[
#         "collection.ttl.seconds"
#     ]
# )

# # load collection
# # 7. Load the collection
# client.load_collection(
#     collection_name="customized_setup_1"
# )
# res = client.get_load_state(
#     collection_name="customized_setup_1"
# )
# print(res)

# # load fields
# client.load_collection(
#     collection_name="customized_setup_1",
#     load_fields=["my_id", "my_vector"], # Load only the specified fields
#     skip_load_dynamic_field=True # Skip loading the dynamic field
# )
# res = client.get_load_state(
#     collection_name="customized_setup_1"
# )
# print(res)

# # release collection
# # 8. Release the collection
# client.release_collection(
#     collection_name="customized_setup_1"
# )
# res = client.get_load_state(
#     collection_name="customized_setup_1"
# )
# print(res)

# data=[
#     {"my_id": 0, "my_vector": [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592], "my_varchar": "pink_8682"},
#     {"my_id": 1, "my_vector": [0.19886812562848388, 0.06023560599112088, 0.6976963061752597, 0.2614474506242501, 0.838729485096104], "my_varchar": "red_7025"},
#     {"my_id": 2, "my_vector": [0.43742130801983836, -0.5597502546264526, 0.6457887650909682, 0.7894058910881185, 0.20785793220625592], "my_varchar": "orange_6781"}
# ]
# # res = client.insert(
# #     collection_name="customized_setup_1",
# #     data=data
# # )
# # print(res)
#
# res = client.upsert(
#     collection_name='customized_setup_1',
#     data=data
# )
# print(res)

# 4. Single vector search
query_vector = [0.3580376395471989, -0.6023495712049978, 0.18414012509913835, -0.26286205330961354, 0.9029438446296592]
res = client.search(
    collection_name="customized_setup_1",
    anns_field="my_vector",
    data=[query_vector],
    limit=3,
    search_params={"metric_type": "COSINE"}
)
for hits in res:
    for hit in hits:
        print(hit)

client.close()
