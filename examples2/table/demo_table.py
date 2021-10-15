from pyflink.table import EnvironmentSettings, StreamTableEnvironment, DataTypes
from pyflink.table.catalog import HiveCatalog
from pyflink.table.expressions import col
from pyflink.table.udf import udf



# 一、定义环境及参数

env_settings = EnvironmentSettings.new_instance().in_streaming_mode().use_blink_planner().build()
t_env = StreamTableEnvironment.create(environment_settings=env_settings)

m = t_env.get_config().get_configuration().set_string('parallelism.default', '1')
t_env.get_config().get_configuration().set_string("pipeline.jars",
                                                  "file:///my/jar/path/flink-sql-connector-kafka_2.11-1.12.0.jar")


# 二、构建数据源
# 方式一：from_elements
tab = t_env.from_elements([("hello", 1), ("world", 2), ("flink", 3)], ['a', 'b'])

# # 方式二：ddl
# t_env.execute_sql("""
#         CREATE TABLE my_source (
#           a VARCHAR,
#           b VARCHAR
#         ) WITH (
#           'connector' = 'datagen',
#           'number-of-rows' = '10'
#         )
#     """)
# tab = t_env.from_path('my_source')
#
# # 方式三：catalog
# hive_catalog = HiveCatalog("hive_catalog")
# t_env.register_catalog("hive_catalog", hive_catalog)
# t_env.use_catalog("hive_catalog")
# # 假设hive catalog中已经定义了一个名字为source_table的表
# tab = t_env.from_path('source_table')

# 三、定义计算逻辑
# 方式一：通过 Table API
@udf(result_type=DataTypes.STRING())
def sub_string(s: str, begin: int, end: int):
   return s[begin:end]
transformed_tab = tab.select(sub_string(col('a'), 2, 4))
# print(transformed_tab)
# print(transformed_tab.explain())

# result = transformed_tab.to_pandas()
# table_result = transformed_tab.execute()
# with table_result.collect() as results:
#     for result in results:
#         print(result)

# print(t_env.explain_sql("INSERT INTO my_sink SELECT * FROM %s " % transformed_tab))
# # 方式二：通过 SQL 语句
# t_env.create_temporary_function("sub_string", sub_string)
# transformed_tab = t_env.sql_query("SELECT sub_string(a, 2, 4) FROM %s" % tab)


# 三、定义sink
t_env.execute_sql("""
        CREATE TABLE my_sink (
          `sum` VARCHAR
        ) WITH (
          'connector' = 'print'
        )
    """)

table_result = transformed_tab.execute_insert('my_sink')
table_result.wait()


