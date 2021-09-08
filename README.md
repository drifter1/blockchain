# blockchain
Educational Python Implementation of a Blockchain

# Prerequisites
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [Mnemonic](https://pypi.org/project/mnemonic/0.20/) 
- [ECDSA](https://pypi.org/project/ecdsa/)

# Basic Installation (Ubuntu)
Install python:
~~~
sudo apt install python
~~~
and then the packages using python's package manager (pip):
~~~
pip install flask requests mnemonic ecdsa
~~~

# REST API

## Node Endpoints
| Endpoint      | HTTP Verb | Request (JSON) | Response (JSON) |  Description                          |
| :----------   | :------:  | :-----------:  | :-----------:   |  :--------------------------------    |
| /             | POST      | Node (opt.)    | Node            |  Check if node is reachable/online    |    
| /nodes/       | GET       | Node (opt.)    | Nodes array     |  Retrieve all known nodes             |
| /nodes/nid/   | GET       | -              | Node            |  Retrieve node by nid                 |
| /nodes/       | POST      | Node           | Nodes array     |  Add node to known nodes              |
| /nodes/       | DELETE    | Node           | Nodes array     |  Remove node from known nodes         |

Using "random" as the nid returns a random node. Otherwise, nid is the node index.

## Blockchain Endpoints
| Endpoint       | HTTP Verb | Request (JSON)    | Response (JSON)    |  Description                         |
| :-----------   | :------:  | :---------------: | :--------------:   |  :--------------------------------   |
| /blockchain/   | GET       | -                 | Blockchain Info    |  Retrieve blockchain information     |
| /blockchain/   | PUT       | Blockchain Info   | Blockchain Info    |  Replace blockchain information      |

## Transaction Endpoints
| Endpoint             | HTTP Verb  | Request (JSON)    | Response (JSON)       |  Description                                |
| :------------------  | :------:   | :---------------: | :------------------:  |  :--------------------------------          |
| /transactions/       | GET        | -                 | Transactions Header   |  Retrieve unconfirmed transactions header   |
| /transactions/tid/   | GET        | -                 | Transaction           |  Retrieve unconfirmed transaction by tid    |
| /transactions/       | POST       | Transaction       | Transaction           |  Post new transaction                       |
| /transactions/       | DELETE     | Transaction       | Transaction           |  Remove posted transaction                  |

For tid both the index and the hash can be used.

## Block Endpoints
| Endpoint                                     | HTTP Verb  | Request (JSON)    | Response (JSON)            |  Description                                          |
| :-----------------------------------------   | :------:   | :--------------:  | :----------------------:   |  :-------------------------------------------------   |
| /blocks/bid/                                 | GET        | -                 | Block Header               |  Retrieve block header by block id                    |
| /blocks/bid/transactions/                    | GET        | -                 | Transactions Header        |  Retrieve block transactions header by block id       |
| /blocks/bid/transactions/tid/                | GET        | -                 | Transaction                |  Retrieve block transaction by bid-tid pair           |
| /blocks/bid/transactions/tid/inputs/         | GET        | -                 | Transaction input array    |  Retrieve block transaction inputs by bid-tid pair    |
| /blocks/bid/transactions/tid/inputs/iid/     | GET        | -                 | Transaction input          |  Retrieve block transaction input by bid-tid-iid      |
| /blocks/bid/transactions/tid/outputs/        | GET        | -                 | Transaction output array   |  Retrieve block transaction outputs by bid-tid pair   |
| /blocks/bid/transactions/tid/outputs/oid/    | GET        | -                 | Transaction output         |  Retrieve block transaction output by bid-tid-oid     |
| /blocks/                                     | POST       | Block             | Block                      |  Create new block                                     |

Using "last" as the bid returns information for the last block in the chain. Otherwise, bid is the block height.

For tid both the index and the hash can be used.

## UTXO Endpoints
| Endpoint                                  | HTTP Verb  | Request (JSON)    | Response (JSON)    |  Description                                   |
| :---------------------------------------  | :------:   | :---------------: | :--------------:   |  :------------------------------------------   |
| /utxo/address/                            | GET        | -                 | UTXO               |  Retrieve utxo by address                      |
| /utxo/address/outputs/                    | GET        | -                 | UTXO Output array  |  Retrieve utxo outputs by address              |
| /utxo/address/outputs/transaction_hash/   | GET        | -                 | UTXO Output        |  Retrieve utxo output by address-hash pair     |
| /utxo/address/                            | POST       | UTXO (opt.)       | UTXO               |  Create utxo of address                        |
| /utxo/address/outputs/                    | POST       | UTXO Output       | UTXO Output        |  Add utxo output to utxo of address            |
| /utxo/address/outputs/                    | DELETE     | UTXO Output       | UTXO Output        |  Remove utxo output from utxo of address       |
