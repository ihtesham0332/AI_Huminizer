# Current Performance Analysis

## 1. Latency
*   **Current:** End-to-end processing of a paragraph takes 5-15 seconds depending on local hardware.
*   **Bottleneck:** Sequential guardian checks and lack of caching.

## 2. Concurrency
*   **Current:** LangGraph nodes process candidates in parallel via `ThreadPoolExecutor`, which is good.
*   **Bottleneck:** The initial document analysis is not parallelized.

## 3. Missing Infrastructure
*   **Redis:** Without Redis, we cannot handle rate-limiting or job queueing effectively at scale, leading to potential timeout errors if 100 users hit the API simultaneously.
