# Vars
SRC = app/ tests/ alembic/  # Source code and test directories
RUFF = ruff
BLACK = black
ISORT = isort
PYTEST = pytest
COV_DIR = htmlcov
PYTHON = python
ALEMBIC = alembic


help:  ## Mostra as opções disponíveis no Makefile
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}'

start-test-containers: stop-dev-containers ## Inicia containers para testes locais
	docker compose up -d postgres-test

stop-test-containers: ## Termina containers para testes locais
	docker compose down postgres-test

start-dev-containers: stop-test-containers ## Inicia containers para testes locais
	docker compose up -d postgres-dev

stop-dev-containers: ## Termina containers para testes locais
	docker compose down postgres-dev

stop-all-containers: ## Termina todos os containers
	docker compose down postgres-dev postgres-test

lint: ## Formata o código com black, isort e ruff
	$(RUFF) format $(SRC)
	$(ISORT) $(SRC)
	$(BLACK) $(SRC)

check-lint: ## Verifica formatação com black, isort e ruff
	$(RUFF) check $(SRC)
	$(ISORT) --check $(SRC)
	$(BLACK) --check $(SRC)

test: start-test-containers  ## Executa os testes com pytest
	ENV=test $(PYTEST) $(SRC)

coverage:  ## Gera o relatório de cobertura de código
	ENV=test $(PYTEST) --cov=$(SRC) --cov-report=html:$(COV_DIR) --cov-report=term $(SRC)

clean:  ## Limpa arquivos temporários e relatórios
	rm -rf $(COV_DIR) .pytest_cache .coverage app.log
	find . -type d -name "__pycache__" -exec rm -rf {} +

migrate-up: ## Aplica migrações de banco de dados no banco de desenvolvimento
	ENV=dev $(ALEMBIC) upgrade head

run-dev: migrate-up start-dev-containers ## Executa a APP localmente na porta 8000
	ENV=dev $(PYTHON) run.py