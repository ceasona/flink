from pyflink.datastream import StreamExecutionEnvironment, TimeCharacteristic
from pyflink.table import StreamTableEnvironment, EnvironmentSettings

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
    'connector.topic' = 'inputMysql',
    'connector.properties.zookeeper.connect' = 'localhost:2181',
    'connector.properties.bootstrap.servers' = 'localhost:9092',
    'connector.startup-mode' = 'earliest-offset',
    'format.type' = 'json'
)
"""

mysql_sink_ddl = """
CREATE TABLE sink (
    rideId BIGINT,
    isStart VARCHAR 
) WITH (
        'connector' = 'jdbc',
        'url' = 'jdbc:mysql://212.64.36.92:3306/schinper_database',
        'driver' = 'com.mysql.cj.jdbc.Driver',
        'table-name' = 'case4',
        'username' = 'root',
        'password' = '681296')
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
    st_env.sql_update(mysql_sink_ddl)

    st_env.from_path('source').select('rideId, isStart').print_schema()

    # query
    st_env.from_path("source").select('rideId, isStart').insert_into("sink")

    # execute
    st_env.execute("kafka2kafka")


if __name__ == '__main__':
    from_kafka_to_kafka_demo()
