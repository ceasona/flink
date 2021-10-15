import os
import shutil

from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, DataTypes, EnvironmentSettings, BatchTableEnvironment
from pyflink.table.descriptors import Schema, Kafka, Json, FileSystem, OldCsv

dir_result = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'result')
# 如果文件/文件夹存在，则删除
if os.path.exists(dir_result):
    if os.path.isfile(dir_result):
        os.remove(dir_result)
    else:
        shutil.rmtree(dir_result, True)

kafka_source_ddl = """
CREATE TABLE source (
    rideId BIGINT,
    isStart VARCHAR,
    eventTime VARCHAR,
    lon FLOAT,
    lat FLOAT,
    psgCnt INT ,
    taxiId BIGINT 
) WITH (
    'connector.type' = 'kafka',
    'connector.version' = 'universal',
    'connector.topic' = 'Rides',
    'connector.properties.zookeeper.connect' = 'localhost:2181',
    'connector.properties.bootstrap.servers' = 'localhost:9092',
    'connector.startup-mode' = 'earliest-offset',
    'format.type' = 'json'
)
"""

file_sink_ddl = """
CREATE TABLE sink (
    rideId BIGINT,
    isStart VARCHAR 
) WITH (
        'connector.type' = 'filesystem',
        'connector.path' = '/home/flink_test/examples/3_database_sync/result',
        'format.type'='csv'
)
"""


def from_kafka_to_kafka_demo():
    s_env = StreamExecutionEnvironment.get_execution_environment()
    s_env.set_stream_time_characteristic(TimeCharacteristic.EventTime)
    s_env.set_parallelism(1)
    # use blink table planner
    st_env = StreamTableEnvironment \
        .create(s_env, environment_settings=EnvironmentSettings
                .new_instance()
                .in_streaming_mode()
                .use_blink_planner().build())

    # register source and sink

    st_env.sql_update(kafka_source_ddl)
    st_env.from_path('source').select('rideId, isStart').print_schema()
    st_env.sql_update(file_sink_ddl)

    # query
    st_env.from_path("source").select('rideId, isStart').insert_into("sink")

    # execute
    st_env.execute("kafka2file")


if __name__ == '__main__':
    from_kafka_to_kafka_demo()
