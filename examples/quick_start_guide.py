#!/usr/bin/env python3
"""FLEXT Meltano - Quick Start Guide.

Guia completo para começar rapidamente com a nova API ultra-simplificada.
Cada exemplo é funcional e pode ser executado independentemente.
"""

from __future__ import annotations

import asyncio
import datetime

from flext_meltano import (
    BatchProcessor,
    FlextMeltano,
    MeltanoProject,
    PipelineSpec,
    PluginSpec,
    async_run_pipeline,
    batch_process_tables,
    discover_catalog,
    run_pipeline,
    setup_project,
    test_tap_connection,
)

# ============================================================================
# 🚀 QUICK START - Primeiros Passos
# ============================================================================

def quick_start_basic() -> None:
    """Quick Start - Pipeline básico em 1 linha."""
    # ✨ UMA LINHA substitui 50+ linhas de código manual
    run_pipeline("tap-csv", "target-csv")



def quick_start_with_configuration() -> None:
    """Quick Start - Com configuração customizada."""
    # 🏗️ Setup com auto-instalação de plugins
    fm = FlextMeltano(
        project_root="/tmp/my_project",
        environment="dev",
        auto_install=True,  # Instala plugins automaticamente
    )

    # 🔧 Execução com configuração específica
    result = fm.run(
        "tap-postgres",
        "target-csv",
        select=["users", "orders"],  # Apenas tabelas específicas
        full_refresh=True,           # Ignorar estado anterior
    )

    if result.success:
        pass
    else:
        pass


# ============================================================================
# 📋 SETUP COMPLETO - Projeto Enterprise
# ============================================================================

def enterprise_project_setup() -> None:
    """Setup completo de projeto enterprise em 3 linhas."""
    # 🏢 SETUP ENTERPRISE COMPLETO - 3 linhas vs 100+ manuais
    result = setup_project(
        "/tmp/enterprise_project",
        # 🔌 Plugins com configuração
        plugins=[
            PluginSpec("tap-postgres", "extractor", config={
                "host": "prod-db.company.com",
                "port": 5432,
                "database": "production",
                "username": "etl_user",
            }),
            PluginSpec("target-postgres", "loader", config={
                "host": "warehouse.company.com",
                "database": "warehouse",
            }),
            PluginSpec("dbt-postgres", "transformer"),
            PluginSpec("tap-csv", "extractor"),  # Para dados auxiliares
        ],
        # 📊 Pipelines com agendamento
        pipelines=[
            PipelineSpec(
                "daily_full_etl",
                "tap-postgres",
                "target-postgres",
                transform="dbt-postgres:run",
                schedule="@daily",
                select=["users", "orders", "products"],
            ),
            PipelineSpec(
                "hourly_incremental",
                "tap-postgres",
                "target-postgres",
                schedule="0 * * * *",
                select=["events", "user_sessions"],
            ),
        ],
    )

    if result.success:
        pass
    else:
        pass


# ============================================================================
# 🔄 PROCESSAMENTO EM LOTE - Múltiplas Tabelas
# ============================================================================

def batch_processing_example() -> None:
    """Processamento batch ultra-simplificado."""
    # 📋 Lista de tabelas para processar
    tables = [
        "customers", "orders", "order_items", "products",
        "categories", "suppliers", "inventory", "shipments",
    ]

    # 🔄 PROCESSAMENTO BATCH - 1 linha vs 60+ linhas manuais
    results = batch_process_tables(
        "/tmp/warehouse_project",
        "tap-postgres",
        "target-warehouse",
        tables,
    )

    # 📊 Análise de resultados
    sum(results.values())
    len(results)
    failed_tables = [table for table, success in results.items() if not success]

    if failed_tables:
        pass


def advanced_batch_processing() -> None:
    """Processamento batch avançado com controle granular."""
    # 🎛️ Processor com configuração avançada
    processor = BatchProcessor(
        "/tmp/advanced_project",
        environment="prod",
    )

    # 📋 Diferentes grupos de tabelas
    critical_tables = ["users", "orders", "payments"]
    audit_tables = ["user_sessions", "events", "logs"]
    reference_tables = ["products", "categories", "suppliers"]

    # 🔄 Processamento sequencial para tabelas críticas
    critical_results = processor.process_tables(
        "tap-postgres", "target-warehouse", critical_tables,
        parallel=False,  # Sequencial para garantir ordem
    )

    # ⚡ Processamento paralelo para tabelas de auditoria
    audit_results = processor.process_tables(
        "tap-postgres", "target-warehouse", audit_tables,
        parallel=True, max_workers=3,
    )

    # 🧹 Limpeza de estados antes de reprocessar referências
    processor.reset_all_states("tap-postgres")

    # 📊 Processamento de referências
    ref_results = processor.process_tables(
        "tap-postgres", "target-warehouse", reference_tables,
    )

    # 📈 Consolidação de resultados
    all_results = {**critical_results, **audit_results, **ref_results}
    sum(r.success for r in all_results.values()) / len(all_results)



