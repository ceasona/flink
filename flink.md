-  wget https://mirrors.tuna.tsinghua.edu.cn/AdoptOpenJDK/8/jdk/x64/linux/ibm-semeru-open-jdk_x64_linux_8u302b08_openj9-0.27.0.tar.gz

- mkdir /usr/lib/jvm

- tar -zxvf ibm-semeru-open-jdk_x64_linux_8u302b08_openj9-0.27.0.tar.gz -C /usr/lib/jvm

- vi ~/.bashrc

  ```
  export JAVA_HOME=/usr/lib/jvm/jdk8u302-b08
  export JRE_HOME=${JAVA_HOME}/jre
  export CLASSPATH=.:${JAVA_HOME}/lib:${JRE_HOME}/lib
  export PATH=${JAVA_HOME}/bin:$PATH
  ```

- source ~/.bashrc

- java -version



tar xzf flink-1.13.2-bin-scala_2.11.tgz

`export FLINK_HOME=`

cd flink-1.13.2

./bin/start-cluster.sh

./bin/flink run -py /home/flink_test/examples2/table/4-udf_add_with_dependency.py



kafka

```
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties &

创建topic
bin/kafka-topics.sh --create --zookeeper localhost:2181 -replication-factor 1 --partitions 1 --topic Rides
 查看当前系统中所有的topic
bin/kafka-topics.sh --list --zookeeper localhost:2181
启动生产者
bin/kafka-console-producer.sh --broker-list localhost:9092 --topic Rides
启动消费者
bin/kafka-console-consumer.sh 	--bootstrap-server localhost:9092 --topic Rides --from-beginning

bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic Rides


```



flink-sql-connector-kafka_2.11-1.13.0.jar与flink版本要一致

https://repo1.maven.org/maven2/org/apache/flink/

redis JAR包

https://repo1.maven.org/maven2/com/alibaba/ververica/ververica-connector-redis/1.13-vvr-4.0.7/

参考：

- 基于 PyFlink 实现在线机器学习  https://www.jianshu.com/p/346e74290d65
- Flink 1.6.0 环境并构建运行简单程序入门  http://www.54tianzhisheng.cn/2018/09/18/flink-install/#%E5%AE%89%E8%A3%85-Flink
- 官方文档  https://ci.apache.org/projects/flink/flink-docs-release-1.9/zh/tutorials/python_table_api.html
- PyFlink中使用kafka和MySQL  https://blog.csdn.net/weixin_41856798/article/details/108703106
- flink中文社区  https://flink-learning.org.cn/
- pyflink  https://github.com/pyflink/playgrounds
- 阿里云实时计算Flink  https://developer.aliyun.com/group/sc?spm=a2c6h.12873639.0.d1002.31ef161b753SWN#/?_k=cqkk62
- PyFlink架构  https://blog.csdn.net/weixin_44904816/article/details/104935756
- CDN 日志实时分析  https://enjoyment.cool/2020/03/27/PyFlink%20%E5%9C%BA%E6%99%AF%E6%A1%88%E4%BE%8B-PyFlink%E5%AE%9E%E7%8E%B0CDN%E6%97%A5%E5%BF%97%E5%AE%9E%E6%97%B6%E5%88%86%E6%9E%90/
- 实时计算  https://help.aliyun.com/document_detail/178498.html
- 



Flink：job报错NoResourceAvailableException: Could not acquire the minimum required resources  https://blog.csdn.net/qq_42584411/article/details/119940818

Flink和Kafka网络连通，但Flink无法消费或者写入数据？ https://help.aliyun.com/document_detail/174840.htm?spm=a2c4g.11186623.0.0.4887391aiATA1F#section-qyp-6ig-ox2



docker run -it --net host --rm 2b8b72f601da /bin/bash

