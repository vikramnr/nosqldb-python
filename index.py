# imports and variable declaration
import socket

HOST = 'localhost'
PORT  = 5050
SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
STATUS = {
    'PUT': {'success': 0, 'error': 0},
    'GET': {'success': 0, 'error': 0},
    'GETLIST': {'success': 0, 'error': 0},
    'PUTLIST': {'success': 0, 'error': 0},
    'INCREMENT': {'success': 0, 'error': 0},
    'APPEND': {'success': 0, 'error': 0},
    'DELETE': {'success': 0, 'error': 0},
    'STATS': {'success': 0, 'error': 0},
}

# data dict
DB_DATA = {}

# parses messages and returns cmd,data and datatype
def parse_message(data):
    command, key, value,  value_type = data.strip().split(';')
    if value_type:
        if value_type == 'LIST':
            value = value.split(',')
        elif value_type == 'INT':
            value = int(value)
        else: 
            value = str(value)
    else: 
        value = None
    return command,key, value

# for each operation status is updated
def update_stats(command, suceess):
    if suceess:
        STATUS[command]['success'] +=1
    else:
        STATUS[command]['error'] += 1

# loosly translated CRUD
def handle_put(key, value):
    DB_DATA[key] = value
    return (True, 'key [{}] set to [{}]'.format(key,value))

def handle_get(key):
    if key not in DB_DATA:
        return(False, 'error [{}] not found'.format(key))
    else:
        return(True, DB_DATA[key])

# adds item of list 
def handle_putlist(key,value):
    return handle_put(key,value)

# returns items of list
def handle_getlist(key):
    return_value = exists, value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value,list):
        return (False, 'err: key [{}] contains not list value [{}]'.format(key, value))
    else:
        return return_value 

def handle_increment(key):
    return_value = exists, value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(value,int):
        return (False, 'err: key [{}] contains not int value [{}]'.format(key, value))
    else:
        DB_DATA[key] +=1
        return(True, 'key [{}] incremented'.format(key))

def handle_append(key, value):
    return_value = exists, list_value = handle_get(key)
    if not exists:
        return return_value
    elif not isinstance(list_value,list):
        return (False, 'err: key [{}] contains not list value [{}]'.format(key, list_value))
    else:
        DB_DATA[key].append(value)
        return (True, 'key [{}] has been appended to value'.format(key))

def handle_delete(key):
    if key not in DB_DATA:
        return(False, 'error [{}] not found'.format(key))
    else:
        del DB_DATA[key]

def handle_stats():
    return (True, str(STATUS))

# cmd dict and mapping functions
COMMAND_HANDLERS = {
    'PUT': handle_put,
    'GET': handle_get,
    'GETLIST': handle_getlist,
    'PUTLIST': handle_putlist,
    'INCREMENT': handle_increment,
    'APPEND': handle_append,
    'DELETE': handle_delete,
    'STATS': handle_stats
}

# start of main
def main():
    # starting server
    SOCKET.bind((HOST, PORT))
    SOCKET.listen(1)
    print('server started listening at'+str(PORT))
    while 1:
        connection, address = SOCKET.accept()
        # detects connection and parses cmd
        print('New connection from [{}]'.format(address))
        data = connection.recv(4096).decode()
        command, key, value = parse_message(data)
        print(command)
        # if stats return it, 
        # for get,increment,delete only key is required 
        # and for put,append both key&values
        if command== 'STATS':
            response = handle_stats()
        elif command in (
            'GET',
            'GETLIST',
            'INCREMENT',
            'DELETE'
                ):
            response = COMMAND_HANDLERS[command](key)
        elif command in (
            'PUT',
            'PUTLIST',
            'APPEND',
                ):
            response = COMMAND_HANDLERS[command](key, value)
        else:
            response = (False, 'Unknown command type[{}]'.format(command))
        # update stats based on response
        update_stats(command, response[0])
        # send response and close connection
        connection.sendall(response[1].encode())
        connection.close()

if __name__ == "__main__":
    main()