# ============================================================================
# 🔍 DESCOBERTA E VALIDAÇÃO - Exploração de Dados
# ============================================================================

def data_discovery_workflow() -> None:
    """Workflow completo de descoberta de dados."""
    project_root = "/tmp/discovery_project"

    # 🔌 Teste de conectividade - 1 linha
    if not test_tap_connection("tap-postgres", project_root=project_root):
        return


    # 🗂️ Descoberta de catálogo - 1 linha
    catalog = discover_catalog("tap-postgres", project_root=project_root)

    # 📊 Análise do catálogo
    streams = catalog.get("streams", [])

    # 🔍 Detalhes das tabelas principais
    for stream in streams[:10]:  # Primeiras 10 tabelas
        stream.get("tap_stream_id", "unknown")
        schema = stream.get("schema", {})
        properties = schema.get("properties", {})
        len(properties)

        # Identificar tipos de campos principais
        field_types = [prop.get("type", "unknown") for prop in properties.values()]
        {t: field_types.count(t) for t in set(field_types)}


    # 🎯 Setup automático baseado na descoberta
    fm = FlextMeltano(project_root=project_root)

    # 📈 Teste de extração com tabelas pequenas primeiro
    small_tables = [s["tap_stream_id"] for s in streams[:3]]  # Primeiras 3 tabelas

    for table in small_tables:
        result = fm.run(
            "tap-postgres", "target-csv",
            select=[table],
            dry_run=True,  # Apenas validação
        )

        if result.success:
            pass
        else:
            pass


# ============================================================================
# ⚡ PIPELINES ASSÍNCRONOS - Alta Performance
# ============================================================================

async def async_pipeline_workflow() -> None:
    """Workflow assíncrono para máxima performance."""
    project_root = "/tmp/async_project"

    # 🚀 MÚLTIPLOS PIPELINES CONCORRENTES - 3 linhas vs 50+ manuais
    tasks = [
        async_run_pipeline("tap-postgres", "target-csv", project_root=project_root),
        async_run_pipeline("tap-csv", "target-postgres", project_root=project_root),
        async_run_pipeline("tap-api", "target-warehouse", project_root=project_root),
    ]

    # ⏱️ Execução paralela com timeout
    try:
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=300,  # 5 minutos máximo
        )

        # 📊 Análise de resultados paralelos
        for _i, result in enumerate(results):
            if isinstance(result, Exception):
                pass
            else:
                pass

    except TimeoutError:
        pass


# ============================================================================
# 🏥 MONITORAMENTO E DIAGNÓSTICO - Health Checks
# ============================================================================

def health_monitoring_example() -> None:
    """Sistema completo de monitoramento de saúde."""
    project = MeltanoProject("/tmp/production_project")

    # 🏥 HEALTH CHECK COMPLETO - 1 linha vs 40+ manuais
    health = project.health_check()

    # 📊 Dashboard de saúde

    if health["healthy"]:
        pass
    else:
        pass

    # 🔌 Status de plugins
    plugins = health.get("plugins", {})

    # 🌍 Ambientes configurados
    environments = health.get("environments", [])

    # 🗄️ Status do banco
    database = health.get("database", {})
    "✅ Configurado" if database.get("configured") else "❌ Não configurado"

    # 🔔 Alertas automáticos
    if not health["healthy"]:
        for issue in health["issues"]:
            if "CLI" in issue or "Database" in issue or "plugins" in issue:
                pass

    # 📈 Recomendações de performance
    plugin_count = sum(plugins.values())
    if plugin_count > 10:
        pass

    env_count = len(environments)
    if env_count < 3:
        pass


# ============================================================================
# 💾 BACKUP E RECUPERAÇÃO - Gestão de Projeto
# ============================================================================

