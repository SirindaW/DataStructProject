from .AVLTree import AVL
from .HashTable import HashTable

class Product:
    def __init__(self, prod_id, name=None,product=None):
        self.prod_id = prod_id
        self.name = name
        self.product= product

    def __repr__(self):
        return '(Product:id=' + str(self.prod_id) + ',name=' + str(self.name) + ']'

    # Comparision operator override
    def __lt__(self, o):
        return self.prod_id < o.prod_id

    def __le__(self, o):
        return self.prod_id <= o.prod_id

    def __gt__(self, o):
        return self.prod_id > o.prod_id

    def __ge__(self, o):
        return self.prod_id >= o.prod_id

    def __eq__(self, o):
        return self.prod_id == o.prod_id

    def __ne__(self, o):
        return self.prod_id != o.prod_id


class ProductStructure:
    def __init__(self, iterable=None):
        self.tree = AVL()
        self.hash_table = HashTable()
        self.size = 0

        if iterable is not None:
            for e in iterable:
                # Convert to 'Product' type (not the same of django model)
                p = Product(e.id,e.title,e)
                # Add elements in Tree
                self.tree.insert(p)
                # Add elements in hashtable
                self.hash_table[p.name] = p

                self.size += 1

    def get(self, **kwargs):
        # Perform search by id
        try :
            by_id = kwargs.get('id')
        except KeyError:
            by_id = None
        if by_id is not None:
            result = self.search_by_id(by_id)
            if result is None:
                raise KeyError(f'No product id "{by_id}"')
            result = result.data

        # print("FROM GET METHOD",result)
            
        # Perform search by name
        if kwargs.get('name'):
            by_name = kwargs.get('name')
        else:
            by_name = None

        if by_name is not None:
            try:
                if result is not None:
                    if result.name != by_name:
                        raise KeyError(f'Product id "{by_id}" does not match name "{by_name}"')
            except UnboundLocalError:
                pass
            result = self.search_by_name(by_name)

        return result

    def get_or_none(self,**kwargs):
        try:
            result = self.get(**kwargs)
        except KeyError:
            result = None
        return result

    def search_by_name(self,name):
        # Search by name using hash table
        result = self.hash_table[name]
        print("RESULTl,",result)
        return result

    def search_by_id(self, prod_id, node=None):
        if node is None:
            node = self.tree.root

        if prod_id == node.data.prod_id:
            return node
        elif prod_id < node.data.prod_id:
            if node.left:
                return self.search_by_id(prod_id, node.left)
        elif prod_id > node.data.prod_id:
            if node.right:
                return self.search_by_id(prod_id, node.right)

        # Not found
        return None

    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.tree)

    def __iter__(self):
        for product in self.tree:
            yield product


if __name__ == "__main__":

    # Generate testing product
    x = []
    for i in range(10):
        x.append(Product(i, "name"+ str(i)))

    p = ProductStructure(x)
    # print(p.get(name='name1'))
    # print(p.get(id=1))
    # print(type(p.get(id=0,name='name1')))
    product = p.get_or_none(id=0)
