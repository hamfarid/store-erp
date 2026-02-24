# Error Catalog: Spark Job Failures (v2026.2)

## 1. OutOfMemoryError (OOM)
-   **Symptom:** `java.lang.OutOfMemoryError: Java heap space`.
-   **Cause:** Executor memory too low, data skew, or large broadcast join.
-   **Fix:**
    -   Increase `spark.executor.memory`.
    -   Increase `spark.sql.shuffle.partitions`.
    -   Use `repartition()` to balance data.
    -   Disable Broadcast Join (`spark.sql.autoBroadcastJoinThreshold = -1`).

## 2. Executor Lost
-   **Symptom:** `ExecutorLostFailure (executor 1 exited caused by one of the running tasks)`.
-   **Cause:** Node failure, network partition, or OOM (killed by YARN/K8s).
-   **Fix:**
    -   Check YARN/K8s logs for resource limits.
    -   Increase `spark.yarn.executor.memoryOverhead`.
    -   Reduce task parallelism per executor.

## 3. Serialization Error
-   **Symptom:** `Task not serializable`.
-   **Cause:** Using non-serializable objects (e.g., DB connection) inside RDD/DataFrame transformations.
-   **Fix:**
    -   Initialize connections inside `mapPartitions` or `foreachPartition`.
    -   Mark non-serializable fields as `transient` (Scala/Java).
    -   Use `broadcast` variables for shared read-only data.

## 4. Slow Stages (Stragglers)
-   **Symptom:** 99% tasks finish quickly, last 1% take hours.
-   **Cause:** Data Skew (one key has millions of records).
-   **Fix:**
    -   Salting: Add random prefix to skewed keys before join/group.
    -   Use `aqe` (Adaptive Query Execution) in Spark 3+.
