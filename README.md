Code: 
In the provided file: assessment.py

Explanation:
The program connects to the Binance Smart Chain (BSC) using the Web3 library and fetches transactions and their receipts for the specified block range (40784970 - 40784980).
It also decodes Transfer and Swap event logs using their signature hashes. Then, it identifies potential arbitrage trades by checking if there are swaps involving buying and selling the same token on different pools within the same transaction.
Finally, we calculate the revenue and profit for each identified arbitrage trade.

Results
The program prints each identified arbitrage trade along with its details, including the buy and sell logs, revenue, and profit.
