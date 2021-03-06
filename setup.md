## Athena Setup

These queries create the **5 required tables**.

#### Creating the relevant tables
First, ensure that the region is set to `us-east-1 (N. Virginia)` (where the OSM data lives), then run the following Athena queries.

##### 1. Changesets
The changesets table is generated from the OSM Amazon Public Dataset: _s3://osm-pds/changesets_. The changeset table is needed for global editing summaries and to connect users to individual objects.

```sql
CREATE EXTERNAL TABLE `changesets`(
  `id` bigint, 
  `tags` map<string,string>, 
  `created_at` timestamp, 
  `open` boolean, 
  `closed_at` timestamp, 
  `comments_count` bigint, 
  `min_lat` decimal(9,7), 
  `max_lat` decimal(9,7), 
  `min_lon` decimal(10,7), 
  `max_lon` decimal(10,7), 
  `num_changes` bigint, 
  `uid` bigint, 
  `user` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://osm-pds/changesets/'
TBLPROPERTIES (
  'CrawlerSchemaDeserializerVersion'='1.0', 
  'CrawlerSchemaSerializerVersion'='1.0', 
  'UPDATED_BY_CRAWLER'='osm-changesets', 
  'averageRecordSize'='33', 
  'classification'='orc', 
  'compressionType'='none', 
  'objectCount'='1', 
  'recordCount'='73447524', 
  'sizeKey'='2487145556', 
  'typeOfData'='file')
```

The next tables are location specific. They include all of the OSM objects (with historical versions) for the listed regions:

##### 2. Nepal
```sql
CREATE EXTERNAL TABLE `nepal`(
  `type` tinyint, 
  `id` bigint, 
  `geom` string, 
  `tags` map<string,string>, 
  `changeset` bigint, 
  `updated` timestamp, 
  `valid_until` timestamp, 
  `visible` boolean, 
  `version` int, 
  `minor_version` int, 
  `bbox` struct<minx:float,miny:float,maxx:float,maxy:float>)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://osm-30k/orc/nepal_wkt'
TBLPROPERTIES (
  'numFiles'='5', 
  'numRows'='8113647', 
  'presto_query_id'='20190821_230045_00023_ehmbb', 
  'presto_version'='0.220', 
  'rawDataSize'='4351815521', 
  'totalSize'='1318338251')
```

##### 3. Central America / Caribbean
```sql
CREATE EXTERNAL TABLE `central_america`(
  `type` tinyint, 
  `id` bigint, 
  `geom` string, 
  `tags` map<string,string>, 
  `changeset` bigint, 
  `updated` timestamp, 
  `valid_until` timestamp, 
  `visible` boolean, 
  `version` int, 
  `minor_version` int, 
  `bbox` struct<minx:float,miny:float,maxx:float,maxy:float>)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://osm-30k/orc/central_america'
TBLPROPERTIES (
  'numFiles'='5', 
  'numRows'='19771168', 
  'presto_query_id'='20190821_224320_00020_ehmbb', 
  'presto_version'='0.220', 
  'rawDataSize'='14250587613', 
  'totalSize'='4170284573')
```

##### 4. SouthEastern Asia
```sql
CREATE EXTERNAL TABLE `southeastern_asia`(
  `type` tinyint, 
  `id` bigint, 
  `geom` string, 
  `tags` map<string,string>, 
  `changeset` bigint, 
  `updated` timestamp, 
  `valid_until` timestamp, 
  `visible` boolean, 
  `version` int, 
  `minor_version` int, 
  `bbox` struct<minx:float,miny:float,maxx:float,maxy:float>)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://osm-30k/orc/southeastern_asia'
TBLPROPERTIES (
  'numFiles'='5', 
  'numRows'='101543069', 
  'presto_query_id'='20190821_223448_00019_ehmbb', 
  'presto_version'='0.220', 
  'rawDataSize'='53964524217', 
  'totalSize'='16477421083')
```

##### 5. Subsaharan Africa
```sql
CREATE EXTERNAL TABLE `subsaharan_africa`(
  `type` tinyint, 
  `id` bigint, 
  `geom` string, 
  `tags` map<string,string>, 
  `changeset` bigint, 
  `updated` timestamp, 
  `valid_until` timestamp, 
  `visible` boolean, 
  `version` int, 
  `minor_version` int, 
  `bbox` struct<minx:float,miny:float,maxx:float,maxy:float>)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.orc.OrcSerde' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.orc.OrcOutputFormat'
LOCATION
  's3://osm-30k/orc/subsaharan_africa'
TBLPROPERTIES (
  'numFiles'='5', 
  'numRows'='108796230', 
  'presto_query_id'='20190821_222319_00018_ehmbb', 
  'presto_version'='0.220', 
  'rawDataSize'='60319965569', 
  'totalSize'='18762706803')
```
