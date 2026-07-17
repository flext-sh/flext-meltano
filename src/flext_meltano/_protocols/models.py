"""Structural contracts for Meltano-owned Pydantic models."""

from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, runtime_checkable

if TYPE_CHECKING:
    from flext_meltano import t


class FlextMeltanoProtocolsModels:
    """Model contracts consumed through ``p.Meltano`` annotations."""

    @runtime_checkable
    class CliDataSourceParams(Protocol):
        """Parameters required to translate one Singer tap command."""

        source_name: str
        config_file: str | None
        catalog_file: str | None
        state_file: str | None
        discover: bool

    @runtime_checkable
    class CliDataSinkParams(Protocol):
        """Parameters required to translate one Singer target command."""

        sink_name: str
        config_file: str | None
        input_file: str | None

    @runtime_checkable
    class CliPipelineParams(Protocol):
        """Parameters required to translate one Singer pipeline command."""

        source_name: str
        sink_name: str
        source_config: str | None
        sink_config: str | None
        catalog_file: str | None
        state_file: str | None
        state_output_file: str | None

    @runtime_checkable
    class CliTransformationParams(Protocol):
        """Parameters required to translate one dbt command."""

        project_dir: str
        models: str | None
        select: str | None
        exclude: str | None
        full_refresh: bool

    @runtime_checkable
    class CommandExecutionResult(Protocol):
        """Normalized result returned by Meltano and dbt execution."""

        command: t.StrSequence
        success: bool
        exit_code: int
        output: str
        error: str
        execution_time: float

        def to_dict(self) -> t.MappingKV[str, t.Scalar | t.StrSequence]:
            """Return the public execution-result mapping."""
            ...

    @runtime_checkable
    class DataSinkConfig(Protocol):
        """Validated configuration required to construct a data sink."""

        sink_type: str
        connection_config: t.JsonMapping
        batch_size: int
        max_batches: int

    @runtime_checkable
    class DataSinkDefinition(Protocol):
        """Configured data-sink definition."""

        sink_name: str
        sink_type: str
        settings: t.ConfigurationMapping
        sink_schema: t.JsonMapping
        status: str

    @runtime_checkable
    class DataSinkInstance(Protocol):
        """Runtime data-sink instance."""

        sink_id: str | None
        sink_type: str
        adapter: t.JsonValue | None
        status: str
        batch_size: int
        sink_count: int

        @property
        def settings(self) -> FlextMeltanoProtocolsModels.DataSinkConfig:
            """Validated sink settings."""
            ...

    @runtime_checkable
    class DataSourceConfig(Protocol):
        """Validated configuration required to construct a data source."""

        source_type: str
        connection_config: t.JsonMapping
        stream_config: t.JsonMapping
        source_version: str

    @runtime_checkable
    class DataSourceInstance(Protocol):
        """Runtime data-source instance."""

        source_type: str
        adapter: t.JsonValue | None
        status: str
        discovered: bool
        metadata: t.ConfigurationMapping
        source_id: str

    @runtime_checkable
    class DbtManifestNode(Protocol):
        """Typed dbt manifest node used by project discovery."""

        name: str | None
        path: str | None
        description: str | None
        fqn: t.StrSequence
        resource_type: str

        @property
        def fqn_string(self) -> str:
            """Dot-separated fully qualified node name."""
            ...

    @runtime_checkable
    class DbtProjectInfo(Protocol):
        """Typed dbt project discovery result."""

        name: str
        dbt_version: str | None
        models_count: int
        tests_count: int

    @runtime_checkable
    class FetchRequest(Protocol):
        """Typed request sent to a consumer record fetcher."""

        stream_name: str
        config: t.JsonMapping

    @runtime_checkable
    class FetchResult(Protocol):
        """Typed records returned by a consumer record fetcher."""

        records: t.SequenceOf[t.JsonMapping]

    @runtime_checkable
    class SingerCatalogEntry(Protocol):
        """One stream entry in a Singer catalog."""

        tap_stream_id: str
        stream: str
        schema_definition: t.JsonMapping

    @runtime_checkable
    class SingerCatalog(Protocol):
        """Singer catalog containing typed stream entries."""

        @property
        def streams(
            self,
        ) -> t.SequenceOf[FlextMeltanoProtocolsModels.SingerCatalogEntry]:
            """Catalog stream entries."""
            ...

        def model_dump_json(
            self,
            *,
            indent: int | None = None,
            by_alias: bool | None = None,
        ) -> str:
            """Serialize the catalog at its JSON egress boundary."""
            ...

    @runtime_checkable
    class SingerSchemaMessage(Protocol):
        """Singer SCHEMA message."""

        stream: str
        schema_definition: t.JsonMapping
        key_properties: t.StrSequence
        bookmark_properties: t.StrSequence

    @runtime_checkable
    class SingerRecordMessage(Protocol):
        """Singer RECORD message."""

        stream: str
        record: t.JsonMapping
        time_extracted: str | None
        version: int | None

    @runtime_checkable
    class SingerStateMessage(Protocol):
        """Singer STATE message."""

        value: t.MutableJsonMapping

        def model_dump_json(self, *, indent: int | None = None) -> str:
            """Serialize the state at its JSON egress boundary."""
            ...

    @runtime_checkable
    class StreamDefinition(Protocol):
        """Validated stream discovered for a data source."""

        stream_name: str
        stream_schema: t.JsonMapping
        source_type: str
        status: str
        records_extracted: int

    @runtime_checkable
    class StreamSpec(Protocol):
        """Declarative Singer stream supplied by a consumer."""

        name: str
        json_schema: t.JsonMapping
        primary_keys: t.StrSequence
        replication_key: str | None

    @runtime_checkable
    class TapConfig(Protocol):
        """Validated tap configuration."""

        tap_type: str
        connection_config: t.JsonMapping
        stream_config: t.JsonMapping
        tap_version: str

    @runtime_checkable
    class TapInstance(Protocol):
        """Runtime tap instance."""

        tap_id: str | None
        tap_type: str
        adapter: t.JsonValue | None
        status: str

        @property
        def settings(self) -> FlextMeltanoProtocolsModels.TapConfig:
            """Validated tap settings."""
            ...

    @runtime_checkable
    class TapSpec(Protocol):
        """Declarative Singer tap supplied by a consumer."""

        tap_name: str
        config_jsonschema: t.JsonMapping

        @property
        def streams(self) -> t.SequenceOf[FlextMeltanoProtocolsModels.StreamSpec]:
            """Declared stream specifications."""
            ...

    @runtime_checkable
    class TargetConfig(Protocol):
        """Validated target configuration."""

        target_type: str
        connection_config: t.JsonMapping
        batch_size: int | None
        batch_wait_limit: float | None
        target_version: str

    @runtime_checkable
    class PipelineCreateInput(Protocol):
        """CLI input for pipeline creation."""

        pipeline_name: str
        config_json: str | None

    @runtime_checkable
    class PipelineRunInput(Protocol):
        """CLI input for pipeline execution."""

        pipeline_name: str
        args: t.StrSequence

    @runtime_checkable
    class PipelineNameInput(Protocol):
        """CLI input identifying one persisted pipeline."""

        pipeline_name: str

    @runtime_checkable
    class PipelineListInput(Protocol):
        """CLI input for listing persisted pipelines."""

    @runtime_checkable
    class PluginListInput(Protocol):
        """CLI input for listing plugins."""

        plugin_type: str | None

    @runtime_checkable
    class PluginInfoInput(Protocol):
        """CLI input identifying one plugin."""

        plugin_type: str
        plugin_name: str

    @runtime_checkable
    class PluginInstallInput(Protocol):
        """CLI input identifying a plugin installation request."""

        plugin_name: str

    @runtime_checkable
    class StatusShowInput(Protocol):
        """CLI input for showing Meltano status."""

    @runtime_checkable
    class StatusHealthInput(Protocol):
        """CLI input for probing Meltano health."""

    @runtime_checkable
    class DbtInput(Protocol):
        """CLI input for a dbt subcommand."""

        subcommand: str
        args: t.StrSequence

    @runtime_checkable
    class TapInput(Protocol):
        """CLI input for a tap operation."""

        operation: str | None
        args: t.StrSequence

    @runtime_checkable
    class TargetInput(Protocol):
        """CLI input for a target operation."""

        operation: str | None
        args: t.StrSequence

    @runtime_checkable
    class VersionInput(Protocol):
        """CLI input for rendering the FLEXT Meltano version."""


__all__: list[str] = ["FlextMeltanoProtocolsModels"]
