# from flext-meltano_docs/guides/architecture-analysis.md:266
# Native Singer protocol usage
tap = FlextSingerTap("tap-gitlab", settings={"api_url": "https://gitlab.com"})
catalog = tap.discover().unwrap()
sync_result = tap.sync(catalog.streams[:5]).unwrap()```
## Performance Considerations

### Execution Optimization

#### Parallel Pipeline Execution

- **Resource Pooling**: Shared resource management across pipelines
- **Load Balancing**: Intelligent distribution of pipeline workload
- **Memory Management**: Efficient memory usage for large datasets
- **CPU Optimization**: Parallel processing for compute-intensive operations

#### Batch Processing Optimization

- **Configurable Batch Sizes**: Optimal batch sizes for different data types
- **Memory-Efficient Processing**: Streaming processing for large datasets
- **Connection Pooling**: Database and API connection reuse
- **Compression Support**: Automatic compression for large data transfers

### Monitoring and Observability

#### Performance Metrics

- **Execution Time Tracking**: Detailed timing for all operations
- **Resource Usage Monitoring**: CPU, memory, and I/O monitoring
- **Throughput Measurement**: Records per second processing rates
- **Error Rate Tracking**: Error frequency and categorization

#### Health Checks

- **Plugin Health Validation**: Regular plugin functionality checks
- **Pipeline Status Monitoring**: Real-time pipeline execution status
- **Resource Availability**: System resource availability monitoring
- **Dependency Health**: External service dependency monitoring

## Scalability Design

### Horizontal Scalability

#### Multi-Worker Architecture

