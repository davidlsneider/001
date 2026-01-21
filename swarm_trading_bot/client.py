"""
Swarm Vault API Client

Wrapper around the Swarm Vault REST API for executing trades
and managing swarm operations.
"""
import requests
import time
from typing import Dict, Any, Optional, List
from .models import (
    Holdings, SwapPreview, Transaction, SwarmInfo,
    Token, SwapPreviewMember
)
from .logger import get_logger


class SwarmVaultClient:
    """Client for interacting with the Swarm Vault API"""

    def __init__(self, api_key: str, base_url: str = "https://api.swarmvault.xyz"):
        """
        Initialize Swarm Vault API client

        Args:
            api_key: API key starting with 'svk_'
            base_url: Base URL for the API
        """
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')
        self.logger = get_logger()
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make HTTP request to API

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint path
            data: Request body data
            params: Query parameters

        Returns:
            API response as dictionary

        Raises:
            requests.exceptions.RequestException: On API errors
        """
        url = f"{self.base_url}{endpoint}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            self.logger.error(f"HTTP error: {e}")
            self.logger.error(f"Response: {e.response.text if e.response else 'No response'}")
            raise
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Request error: {e}")
            raise

    # ==================== Authentication ====================

    def verify_api_key(self) -> Dict[str, Any]:
        """
        Verify API key and get user info

        Returns:
            User profile data
        """
        self.logger.debug("Verifying API key")
        result = self._request('GET', '/api/auth/me')
        return result.get('data', {})

    # ==================== Swarms ====================

    def get_swarm(self, swarm_id: str) -> SwarmInfo:
        """
        Get swarm details

        Args:
            swarm_id: Swarm ID

        Returns:
            SwarmInfo object
        """
        self.logger.debug(f"Getting swarm info: {swarm_id}")
        result = self._request('GET', f'/api/swarms/{swarm_id}')
        data = result.get('data', {})

        return SwarmInfo(
            id=data['id'],
            name=data['name'],
            description=data['description'],
            member_count=data['memberCount'],
            is_manager=data['isManager'],
            managers=data.get('managers', [])
        )

    def list_swarms(self) -> List[SwarmInfo]:
        """
        List all available swarms

        Returns:
            List of SwarmInfo objects
        """
        self.logger.debug("Listing all swarms")
        result = self._request('GET', '/api/swarms')
        swarms_data = result.get('data', [])

        return [
            SwarmInfo(
                id=s['id'],
                name=s['name'],
                description=s['description'],
                member_count=s['memberCount'],
                is_manager=s['isManager'],
                managers=s.get('managers', [])
            )
            for s in swarms_data
        ]

    # ==================== Holdings ====================

    def get_holdings(self, swarm_id: str) -> Holdings:
        """
        Get aggregate holdings across all swarm members

        Args:
            swarm_id: Swarm ID

        Returns:
            Holdings object with token balances
        """
        self.logger.debug(f"Getting holdings for swarm: {swarm_id}")
        result = self._request('GET', f'/api/swarms/{swarm_id}/holdings')
        data = result.get('data', {})

        tokens = [
            Token(
                address=t['address'],
                symbol=t['symbol'],
                name=t['name'],
                decimals=t['decimals'],
                balance=t.get('balance', '0'),
                total_balance=t.get('totalBalance'),
                holder_count=t.get('holderCount'),
                logo_url=t.get('logoUrl')
            )
            for t in data.get('tokens', [])
        ]

        return Holdings(
            eth_balance=data.get('ethBalance', '0'),
            tokens=tokens,
            member_count=data.get('memberCount', 0),
            common_tokens=data.get('commonTokens', [])
        )

    # ==================== Swaps ====================

    def preview_swap(
        self,
        swarm_id: str,
        sell_token: str,
        buy_token: str,
        sell_percentage: float = 100,
        slippage_percentage: float = 1.0
    ) -> SwapPreview:
        """
        Preview a swap without executing it

        Args:
            swarm_id: Swarm ID
            sell_token: Token address to sell (or 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE for ETH)
            buy_token: Token address to buy
            sell_percentage: Percentage of balance to sell (1-100)
            slippage_percentage: Slippage tolerance (0.01-50)

        Returns:
            SwapPreview object with expected outcomes
        """
        self.logger.info(
            f"Previewing swap: {sell_percentage}% of {sell_token} -> {buy_token} "
            f"(slippage: {slippage_percentage}%)"
        )

        data = {
            'sellToken': sell_token,
            'buyToken': buy_token,
            'sellPercentage': sell_percentage,
            'slippagePercentage': slippage_percentage
        }

        result = self._request('POST', f'/api/swarms/{swarm_id}/swap/preview', data=data)
        preview_data = result.get('data', {})

        members = [
            SwapPreviewMember(
                membership_id=m['membershipId'],
                user_id=m['userId'],
                user_wallet_address=m['userWalletAddress'],
                agent_wallet_address=m['agentWalletAddress'],
                sell_amount=m['sellAmount'],
                buy_amount=m['buyAmount'],
                fee_amount=m['feeAmount'],
                estimated_price_impact=m['estimatedPriceImpact'],
                error=m.get('error')
            )
            for m in preview_data.get('members', [])
        ]

        return SwapPreview(
            sell_token=preview_data['sellToken'],
            buy_token=preview_data['buyToken'],
            sell_percentage=preview_data['sellPercentage'],
            slippage_percentage=preview_data['slippagePercentage'],
            members=members,
            total_sell_amount=preview_data['totalSellAmount'],
            total_buy_amount=preview_data['totalBuyAmount'],
            total_fee_amount=preview_data['totalFeeAmount'],
            success_count=preview_data['successCount'],
            error_count=preview_data['errorCount'],
            fee=preview_data.get('fee')
        )

    def execute_swap(
        self,
        swarm_id: str,
        sell_token: str,
        buy_token: str,
        sell_percentage: float = 100,
        slippage_percentage: float = 1.0
    ) -> str:
        """
        Execute a swap for all swarm members

        Args:
            swarm_id: Swarm ID
            sell_token: Token address to sell
            buy_token: Token address to buy
            sell_percentage: Percentage of balance to sell (1-100)
            slippage_percentage: Slippage tolerance (0.01-50)

        Returns:
            Transaction ID for tracking execution status
        """
        self.logger.info(
            f"Executing swap: {sell_percentage}% of {sell_token} -> {buy_token}"
        )

        data = {
            'sellToken': sell_token,
            'buyToken': buy_token,
            'sellPercentage': sell_percentage,
            'slippagePercentage': slippage_percentage
        }

        result = self._request('POST', f'/api/swarms/{swarm_id}/swap/execute', data=data)
        execution_data = result.get('data', {})

        transaction_id = execution_data.get('transactionId')
        self.logger.info(f"Swap initiated. Transaction ID: {transaction_id}")

        return transaction_id

    # ==================== Transactions ====================

    def get_transaction(self, transaction_id: str) -> Transaction:
        """
        Get transaction status and details

        Args:
            transaction_id: Transaction ID

        Returns:
            Transaction object
        """
        self.logger.debug(f"Getting transaction status: {transaction_id}")
        result = self._request('GET', f'/api/transactions/{transaction_id}')
        data = result.get('data', {})

        return Transaction(
            id=data['id'],
            swarm_id=data['swarmId'],
            status=data['status'],
            template=data.get('template', {}),
            created_at=data['createdAt'],
            updated_at=data['updatedAt'],
            target_count=data.get('targetCount'),
            status_counts=data.get('statusCounts'),
            targets=data.get('targets', [])
        )

    def wait_for_transaction(
        self,
        transaction_id: str,
        timeout: int = 300,
        poll_interval: int = 5
    ) -> Transaction:
        """
        Wait for transaction to complete

        Args:
            transaction_id: Transaction ID to monitor
            timeout: Maximum wait time in seconds
            poll_interval: How often to check status (seconds)

        Returns:
            Completed Transaction object

        Raises:
            TimeoutError: If transaction doesn't complete within timeout
            RuntimeError: If transaction fails
        """
        self.logger.info(f"Waiting for transaction {transaction_id} to complete...")

        start_time = time.time()
        while True:
            tx = self.get_transaction(transaction_id)

            if tx.status == 'COMPLETED':
                self.logger.info(f"Transaction {transaction_id} completed successfully")
                return tx
            elif tx.status == 'FAILED':
                self.logger.error(f"Transaction {transaction_id} failed")
                raise RuntimeError(f"Transaction failed: {transaction_id}")

            elapsed = time.time() - start_time
            if elapsed > timeout:
                raise TimeoutError(
                    f"Transaction {transaction_id} did not complete within {timeout}s"
                )

            # Log progress
            if tx.status_counts:
                counts = tx.status_counts
                self.logger.info(
                    f"Progress: {counts.get('confirmed', 0)}/{tx.target_count} confirmed, "
                    f"{counts.get('failed', 0)} failed"
                )

            time.sleep(poll_interval)

    def list_swarm_transactions(self, swarm_id: str) -> List[Transaction]:
        """
        List all transactions for a swarm

        Args:
            swarm_id: Swarm ID

        Returns:
            List of Transaction objects
        """
        self.logger.debug(f"Listing transactions for swarm: {swarm_id}")
        result = self._request('GET', f'/api/swarms/{swarm_id}/transactions')
        tx_data = result.get('data', [])

        return [
            Transaction(
                id=tx['id'],
                swarm_id=tx['swarmId'],
                status=tx['status'],
                template=tx.get('template', {}),
                created_at=tx['createdAt'],
                updated_at=tx['updatedAt'],
                target_count=tx.get('targetCount'),
                status_counts=tx.get('statusCounts')
            )
            for tx in tx_data
        ]

    # ==================== Utility Methods ====================

    def format_amount(self, amount: str, decimals: int) -> float:
        """
        Convert token amount from wei to human-readable format

        Args:
            amount: Amount as string (wei)
            decimals: Token decimals

        Returns:
            Human-readable amount as float
        """
        return int(amount) / (10 ** decimals)

    def wei_to_eth(self, wei: str) -> float:
        """Convert wei to ETH"""
        return self.format_amount(wei, 18)

    def __repr__(self):
        return f"SwarmVaultClient(base_url={self.base_url})"
