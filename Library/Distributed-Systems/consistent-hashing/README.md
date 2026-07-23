# Consistent Hashing

## Overview
Consistent hashing is a distributed hashing scheme that operates independently of the number of servers or objects in a distributed hash table by assigning them a position on an abstract circle, or hash ring. This allows servers and objects to scale without affecting the overall system. When a node is added or removed, it only affects its immediate neighbors.

## Implementation
This directory contains a Python implementation of a Consistent Hash Ring, utilizing `hashlib.md5` for distributing the keys and `bisect` for fast key lookups on the ring. It also supports virtual nodes (replicas) to distribute the load more evenly across physical nodes.

## Usage
Run the script to see a basic example:
```bash
python core/consistent_hashing.py
```
