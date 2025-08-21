"""Simple Executors - Executores Meltano e DBT sem dependência do flext-core.

FUNÇÃO 2: Runtime execution via Go bridge - Versão simplificada
- SimpleMeltanoExecutor: ELT pipelines reais usando APIs nativas
- SimpleDbtExecutor: DBT commands reais usando dbtRunner nativo  
- SimpleResult: Pattern similar ao FlextResult

Demonstra execução real sem subprocess, usando:
- Meltano 3.9.1 nativo via click.testing.CliRunner
- DBT Core 1.10.5 nativo via dbtRunner
- .unwrap_or() patterns
"""

from __future__ import annotations

import tempfile
import yaml
import os
from pathlib import Path
from typing import TypeVar, Generic

import click.testing
from meltano.cli import main as meltano_cli
from dbt.cli.main import dbtRunner

T = TypeVar("T")


class SimpleResult(Generic[T]):
    """Versão simplificada do FlextResult para demonstração."""
    
    def __init__(self, success: bool, value: T | None = None, error: str | None = None):
        self.success = success
        self.value = value  
        self.error_message = error
    
    @classmethod
    def ok(cls, value: T) -> SimpleResult[T]:
        return cls(True, value, None)
    
    @classmethod  
    def fail(cls, error: str) -> SimpleResult[T]:
        return cls(False, None, error)
    
    def unwrap_or(self, default: T) -> T:
        return self.value if self.success and self.value is not None else default


class SimpleMeltanoExecutor:
    """Executor ELT simples usando Meltano nativo."""
    
    def create_test_project(self, project_name: str = "simple_test") -> SimpleResult[Path]:
        """Cria projeto Meltano temporário."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=f'meltano_{project_name}_')
            temp_path = Path(temp_dir)
            
            # Configuração mínima com plugins reais
            meltano_config = {
                'version': 1,
                'project_id': project_name,
                'environments': [{'name': 'dev'}],
                'plugins': {
                    'extractors': [{
                        'name': 'tap-csv',
                        'namespace': 'tap_csv',
                        'pip_url': 'git+https://github.com/MeltanoLabs/tap-csv.git',
                        'config': {
                            'files': [{'path': 'test.csv', 'entity': 'test_data'}]
                        }
                    }],
                    'loaders': [{
                        'name': 'target-csv',
                        'namespace': 'target_csv', 
                        'pip_url': 'git+https://github.com/MeltanoLabs/target-csv.git',
                        'config': {'destination_path': 'output'}
                    }]
                }
            }
            
            # Salvar meltano.yml
            meltano_file = temp_path / 'meltano.yml'
            with meltano_file.open('w') as f:
                yaml.dump(meltano_config, f)
            
            # Criar dados de teste
            test_csv = temp_path / 'test.csv'
            with test_csv.open('w') as f:
                f.write('id,name,value\\n')
                f.write('1,test1,100\\n')
                f.write('2,test2,200\\n')
            
            print(f"✅ Projeto Meltano criado em: {temp_path}")
            return SimpleResult.ok(temp_path)
            
        except Exception as e:
            return SimpleResult.fail(f"Erro ao criar projeto: {e}")

    def run_elt_pipeline(
        self, project_path: Path, extractor: str, loader: str
    ) -> SimpleResult[dict[str, str]]:
        """Executa pipeline ELT real usando meltano CLI nativo."""
        try:
            runner = click.testing.CliRunner()
            
            with runner.isolated_filesystem():
                os.chdir(project_path)
                
                print(f"🚀 Executando ELT: {extractor} → {loader}")
                
                # Executar meltano elt usando API nativa
                result = runner.invoke(meltano_cli, ['elt', extractor, loader])
                
                if result.exit_code == 0:
                    # Verificar outputs
                    output_dir = project_path / 'output'
                    output_files = list(output_dir.glob('*')) if output_dir.exists() else []
                    
                    pipeline_result = {
                        "success": "true",
                        "exit_code": str(result.exit_code),
                        "output_files": str(len(output_files)),
                        "extractor": extractor,
                        "loader": loader
                    }
                    
                    print(f"✅ Pipeline ELT concluído: {len(output_files)} arquivos gerados")
                    return SimpleResult.ok(pipeline_result)
                else:
                    error_result = {
                        "success": "false", 
                        "exit_code": str(result.exit_code),
                        "error": result.output[:200],
                        "extractor": extractor,
                        "loader": loader
                    }
                    return SimpleResult.ok(error_result)  # Still return result for analysis
                    
        except Exception as e:
            return SimpleResult.fail(f"Erro na execução ELT: {e}")


class SimpleDbtExecutor:
    """Executor DBT simples usando dbtRunner nativo."""
    
    def create_test_dbt_project(self, project_name: str = "simple_dbt") -> SimpleResult[Path]:
        """Cria projeto DBT temporário."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=f'dbt_{project_name}_')
            temp_path = Path(temp_dir)
            
            # Criar dbt_project.yml
            dbt_project_config = {
                'name': project_name,
                'version': '1.0.0', 
                'profile': project_name,
                'model-paths': ['models'],
                'target-path': 'target',
                'models': {project_name: {'materialized': 'table'}}
            }
            
            dbt_project_file = temp_path / 'dbt_project.yml'
            with dbt_project_file.open('w') as f:
                yaml.dump(dbt_project_config, f)
            
            # Criar profiles.yml
            profiles_config = {
                project_name: {
                    'outputs': {
                        'dev': {
                            'type': 'sqlite',
                            'database': str(temp_path / 'test.db'),
                            'schema': 'main',
                            'schema_directory': str(temp_path),
                            'schemas_and_paths': {'main': str(temp_path / 'test.db')}
                        }
                    },
                    'target': 'dev'
                }
            }
            
            profiles_file = temp_path / 'profiles.yml'
            with profiles_file.open('w') as f:
                yaml.dump(profiles_config, f)
            
            # Criar estrutura de diretórios
            (temp_path / 'models').mkdir()
            
            # Criar modelo de teste
            test_model = temp_path / 'models' / 'test_model.sql'
            with test_model.open('w') as f:
                f.write("""
                SELECT 
                    1 as id,
                    'test' as name,
                    datetime('now') as created_at
                UNION ALL
                SELECT 
                    2 as id,
                    'test2' as name, 
                    datetime('now') as created_at
                """)
            
            print(f"✅ Projeto DBT criado em: {temp_path}")
            return SimpleResult.ok(temp_path)
            
        except Exception as e:
            return SimpleResult.fail(f"Erro ao criar projeto DBT: {e}")

    def run_dbt_command(
        self, project_path: Path, command: list[str]
    ) -> SimpleResult[dict[str, str]]:
        """Executa comando DBT usando dbtRunner nativo."""
        try:
            runner = dbtRunner()
            
            # Adicionar project-dir e profiles-dir
            full_command = command + [
                '--project-dir', str(project_path),
                '--profiles-dir', str(project_path)
            ]
            
            print(f"🚀 Executando DBT: {' '.join(command)}")
            
            # Executar comando DBT real
            result = runner.invoke(full_command)
            
            command_result = {
                "command": " ".join(command),
                "success": str(getattr(result, 'success', False)),
                "project_path": str(project_path)
            }
            
            if getattr(result, 'success', False):
                print(f"✅ Comando DBT executado com sucesso: {' '.join(command)}")
                return SimpleResult.ok(command_result)
            else:
                print(f"⚠️ Comando DBT falhou: {' '.join(command)}")
                return SimpleResult.ok(command_result)  # Still return for analysis
                
        except Exception as e:
            return SimpleResult.fail(f"Erro na execução DBT: {e}")


