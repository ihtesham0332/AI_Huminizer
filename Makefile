.PHONY: install start-engine start-ui start-all start-discord start-mobile docker-up docker-down clean

# Colors for terminal output
CYAN=\033[0;36m
GREEN=\033[0;32m
NC=\033[0m # No Color

install:
	@echo "$(CYAN)Installing backend dependencies...$(NC)"
	cd humantext-engine && pip install -r requirements.txt
	@echo "$(CYAN)Installing frontend dependencies...$(NC)"
	cd humantext-ui && npm install
	@echo "$(CYAN)Installing mobile dependencies...$(NC)"
	cd humantext-mobile && npm install
	@echo "$(GREEN)All dependencies installed!$(NC)"

start-engine:
	@echo "$(CYAN)Starting FastAPI Engine...$(NC)"
	cd humantext-engine && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

start-ui:
	@echo "$(CYAN)Starting Next.js UI...$(NC)"
	cd humantext-ui && npm run dev

start-all:
	@echo "$(GREEN)Starting entire local stack...$(NC)"
	# Run engine in background, then run UI
	cd humantext-engine && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 & \
	cd humantext-ui && npm run dev

start-discord:
	@echo "$(CYAN)Starting Discord Bot...$(NC)"
	cd humantext-discord && python bot.py

start-mobile:
	@echo "$(CYAN)Starting Expo Mobile Server...$(NC)"
	cd humantext-mobile && npm start

docker-up:
	@echo "$(GREEN)Deploying Docker stack...$(NC)"
	docker compose up --build -d

docker-down:
	@echo "$(CYAN)Tearing down Docker stack...$(NC)"
	docker compose down

clean:
	@echo "$(CYAN)Cleaning up monorepo cache and dependencies...$(NC)"
	find . -type d -name "node_modules" -exec rm -rf {} +
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".next" -exec rm -rf {} +
	find . -type d -name ".expo" -exec rm -rf {} +
	@echo "$(GREEN)Clean up complete!$(NC)"
