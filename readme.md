## No-SQL DB using Python

This program is written with the aim of understanding how Key-value pair DB's work at basic level and have implemented few operations using TCP-IP.

### Supporting Commands
- GET
- PUT
- DELETE

- GETLIST
- PUTLIST
- APPEND
- STATS

Db is started by running `python3 index.py` and send commands to the port accordingly using `client.py`. Below are few examples of supported
operations

- PUT;foo;1;INT"
- "GET;foo;;"
- "PUTLIST;bar;a,b,c;LIST"

- "APPEND;bar;d;STRING
- "GETLIST;bar;;"
- "STATS;;;"
- "INCREMENT;foo;;"
- "DELETE;foo;;"