# FLEXT Meltano

Camada de orquestracao Singer/Meltano para coordenar extracao, carga e transformacao em pipelines FLEXT.

Descricao oficial atual: "FLEXT Meltano - Enterprise Data Integration Platform".

## O que este projeto entrega

- Executa jobs de tap/target sob agenda operacional.
- Padroniza integracao entre conectores e dbt.
- Apoia operacao recorrente de pipelines de dados.

## Contexto operacional

- Entrada: definicao de jobs, taps, targets e schedule.
- Saida: pipelines executados com trilha operacional.
- Dependencias: conectores Singer e ambientes de dados conectados.

## Estado atual e risco de adocao

- Qualidade: **Alpha**
- Uso recomendado: **Nao produtivo**
- Nivel de estabilidade: em maturacao funcional e tecnica, sujeito a mudancas de contrato sem garantia de retrocompatibilidade.

## Diretriz para uso nesta fase

Aplicar este projeto somente em desenvolvimento, prova de conceito e homologacao controlada, com expectativa de ajustes frequentes ate maturidade de release.
