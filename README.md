# Controle de Estoque Simples (CLI) – Python

Este repositório contém um sistema simples de **controle de estoque via linha de comando**, desenvolvido em Python.  
Ele permite cadastrar produtos, registrar entradas e saídas e manter o histórico em um arquivo JSON.

## Funcionalidades

- Cadastro de produtos (código, nome, quantidade inicial)
- Registro de **entradas** e **saídas** de estoque
- Validação para não permitir saída maior que o saldo disponível
- Listagem de produtos com saldo atualizado
- Armazenamento dos dados em `inventory.json` (sem banco de dados)

## Tecnologias

- Python 3
- Módulos padrão: `json`, `datetime`, `os`, `typing`

## Como executar

```bash
git clone https://github.com/SEU-USUARIO/NOME-DO-REPO.git
cd NOME-DO-REPO
python estoque_simples.py
