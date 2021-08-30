# blockchain
Educational Python Implementation of a Blockchain

# Prerequisites
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [Mnemonic](https://pypi.org/project/mnemonic/0.20/) 
- [ECDSA](https://pypi.org/project/ecdsa/)

# REST API

## Node Endpoints
| Resource Type       | HTTP Verb | Endpoint  | Request (JSON) | Response (JSON) |  Description                          |
| :----------------:  | :-----:   | :------:  | :-----------:  | :-----------:   |  :--------------------------------    |
| Connection Check    | POST      | /         | Node (opt.)    | Node            |  Check if node is reachable/online    |    
| Nodes               | GET       | /nodes/   | Node (opt.)    | Nodes array     |  Retrieve all known nodes             |
| Nodes               | POST      | /nodes/   | Node           | Nodes array     |  Add node to known nodes              |
| Nodes               | DELETE    | /nodes/   | Node           | Nodes array     |  Remove node from known nodes         |

## Blockchain Endpoints
| Resource Type       | HTTP Verb | Endpoint       | Request (JSON)    | Response (JSON)    |  Description                         |
| :----------------:  | :-----:   | :-----------:  | :---------------: | :--------------:   |  :--------------------------------   |
| Blockchain Info     | GET       | /blockchain/   | -                 | Blockchain Info    |  Retrieve blockchain information     |
| Blockchain Info     | PUT       | /blockchain/   | Blockchain Info   | Blockchain Info    |  Replace blockchain information      |

## Transaction Endpoints
| Resource Type     | HTTP Verb | Endpoint          | Request (JSON)    | Response (JSON)     |  Description                         |
| :--------------:  | :-----:   | :--------------:  | :---------------: | :----------------:  |  :--------------------------------   |
| Transactions      | GET       | /transactions/    | -                 | Transaction array   |  Retrieve unconfirmed transactions   |
| Transactions      | POST      | /transactions/    | Transaction       | Transaction         |  Post new transaction                |
| Transactions      | DELETE    | /transactions/    | Transaction       | Transaction         |  Cancel posted transaction           |

## Block Endpoints
| Resource Type                 | HTTP Verb | Endpoint                                    | Request (JSON)    | Response (JSON)            |  Description                                             |
| :---------------------------: | :-----:   | :----------------------------------------:  | :---------------: | :----------------------:   |  :----------------------------------------------------   |
| Block                         | GET       | /blocks/bid/                                | -                 | Block                      |  Retrieve block by block id                              |
| Block Transactions            | GET       | /blocks/bid/transactions/                   | -                 | Transaction array          |  Retrieve block transactions by block id                 |
| Block Transaction             | GET       | /blocks/bid/transactions/tid/               | -                 | Transaction                |  Retrieve block transaction by bid-tid pair              |
| Block Transaction Inputs      | GET       | /blocks/bid/transactions/tid/inputs/        | -                 | Transaction input array    |  Retrieve block transaction inputs by bid-tid pair       |
| Block Transaction Input       | GET       | /blocks/bid/transactions/tid/inputs/iid/    | -                 | Transaction input          |  Retrieve block transaction input by bid-tid-iid         |
| Block Transaction Outputs     | GET       | /blocks/bid/transactions/tid/outputs/       | -                 | Transaction output array   |  Retrieve block transaction outputs by bid-tid pair      |
| Block Transaction Output      | GET       | /blocks/bid/transactions/tid/outputs/oid/   | -                 | Transaction output         |  Retrieve block transaction output by bid-tid-oid        |
| Blocks                        | POST      | /blocks/                                    | Block             | Block                      |  Create new block                                        |

## UTXO Endpoints
| Resource Type       | HTTP Verb | Endpoint                                  | Request (JSON)    | Response (JSON)    |  Description                                   |
| :-----------------: | :-----:   | :--------------------------------------:  | :---------------: | :--------------:   |  :------------------------------------------   |
| UTXO                | GET       | /utxo/address/                            | -                 | UTXO               |  Retrieve utxo by address                      |
| UTXO Outputs        | GET       | /utxo/address/outputs/                    | -                 | UTXO Output array  |  Retrieve utxo outputs by address              |
| UTXO Output         | GET       | /utxo/address/outputs/transaction_hash/   | -                 | UTXO Output        |  Retrieve utxo output by address-hash pair     |
| UTXO                | POST      | /utxo/address/                            | UTXO (opt.)       | UTXO               |  Create utxo of address                        |
| UTXO Output         | POST      | /utxo/address/outputs/                    | UTXO Output       | UTXO Output        |  Add utxo output to utxo of address            |
| UTXO Output         | DELETE    | /utxo/address/outputs/                    | UTXO Output       | UTXO Output        |  Remove utxo output from utxo of address       |