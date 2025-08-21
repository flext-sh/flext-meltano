"""Meltano ELT Real Execution - Pipelines ELT funcionais sem subprocess.

FUNÇÃO 1 & 2: Execução real de pipelines Meltano ELT
- MeltanoEltExecutor: Executa pipelines ELT reais usando APIs nativas
- Configuração de projetos temporários
- Instalação e execução de plugins reais
- Padrões .unwrap_or() para FlextResult
"""

from __future__ import annotations

import tempfile
import yaml
from pathlib import Path

import click.testing
from flext_core import FlextDomainService, FlextResult, get_logger
from meltano.cli import cli
from meltano.core.project import Project


class MeltanoEltExecutor(FlextDomainService[None]):
    """Executor de pipelines ELT reais usando Meltano nativo."""

    def __init__(self) -> None:
        super().__init__()

    @property 
    def logger(self):
        """Get logger instance."""
        return get_logger(__name__)

    def execute(self) -> FlextResult[None]:
        """Execute service operation."""
        return FlextResult.ok(None)

    def create_test_project(self, project_name: str = "test-elt") -> FlextResult[Path]:
        """Cria projeto Meltano temporário para testes ELT."""
        try:
            temp_dir = tempfile.mkdtemp(prefix=f'meltano_{project_name}_')
            temp_path = Path(temp_dir)
            
            # Configuração mínima com plugins reais do Hub
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
                            'files': [
                                {
                                    'path': 'sample.csv',
                                    'entity': 'sample_data'
                                }
                            ]
                        }
                    }],
                    'loaders': [{
                        'name': 'target-csv',
                        'namespace': 'target_csv', 
                        'pip_url': 'git+https://github.com/MeltanoLabs/target-csv.git',
                        'config': {
                            'destination_path': 'output'
                        }
                    }]
                }
            }
            
            # Salvar meltano.yml
            meltano_file = temp_path / 'meltano.yml'
            with meltano_file.open('w') as f:
                yaml.dump(meltano_config, f)
            
            # Criar dados de teste CSV
            sample_csv = temp_path / 'sample.csv' 
            with sample_csv.open('w') as f:
                f.write('id,name,category,value\\n')
                f.write('1,Product A,electronics,99.99\\n')
                f.write('2,Product B,books,19.99\\n')
                f.write('3,Product C,electronics,149.99\\n')
            
            self.logger.info("Test project created", path=str(temp_path))
            return FlextResult.ok(temp_path)
            
        except Exception as e:
            error_msg = f"Failed to create test project: {e}"
            self.logger.error(error_msg)
            return FlextResult.fail(error_msg)

    def install_plugins(self, project_path: Path) -> FlextResult[bool]:
        """Instala plugins do projeto usando meltano install."""
        try:
            runner = click.testing.CliRunner()
            
            with runner.isolated_filesystem():
                import os
                os.chdir(project_path)
                
                self.logger.info("Installing Meltano plugins", project=str(project_path))
                
                # Executar meltano install
                result = runner.invoke(cli, ['install'])
                
                if result.exit_code == 0:
                    self.logger.info("Plugins installed successfully")
                    return FlextResult.ok(True)
                else:
                    error_msg = f"Plugin installation failed: {result.output}"
                    self.logger.error(error_msg)
                    return FlextResult.fail(error_msg)
                    
        except Exception as e:
            error_msg = f"Installation error: {e}"
            self.logger.error(error_msg)
            return FlextResult.fail(error_msg)

    def run_elt_pipeline(self, project_path: Path, extractor: str, loader: str) -> FlextResult[dict[str, int]]:
        """Executa pipeline ELT real usando meltano elt."""
        try:
            runner = click.testing.CliRunner()
            
            with runner.isolated_filesystem():
                import os
                os.chdir(project_path)
                
                self.logger.info("Running ELT pipeline", 
                               extractor=extractor, loader=loader, project=str(project_path))
                
                # Executar meltano elt 
                result = runner.invoke(cli, ['elt', extractor, loader])
                
                if result.exit_code == 0:
                    # Verificar outputs
                    output_dir = project_path / 'output'
                    output_files = list(output_dir.glob('*')) if output_dir.exists() else []
                    
                    pipeline_result = {
                        "exit_code": result.exit_code,
                        "output_files": len(output_files),
                        "success": 1
                    }
                    
                    self.logger.info("ELT pipeline completed successfully", 
                                   output_files=len(output_files))
                    return FlextResult.ok(pipeline_result)
                else:
                    error_msg = f"ELT pipeline failed: {result.output}"
                    self.logger.error(error_msg)
                    return FlextResult.fail(error_msg)
                    
        except Exception as e:
            error_msg = f"ELT execution error: {e}"
            self.logger.error(error_msg)
            return FlextResult.fail(error_msg)

    def test_plugin_discovery(self, project_path: Path, plugin_name: str) -> FlextResult[dict[str, str]]:
        """Testa descoberta de schema do plugin.""" 
        try:
            runner = click.testing.CliRunner()
            
            with runner.isolated_filesystem():
                import os
                os.chdir(project_path)
                
                self.logger.info("Testing plugin discovery", plugin=plugin_name)
                
                # Executar discover
                result = runner.invoke(cli, ['invoke', f'{plugin_name}:discover'])
                
                discovery_result = {
                    "plugin": plugin_name,
                    "exit_code": str(result.exit_code), 
                    "has_output": str(bool(result.output.strip())),
                    "status": "success" if result.exit_code == 0 else "failed"
                }
                
                if result.exit_code == 0:
                    self.logger.info("Plugin discovery successful", plugin=plugin_name)
                    return FlextResult.ok(discovery_result)
                else:
                    self.logger.warning("Plugin discovery failed", plugin=plugin_name, 
                                      output=result.output[:200])
                    return FlextResult.ok(discovery_result)  # Ainda retorna resultado
                    
        except Exception as e:
            error_msg = f"Discovery test error: {e}"
            self.logger.error(error_msg)
            return FlextResult.fail(error_msg)


# Função utilitária usando .unwrap_or() pattern
def execute_real_elt_pipeline() -> dict[str, int]:
    """Executa pipeline ELT completo usando padrões .unwrap_or()."""
    executor = MeltanoEltExecutor()
    
    # Criar projeto (usando .unwrap_or() para fallback)
    project_path = executor.create_test_project().unwrap_or(Path.cwd())
    
    # Instalar plugins (usando .unwrap_or() para fallback)
    install_success = executor.install_plugins(project_path).unwrap_or(False)
    
    if install_success:
        # Executar ELT (usando .unwrap_or() para fallback) 
        elt_result = executor.run_elt_pipeline(project_path, 'tap-csv', 'target-csv').unwrap_or({
            "exit_code": -1,
            "output_files": 0, 
            "success": 0
        })
        return elt_result
    else:
        return {"exit_code": -1, "output_files": 0, "success": 0}


# =============================================================================
# PUBLIC API EXPORTS
# =============================================================================

__all__ = ["MeltanoEltExecutor", "execute_real_elt_pipeline"]