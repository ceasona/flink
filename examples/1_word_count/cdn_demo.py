import os

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from cdn_connector_ddl import kafka_source_ddl, mysql_sink_ddl

# 创建Table Environment， 并选择使用的Planner
env = StreamExecutionEnvironment.get_execution_environment()
t_env = StreamTableEnvironment.create(
    env,
    environment_settings=EnvironmentSettings.new_instance().use_blink_planner().build())
# set source table
# 创建Kafka数据源表,以及会创建一个kafka的新的topic——cdn_access_log
t_env.sql_update(kafka_source_ddl)
# 创建MySql结果表,这个创建的只是flink内部的table，所以在此之前我们需要在MySQL中重新建立MySQL的table表。
t_env.sql_update(mysql_sink_ddl)

# 核心的统计逻辑
t_env.from_path("cdn_access_log") \
    .select("uuid, "
            "client_ip as province, "
            "response_size, request_time") \
    .group_by("province") \
    .select(  # 计算访问量
    "province, count(uuid) as access_count, "
    # 计算下载总量 
    "sum(response_size) as total_download,  "
    # 计算下载速度
    "sum(response_size) * 1.0 / sum(request_time) as download_speed") \
    .insert_into("cdn_access_statistic")

# 执行作业
t_env.execute("test")
