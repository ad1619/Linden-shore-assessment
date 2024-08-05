import requests
import json
from web3 import Web3

BSC_RPC_ENDPOINT = 'https://bsc-dataseed.binance.org/'

# Block range
START_BLOCK = 40784970
END_BLOCK = 40784980

# Initialize web3
w3 = Web3(Web3.HTTPProvider(BSC_RPC_ENDPOINT))

# Function to fetch transaction by hash
def fetch_transaction_by_hash(tx_hash):
    return w3.eth.getTransaction(tx_hash)

# Function to fetch transaction receipt by hash
def fetch_transaction_receipt(tx_hash):
    return w3.eth.getTransactionReceipt(tx_hash)

# Function to decode event logs
def decode_event_logs(logs):
    decoded_logs = []
    for log in logs:
        if log['topics'][0].hex() == '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef':
            # Transfer event
            decoded_logs.append({
                'type': 'Transfer',
                'from': Web3.toChecksumAddress('0x' + log['topics'][1].hex()[26:]),
                'to': Web3.toChecksumAddress('0x' + log['topics'][2].hex()[26:]),
                'value': int(log['data'], 16)
            })
        elif log['topics'][0].hex() == '0xd78ad95fa46c994b6551d0da85fc275fe613ce37657fb8d5e3d130840159d822':
            # Uniswap V2 Swap event
            decoded_logs.append({
                'type': 'Swap',
                'sender': Web3.toChecksumAddress('0x' + log['topics'][1].hex()[26:]),
                'amount0In': int(log['data'][2:66], 16),
                'amount1In': int(log['data'][66:130], 16),
                'amount0Out': int(log['data'][130:194], 16),
                'amount1Out': int(log['data'][194:258], 16),
                'to': Web3.toChecksumAddress('0x' + log['topics'][2].hex()[26:])
            })
    return decoded_logs

# Function to identify arbitrage trades
def identify_arbitrage_trades(decoded_logs):
    arbitrage_trades = []
    for log in decoded_logs:
        if log['type'] == 'Swap':
            for other_log in decoded_logs:
                if other_log['type'] == 'Swap' and log != other_log:
                    if log['amount0Out'] == other_log['amount0In'] and log['amount1In'] < other_log['amount1Out']:
                        arbitrage_trades.append({
                            'buy': log,
                            'sell': other_log,
                            'revenue': other_log['amount1Out'] - log['amount1In']
                        })
    return arbitrage_trades

# Function to calculate profit
def calculate_profit(arbitrage_trades):
    for trade in arbitrage_trades:
        trade['profit'] = trade['revenue'] - (trade['buy']['amount1In'] + trade['sell']['amount1Out'])
    return arbitrage_trades

def main():
    arbitrage_trades = []

    for block_number in range(START_BLOCK, END_BLOCK + 1):
        block = w3.eth.getBlock(block_number, full_transactions=True)
        for tx in block.transactions:
            tx_receipt = fetch_transaction_receipt(tx.hash)
            decoded_logs = decode_event_logs(tx_receipt.logs)
            arbitrage_trades.extend(identify_arbitrage_trades(decoded_logs))

    arbitrage_trades = calculate_profit(arbitrage_trades)
    for trade in arbitrage_trades:
        print(f"Arbitrage Trade: {trade}")

if __name__ == "__main__":
    main()
