

# AI Stock Trading Simulator

Welcome to the AI Stock Trading Simulator! This project simulates a stock trading platform powered by AI, allowing users to make trades, manage a portfolio, and track virtual investments. It uses AI to analyze trends and provide trading suggestions, creating a fun and interactive way to explore the stock market without real financial risk.

----------

## Features

1.  **AI-Powered Trading Suggestions**  
    The GPT-4o-mini model processes trends and data to provide actionable insights for trading.
    
2.  **Simulated Stock Data**  
    The system uses predefined or simulated stock data to mimic real-world market scenarios.
    
3.  **Portfolio Management**
    
    -   Simulate buying and selling stocks.
    -   Track your portfolio balance and holdings.
4.  **JSON Data Persistence**  
    Portfolio and account details are stored in  `account_data.json`, ensuring data is retained between sessions.
    

----------

## Installation

1.  **Clone the Repository**
    

    
    `git clone https://github.com/EvanMeyer36/AI-Stock-Simulator.git`
    
    `cd AI-Stock-Simulator ` 
    
3.  **Install Dependencies**  
    Make sure you have Python 3.8+ installed, then run:

    `pip install -r requirements.txt` 
    
4. **Create ENV**
   Make sure to create a .env file and include your OpenAI API key:

   `OPENAI_API_KEY=<KEY>`  *Repace **< KEY >** with your key.*

----------

## Usage

1.  **Start the Simulator**  
    Run the main script to start the simulation:
    
    `python main.py` 
    
2.  **Manage Your Portfolio**
    
    -   Add or withdraw virtual funds.
    -   Buy or sell stocks.
    -   View your portfolio's current balance and holdings.
3.  **AI Trading Suggestions**  
    Use AI features to get stock trading advice based on simulated market data.
    

----------

## File Structure

-   **`main.py`**: The entry point for the simulation. Handles user interactions and main logic.
-   **`account_manager.py`**: Manages account data, including balance and holdings.
-   **`ai_utils.py`**: Contains AI-related functionalities for generating trading suggestions.
-   **`market_utils.py`**: Simulates stock market data and handles stock trading operations.
-   **`account_data.json`**: Stores user account and portfolio details for persistence.

----------

## Future Enhancements

-   Integration with real-time stock data APIs (optional).
-   More advanced AI models for dynamic trading strategies.
-   Enhanced data visualization for portfolio performance.

----------

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests with your ideas or improvements.

----------

## License

This project is licensed under the MIT License. See the  `LICENSE`  file for details
