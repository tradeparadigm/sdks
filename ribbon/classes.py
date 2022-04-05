from dataclasses import dataclass

@dataclass
class Domain:
  """Domain parameters for signatures"""
  name: str
  chainId: int
  verifyingContract: str
  version: int
  salt: str = None

@dataclass
class Bid:
  """Bid parameters"""
  swapId: int
  nonce: int
  signerWallet: str
  sellAmount: int
  buyAmount: int
  referrer: str

@dataclass
class SignedBid(Bid):
  """Signed bid fields"""
  v: int
  r: str
  s: str