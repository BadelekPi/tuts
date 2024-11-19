main types: document, key-value, wide-column, graph
    and become quite popular: multi-model databases

----------------------------
Document oriented databases |
----------------------------
similar to JSON, contains pairs of fields and values
Values can be variety of types.
Offers a flexible data model, preffered for semi-structured and unstructered data sets.
Support nested structures.
Examples: MongoDB, Couchbase

--------------------
Key-value databases |
--------------------
each item contains keys and values
Examples: Amazon DynamoDB, Redis

-------------------
Wide-column stores |
-------------------
stores data in tables, rows and dynamic columns. Data stored in tables
wide-column stores are flexible, where different rows can have different sets of columns
can employ column compression techniques to reduce storage space and enhance performance
enable efficient retrieval of sparse and wide data
Examples: Apache Cassandra, HBase

----------------
Graph databases |
----------------
Stores data in forms of nodes and edges.
Edges store information about the reliationships between the nodes.
Work well for highly connected data, where the relationships or patterns may not be very obvious initially.
Examples: Neo4J, Amazon Neptune, MongoDB graphLookup

----------------------
Multi-model databases |
----------------------
Can support more than one type of NoSQL data model.
Examples: CosmosDB, ArangoDB
