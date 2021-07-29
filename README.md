# blockchain
Educational Python Implementation of a Blockchain

# Prerequisites
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)

# REST API

## DNS Server
| Resource Type       | HTTP Verb | Endpoint   | Request (JSON) | Response (JSON) |  Description                          |
| :----------------:  | :-----:   | :-----:    | :-----------:  | :-----------:   |  :--------------------------------    |
| Initial Connection  | POST      | /          | Node           | Node            |  Initial network connection           |    
| Nodes               | GET       | /nodes/    | -              | Nodes array     |  Retrieve all known nodes             |
| Nodes               | POST      | /nodes/    | Node           | Nodes array     |  Add node to known nodes              |
| Nodes               | DELETE    | /nodes/    | Node           | Nodes array     |  Remove node from known nodes         |

## Basic Client
| Resource Type       | HTTP Verb | Endpoint   | Request (JSON) | Response (JSON) |  Description                          |
| :----------------:  | :-----:   | :-----:    | :-----------:  | :-----------:   |  :--------------------------------    |
| Initial Connection  | POST      | /          | Node           | Node            |  Initial network connection           |   
| Connection Check    | GET       | /          | -              | -               |  Check if node is reachable/online    |    
| Nodes               | GET       | /nodes/    | -              | Nodes array     |  Retrieve all known nodes             |
| Nodes               | POST      | /nodes/    | Node           | Nodes array     |  Add node to known nodes              |
| Nodes               | DELETE    | /nodes/    | Node           | Nodes array     |  Remove node from known nodes         |
