from .LinkedList import DoublyLinkedList as LinkedList


class Item:
    def __init__(self, key, val):
        self.__key = key
        self.__val = val

    @property
    def key(self):
        return self.__key

    @key.setter
    def key(self, key):
        self.__key = key

    @property
    def val(self):
        return self.__val

    @val.setter
    def val(self, val):
        self.__val = val

    def __repr__(self):
        return '(' + str(self.key) + ':' + str(self.val) + ')'


class HashTable:
    def __init__(self, MAX=10):
        self.MAX = MAX
        self.arr = [LinkedList() for _ in range(self.MAX)]
        self.size = 0
        return

    def get_hash(self, key):
        # Hash Funciton sum of ascii
        key = str(key)
        h = 0
        for char in key:
            h += ord(char)
        return h % self.MAX

    def add(self, key, val):
        # Check dynamic MAX table size
        if (1+self.size) * 2 > self.MAX:
            new_table = HashTable(2*self.MAX)
            for k in self:
                new_table[k] = self[k]
            self.arr = new_table.arr
            self.MAX = new_table.MAX

        h = self.get_hash(key)

        if self.arr[h].is_not_empty():
            # Go thorugh the Chain, update the val
            for item in self.arr[h]:
                if item.key == key:
                    item.val = val
                    return
            # Create new item
            item = Item(key, val)
            self.arr[h].append(item)
            self.size += 1

        else:
            # If never existed
            item = Item(key, val)
            self.arr[h].append(item)
            self.size += 1

    def get(self, key):
        h = self.get_hash(key)
        if self.arr[h].is_not_empty():
            # Go through the Chain
            for item in self.arr[h]:
                if item.key == key:
                    return item.val

            raise KeyError(f'No key "{key}" exists in the table')
        # return self.arr[h].val

    def contains(self,key):
        h = self.get_hash(key)

        if self.arr[h].is_not_empty():
            for item in self.arr[h]:
                if item.key == key:
                    return True
            return False
            

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, val):
        return self.add(key, val)

    def __iter__(self):
        for cell in self.arr:
            if cell.is_not_empty():
                # Going through the LinkedList
                for item in cell:
                    yield item.key

    def __repr__(self):
        res = []
        for cell in self.arr:
            if cell.is_not_empty():
                # Going through the Chain
                for item in cell:
                    res.append(item)

        return '{' + ', '.join(str(x) for x in res) + '}'


if __name__ == "__main__":
    x = HashTable()
    x['march 6'] = 6
    x['march 6'] = 12
    x['march 17'] = 32
    x['march'] = 145
    x['may'] = 300
    x['apr'] = 192
    x['sub'] = 84

    print(x)