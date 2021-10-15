kafka_source_ddl = """
CREATE TABLE cdn_access_log (
 uuid VARCHAR,
 client_ip VARCHAR,
 request_time BIGINT,
 response_size BIGINT
) WITH (
 'connector.type' = 'kafka',
 'connector.version' = 'universal',
 'connector.topic' = 'cdn_access_log',
 'connector.properties.zookeeper.connect' = 'localhost:2181',
 'connector.properties.bootstrap.servers' = 'localhost:9092',
 'format.type' = 'csv',
 'format.ignore-parse-errors' = 'true'
)
"""
# 注意修改MySQL中table的名称和MySQL的登录密码
mysql_sink_ddl = """
CREATE TABLE cdn_access_statistic (
 province VARCHAR,
 access_count BIGINT,
 total_download BIGINT,
 download_speed DOUBLE
 ) WITH (
 'connector' = 'jdbc',
 'url' = 'jdbc:mysql://172.17.0.1:3306/automl',
 'driver' = 'com.mysql.cj.jdbc.Driver',
 'table-name' = 'cdn_access_statistic',
 'username' = 'root',
 'password' = '681296'
)
"""
