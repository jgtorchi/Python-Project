class HashEntry:

    def __init__(self, key, value):  # can add additional attributes
        self.key = key
        self.value = value


class HashTable:

    def __init__(self, table_size):         # can add additional attributes
        self.table_size = table_size        # initial table size
        self.hash_table = [None]*table_size # hash table
        self.num_items = 0                  # empty hash table

    def insert(self, key, value):
        """ Inserts an entry into the hash table (using Horner hash function to determine index, 
        and quadratic probing to resolve collisions).
        The key is a string (a word) to be entered, and value is the line number that the word appears on. 
        If the key is not already in the table, then the key is inserted, and the value is used as the first 
        line number in the list of line numbers. If the key is in the table, then the value is appended to that 
        key’s list of line numbers. If value is not used for a particular hash table (e.g. the stop words hash table),
        can use the default of 0 for value and just call the insert function with the key.
        If load factor is greater than 0.5 after an insertion, hash table size should be increased (doubled + 1)."""
        hash_num = self.horner_hash(key)
        index = self.get_index(key)
        if index is not None:
            self.hash_table[index].value += [value]
            found = True
        else:
            found = False
        x = 0
        y = 0
        while (not found) and (x <= self.table_size):
            if self.hash_table[(hash_num + y) % self.table_size] is None:
                if type(value) != list:
                    value = [value]
                self.hash_table[(hash_num + y) % self.table_size] = HashEntry(key, value)
                self.num_items += 1
                found = True
            x += 1
            y = x**2
        if (self.num_items/self.table_size) > 0.5:
            self.rehash(self.table_size * 2 + 1)
        return

    def horner_hash(self, key):
        """ Compute and return an integer from 0 to the (size of the hash table) - 1
        Compute the hash value by using Horner’s rule, as described in project specification."""
        n = min(8, len(key))
        total = 0
        for i in range(0, n):
            total += ord(key[i]) * (31**(n-1-i))
        return total % self.table_size

    def in_table(self, key):
        """ Returns True if key is in an entry of the hash table, False otherwise."""
        hash_num = self.horner_hash(key)
        x = 0
        y = 0
        while x <= self.table_size:
            if self.hash_table[(hash_num + y) % self.table_size] is None:
                return False
            elif self.hash_table[(hash_num + y) % self.table_size].key == key:
                return True
            else:
                x += 1
                y = x ** 2

    def get_index(self, key):
        """ Returns the index of the hash table entry containing the provided key. 
        If there is not an entry with the provided key, returns None."""
        hash_num = self.horner_hash(key)
        x = 0
        y = 0
        while x <= self.table_size:
            if self.hash_table[(hash_num + y) % self.table_size] is None:
                return None
            elif self.hash_table[(hash_num + y) % self.table_size].key == key:
                return (hash_num + y) % self.table_size
            else:
                x += 1
                y = x ** 2

    def get_all_keys(self):
        """ Returns a Python list of all keys in the hash table."""
        keys = []
        for x in range(0, self.table_size):
            if self.hash_table[x] is not None:
                keys.append(self.hash_table[x].key)
        return keys

    def get_value(self, key):
        """ Returns the value (list of line numbers) associated with the key. 
        If key is not in hash table, returns None."""
        hash_num = self.horner_hash(key)
        x = 0
        y = 0
        while x <= self.table_size:
            if self.hash_table[(hash_num + y) % self.table_size] is None:
                return None
            elif self.hash_table[(hash_num + y) % self.table_size].key == key:
                return self.hash_table[(hash_num + y) % self.table_size].value
            else:
                x += 1
                y = x ** 2

    def get_num_items(self):
        """ Returns the number of entries (words) in the table."""
        return self.num_items

    def get_table_size(self):
        """ Returns the size of the hash table."""
        return self.table_size

    def get_load_factor(self):
        """ Returns the load factor of the hash table (entries / table_size)."""
        return self.num_items/self.table_size

    def rehash(self, new_size):
        """ Rehashes with new_size as the table_size"""
        new_hash = HashTable(new_size)
        for x in range(0, self.table_size):
            if self.hash_table[x] is not None:
                new_hash.insert(self.hash_table[x].key, self.hash_table[x].value)
        self.hash_table = new_hash.hash_table
        self.table_size = new_size