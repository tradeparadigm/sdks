from typing import Tuple

from friktion_swap_client.friktion_anchor.accounts.user_orders import UserOrders
from friktion_swap_client.friktion_anchor.program_id import PROGRAM_ID
from solana.publickey import PublicKey
from solana.rpc.async_api import AsyncClient


def find_swap_order_address(user: PublicKey, order_id: int) -> Tuple[PublicKey, int]:
    seeds = [str.encode("swapOrder"), bytes(user), order_id.to_bytes(8, byteorder="little")]
    return PublicKey.find_program_address(seeds, PROGRAM_ID)


def find_user_orders_address(user: PublicKey) -> Tuple[PublicKey, int]:
    user_orders_seeds = [str.encode("userOrders"), bytes(user)]
    return PublicKey.find_program_address(user_orders_seeds, PROGRAM_ID)


def find_give_pool_address(swap_order_addr: PublicKey) -> Tuple[PublicKey, int]:
    give_pool_seeds = [str.encode("givePool"), bytes(swap_order_addr)]
    return PublicKey.find_program_address(give_pool_seeds, PROGRAM_ID)


def find_receive_pool_address(swap_order_addr: PublicKey) -> Tuple[PublicKey, int]:
    receive_pool_seeds = [str.encode("receivePool"), bytes(swap_order_addr)]
    return PublicKey.find_program_address(receive_pool_seeds, PROGRAM_ID)


def find_delegate_authority_address() -> Tuple[PublicKey, int]:
    receive_pool_seeds = [str.encode("delegateAuthority")]
    return PublicKey.find_program_address(receive_pool_seeds, PROGRAM_ID)


DELEGATE_AUTHORITY_ADDRESS = find_delegate_authority_address()[0]


class SwapOrderAddresses:
    user_orders_address: PublicKey
    swap_order_address: PublicKey
    give_pool_address: PublicKey
    receive_pool_address: PublicKey
    delegate_authority_address: PublicKey

    def __init__(self, user: PublicKey, order_id: int = None, swap_order_address=None):
        self.user_orders_address = find_user_orders_address(user)[0]
        if order_id is not None:
            self.swap_order_address = find_swap_order_address(user, order_id)[0]
        elif swap_order_address is None:
            raise Exception("either order id or swap order address must be not None")
        else:
            self.swap_order_address = swap_order_address
        self.give_pool_address = find_give_pool_address(self.swap_order_address)[0]
        self.receive_pool_address = find_receive_pool_address(self.swap_order_address)[0]
        self.delegate_authority_address = find_delegate_authority_address()[0]

    @staticmethod
    async def from_user(
        client: AsyncClient, user: PublicKey, order_id: int = None
    ) -> 'SwapOrderAddresses':
        if order_id is None:
            user_orders_address = find_user_orders_address(user)[0]
            user_orders = await UserOrders.fetch(client, user_orders_address)
            if user_orders is None:
                order_id = 0
            else:
                order_id = user_orders.curr_order_id
        return SwapOrderAddresses(user, order_id)
