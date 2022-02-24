class Database:

    operations = {
        'GET': (1, lambda database, name: print(database.get(name) if database.get(name) is not None else 'NULL')),
        'SET': (2, lambda database, name, value: database.set(name, value)),
        'DELETE': (1, lambda database, name: database.delete(name)),
        'COUNT': (1, lambda database, value: print(database.count(value))),
        'BEGIN': (0, lambda database: database.start_transaction()),
        'COMMIT': (0, lambda database: database.commit()),
        'ROLLBACK': (0, lambda database: print('NO TRANSACTION') if not database.is_transaction else database.rollback()),
        'EXIT': (0, lambda database: exit())
    }

    def __init__(self):
        self.database = {}
        self.transactions = []
        self.is_transaction = False
        self.is_rollback = False
        self.counts = {}

    def get(self, name):
        """
        Get value name from dict

        Args:
            name ([str]): name of the key

        Returns:
            [str]: key 
        """
        
        # print(f"Printing current database state {self.database}")
        return self.database.get(name, None)

    def set(self, name, value):
        """
        Set key & value in the dictionary
        Hold number of appearances of the value in 'counts' list 
        of database object
        
        Args:
            name ([str]): name of the value (key)
            value ([str]): value
        """
        previous_value = self.database.get(name, None)
        # print(f"Previous value {previous_value}")
        if previous_value == value:
            return
        self.database[name] = value
        self.counts[value] = self.counts.get(value, 0) + 1
        if previous_value is not None:
            self.counts[previous_value] -= 1 # replace earlier value, decrease counter
        if self.is_transaction and not self.is_rollback: 
            # if its transaction and not rollback set last element 
            self.transactions[-1].append((name, previous_value))
        # print(f"Transactions lists: {self.transactions}")

    def delete(self, name):
        """Delete a key/value pair from the database"""
        if name in self.database:
            value = self.database.get(name) # o(n)
            del self.database[name]
            self.counts[value] -= 1
            if self.is_transaction and not self.is_rollback:
                self.transactions[-1].append((name, value))

    def count(self, value):
        return self.counts.get(value, 0)

    def start_transaction(self):
        self.transactions.append([])
        self.is_transaction = True

    def rollback(self):
        self.is_rollback = True
        past_operations = self.transactions.pop() # remove and return last element of the transactions
        while past_operations:
            name, value = past_operations.pop()
            self.delete(name) if value is None else self.set(name, value)
        self.is_rollback = False
        if not self.transactions:
            self.is_transaction = False

    def commit(self):
        self.transactions.clear() # clear list of transactions
        self.is_transaction = False 

    def apply(self, command):
        command = command.split()
        operation = command.pop(0).upper() if command else None
        if operation not in self.operations or len(command) != self.operations[operation][0]:
            print('INVALID COMMAND')
        else:
            self.operations[operation][1](self, *command)
        return True
