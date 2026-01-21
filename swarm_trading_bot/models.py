"""
Data models for Swarm Vault API responses
"""
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
from datetime import datetime


@dataclass
class Token:
    """Represents a token with balance information"""
    address: str
    symbol: str
    name: str
    decimals: int
    balance: str
    logo_url: Optional[str] = None
    holder_count: Optional[int] = None
    total_balance: Optional[str] = None


@dataclass
class Holdings:
    """Aggregate holdings across swarm members"""
    eth_balance: str
    tokens: List[Token]
    member_count: int
    common_tokens: List[Dict[str, Any]]


@dataclass
class SwapPreviewMember:
    """Preview data for a single member's swap"""
    membership_id: str
    user_id: str
    user_wallet_address: str
    agent_wallet_address: str
    sell_amount: str
    buy_amount: str
    fee_amount: str
    estimated_price_impact: str
    error: Optional[str] = None


@dataclass
class SwapPreview:
    """Preview of a swap operation"""
    sell_token: str
    buy_token: str
    sell_percentage: float
    slippage_percentage: float
    members: List[SwapPreviewMember]
    total_sell_amount: str
    total_buy_amount: str
    total_fee_amount: str
    success_count: int
    error_count: int
    fee: Optional[Dict[str, Any]] = None


@dataclass
class Transaction:
    """Transaction status and details"""
    id: str
    swarm_id: str
    status: str  # PENDING, PROCESSING, COMPLETED, FAILED
    template: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    target_count: Optional[int] = None
    status_counts: Optional[Dict[str, int]] = None
    targets: Optional[List[Dict[str, Any]]] = None


@dataclass
class SwarmInfo:
    """Basic swarm information"""
    id: str
    name: str
    description: str
    member_count: int
    is_manager: bool
    managers: List[Dict[str, str]]


@dataclass
class ApiResponse:
    """Generic API response wrapper"""
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None
    error_code: Optional[str] = None