def backup_and_recovery_example() -> None:
    """Sistema completo de backup e recuperação."""
    project = MeltanoProject("/tmp/critical_project")

    # 📅 Backup com timestamp
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = f"/backups/meltano_project_{timestamp}"

    # 💾 BACKUP COMPLETO - 1 linha vs 30+ manuais
    backup_result = project.backup_project(backup_path)

    if backup_result.success:

        # 📊 Informações do backup
        pass

    else:
        pass

    # 🏥 Backup com verificação de saúde
    health = project.health_check()
    if health["healthy"]:
        pass
    else:
        pass


# ============================================================================
# 🎯 WORKFLOWS ESPECÍFICOS - Casos de Uso Reais
# ============================================================================

def real_world_etl_workflow() -> None:
    """Workflow ETL real - E-commerce para Data Warehouse."""
    # 🏪 Cenário: E-commerce pipeline

    fm = FlextMeltano("/tmp/ecommerce_project", environment="prod")

    # 1️⃣ DADOS CRÍTICOS (sequencial para garantir consistência)
    critical_tables = ["customers", "orders", "payments"]

    for table in critical_tables:
        fm.run(
            "tap-postgres-prod", "target-warehouse",
            select=[table],
            full_refresh=False,  # Incremental para performance
        )

    # 2️⃣ DADOS AUXILIARES (paralelo para velocidade)
    processor = BatchProcessor("/tmp/ecommerce_project", environment="prod")

    auxiliary_tables = [
        "products", "categories", "suppliers", "inventory",
        "shipping_zones", "tax_rules", "promotions",
    ]

    aux_results = processor.process_tables(
        "tap-postgres-prod", "target-warehouse", auxiliary_tables,
        parallel=True, max_workers=3,
    )

    aux_success = sum(aux_results.values())

    # 3️⃣ DADOS DE ANALYTICS (batch otimizado)
    analytics_tables = [
        "user_sessions", "page_views", "search_queries",
        "cart_events", "conversion_events", "email_opens",
    ]

    analytics_results = processor.process_tables(
        "tap-analytics", "target-warehouse", analytics_tables,
        parallel=True, max_workers=2,  # Menos workers para não sobrecarregar
    )

    analytics_success = sum(analytics_results.values())

    # 4️⃣ TRANSFORMAÇÕES DBT
    fm.run(
        "dbt-warehouse", "dbt-warehouse",  # DBT plugin especial
        select=["marts", "staging"],
    )

    # 📊 RESUMO FINAL
    total_tables = len(critical_tables) + len(auxiliary_tables) + len(analytics_tables)
    total_success = 3 + aux_success + analytics_success  # Critical + aux + analytics
    success_rate = (total_success / total_tables) * 100


    if success_rate >= 95 or success_rate >= 80:
        pass
    else:
        pass


# ============================================================================
# 🎮 DEMO INTERATIVO - Teste das Funcionalidades
# ============================================================================

def interactive_demo() -> None:
    """Demo interativo para testar funcionalidades."""
    examples = {
        "1": ("Pipeline Básico (1 linha)", quick_start_basic),
        "2": ("Setup Enterprise (3 linhas)", enterprise_project_setup),
        "3": ("Batch Processing (1 linha)", batch_processing_example),
        "4": ("Descoberta de Dados", data_discovery_workflow),
        "5": ("Health Check (1 linha)", health_monitoring_example),
        "6": ("ETL Real E-commerce", real_world_etl_workflow),
    }

    for _key, (_description, _) in examples.items():
        pass



# ============================================================================
# 🚀 EXECUÇÃO DOS EXEMPLOS
# ============================================================================

if __name__ == "__main__":
    # 🎮 Demo interativo
    interactive_demo()


    # Descomente os exemplos que quiser testar:

    # 🚀 Quick Start
    # quick_start_basic()
    # quick_start_with_configuration()

    # 🏢 Enterprise Setup
    # enterprise_project_setup()

    # 🔄 Batch Processing
    # batch_processing_example()
    # advanced_batch_processing()

    # 🔍 Data Discovery
    # data_discovery_workflow()

    # ⚡ Async (requires: asyncio.run(async_pipeline_workflow()))
    # import asyncio
    # asyncio.run(async_pipeline_workflow())

    # 🏥 Health Monitoring
    # health_monitoring_example()

    # 💾 Backup & Recovery
    # backup_and_recovery_example()

    # 🏪 Real World ETL
    # real_world_etl_workflow()