# =============================================================================
# UTILITY FUNCTIONS WITH .unwrap_or() PATTERNS
# =============================================================================

def execute_simple_elt_workflow() -> dict[str, str]:
    """Executa workflow ELT completo usando .unwrap_or() patterns."""
    executor = SimpleMeltanoExecutor()
    
    # Criar projeto (com fallback)
    project_path = executor.create_test_project().unwrap_or(Path.cwd())
    
    # Executar ELT (com fallback)
    elt_result = executor.run_elt_pipeline(
        project_path, 'tap-csv', 'target-csv'
    ).unwrap_or({
        "success": "false", 
        "exit_code": "-1", 
        "output_files": "0",
        "error": "fallback_triggered"
    })
    
    return elt_result


def execute_simple_dbt_workflow() -> dict[str, str]:
    """Executa workflow DBT completo usando .unwrap_or() patterns.""" 
    executor = SimpleDbtExecutor()
    
    # Criar projeto (com fallback)
    project_path = executor.create_test_dbt_project().unwrap_or(Path.cwd())
    
    # Parse do projeto (com fallback)
    parse_result = executor.run_dbt_command(project_path, ['parse']).unwrap_or({
        "success": "false", "command": "parse"
    })
    
    if parse_result["success"] == "true":
        # Run (com fallback)
        run_result = executor.run_dbt_command(project_path, ['run']).unwrap_or({
            "success": "false", "command": "run"
        })
        
        return {
            "workflow": "complete",
            "parse": parse_result["success"], 
            "run": run_result["success"]
        }
    else:
        return {"workflow": "stopped_at_parse", "parse": "false"}


# =============================================================================
# TESTING FUNCTIONS
# =============================================================================

def test_simple_executors() -> None:
    """Testa os executores simples."""
    print("🧪 Testing Simple Meltano & DBT Executors...")
    
    print("\\n=== TESTE MELTANO ELT ===")
    try:
        result = execute_simple_elt_workflow()
        print(f"✅ Resultado ELT: {result}")
    except Exception as e:
        print(f"❌ Erro ELT: {e}")
    
    print("\\n=== TESTE DBT ===")
    try:
        result = execute_simple_dbt_workflow()
        print(f"✅ Resultado DBT: {result}")
    except Exception as e:
        print(f"❌ Erro DBT: {e}")
        
    print("\\n🎉 Testes de executores simples concluídos!")


if __name__ == "__main__":
    test_simple_executors()


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = [
    "SimpleMeltanoExecutor",
    "SimpleDbtExecutor", 
    "SimpleResult",
    "execute_simple_elt_workflow",
    "execute_simple_dbt_workflow"
]