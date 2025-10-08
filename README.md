## AlpacaTrading

A Python-based automated trading bot built around the Alpaca Markets API.  
Designed for live and paper trading with daily position management, trade logging, and configurable risk controls.

---

## Features
- Connects securely to **Alpaca Trading API** (live or paper)
- Automated **buy/sell execution** using custom strategies
- **Daily trade restriction** and position management logic
- Configurable **take-profit / stop-loss**
- Exports trade logs and order data for analysis
- Modular design (`account/`, `auth/`, `data/`, `order/`, `research/`, `utils/`)

---

## Tech Stack
- **Python 3.11+**
- **Alpaca-py SDK**
- **Pandas / NumPy**
- **Matplotlib** for quick data visualization
- **dotenv** for secure API key management

---

## Setup
1. **Clone the repo**
   ```bash
   git clone https://github.com/oroke24/AlpacaTrading.git
   cd AlpacaTrading
