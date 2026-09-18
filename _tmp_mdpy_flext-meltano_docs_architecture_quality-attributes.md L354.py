# from flext-meltano/docs/architecture/quality-attributes.md:354
from __future__ import annotations


class AsyncPipelineExecutor:
    """Asynchronous pipeline execution with concurrency control."""

    def __init__(self, max_concurrent: int = 10, queue_size: int = 1000):
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.queue = asyncio.Queue(queue_size)
        self.metrics = AsyncMetrics()
        self.running_tasks: Set[asyncio.Task] = set()

    async def execute_pipeline_async(self, pipeline: Pipeline) -> PipelineResult:
        """Execute pipeline asynchronously with resource control."""
        async with self.semaphore:
            self.metrics.pipeline_started()

            try:
                # Validate pipeline
                validation_result = await self.validate_pipeline_async(pipeline)
                if validation_result.failure:
                    return PipelineResult.failure(validation_result.error)

                # Execute stages concurrently where possible
                results = await asyncio.gather(
                    self.execute_extraction_async(pipeline),
                    self.execute_transformation_async(pipeline),
                    self.execute_loading_async(pipeline),
                    return_exceptions=True,
                )

                # Process results
                if any(isinstance(r, Exception) for r in results):
                    # Handle exceptions
                    exceptions = [r for r in results if isinstance(r, Exception)]
                    return PipelineResult.failure(PipelineExecutionError(exceptions))

                # Combine results
                combined_result = self.combine_results(results)
                self.metrics.pipeline_completed()
                return combined_result

            except Exception as e:
                self.metrics.pipeline_failed()
                return PipelineResult.failure(PipelineExecutionError(str(e)))

    async def validate_pipeline_async(
        self, pipeline: Pipeline
    ) -> p.Result[ValidatedPipeline]:
        """Async pipeline validation."""
        # Run validation checks concurrently
        validation_tasks = [
            self.validate_sources_async(pipeline.sources),
            self.validate_targets_async(pipeline.targets),
            self.validate_transforms_async(pipeline.transforms),
            self.check_dependencies_async(pipeline),
        ]

        results = await asyncio.gather(*validation_tasks, return_exceptions=True)

        if any(isinstance(r, Exception) for r in results):
            exceptions = [r for r in results if isinstance(r, Exception)]
            return r.fail(ValidationError(f"Validation failed: {exceptions}"))

        return r.ok(ValidatedPipeline(pipeline, results))

    async def execute_extraction_async(self, pipeline: Pipeline) -> ExtractionResult:
        """Execute data extraction asynchronously."""
        extractors = []
        for source in pipeline.sources:
            extractor = self.create_extractor(source)
            extractors.append(extractor.extract_async())

        # Execute extractions concurrently
        results = await asyncio.gather(*extractors, return_exceptions=True)

        # Process results and handle errors
        successful_extractions = [r for r in results if not isinstance(r, Exception)]
        failed_extractions = [r for r in results if isinstance(r, Exception)]

        return ExtractionResult(successful_extractions, failed_extractions)```
### Performance Monitoring

