# blockchain
Educational Python Implementation of a Blockchain

# Prerequisites
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)

# REST API

## Node Endpoints
| Resource Type       | HTTP Verb | Endpoint   | Request (JSON) | Response (JSON) |  Description                          |
| :----------------:  | :-----:   | :-----:    | :-----------:  | :-----------:   |  :--------------------------------    |
| Connection Check    | POST      | /          | Node           | Node            |  Check if node is reachable/online    |    
| Nodes               | GET       | /nodes/    | Node           | Nodes array     |  Retrieve all known nodes             |
| Nodes               | POST      | /nodes/    | Node           | Nodes array     |  Add node to known nodes              |
| Nodes               | DELETE    | /nodes/    | Node           | Nodes array     |  Remove node from known nodes         |
