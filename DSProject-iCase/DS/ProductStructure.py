from .AVLTree import AVL
from .HashTable import HashTable


class Product:
    def __init__(self, prod_id, name=None, product=None):
        self.prod_id = prod_id
        self.name = name
        self.product = product

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
                self.add(e)

    def add(self,product):
        # Convert to 'Product' type (not the same of django model)
        p = Product(product.id,product.title,product)
        self.tree.insert(p)
        self.hash_table[p.name] = p
        self.size+=1


    def get(self, **kwargs):
        # Perform search by id
        try:
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
                        raise KeyError(
                            f'Product id "{by_id}" does not match name "{by_name}"')
            except UnboundLocalError:
                pass
            result = self.search_by_name(by_name)

        return result

    def get_or_none(self, **kwargs):
        try:
            result = self.get(**kwargs)
        except KeyError:
            result = None
        return result

    def search_by_name(self, name):
        # Search by name using hash table
        result = self.hash_table[name]
        print("RESULTl,", result)
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

    def binary_search_id(self,prod_id):
        products = sorted(list(self))

        try:
            result = self._binary_search_id(products,prod_id)
        except KeyError:
            result = None
        
        return result

    def _binary_search_id(self, arr ,prod_id, low=None, high=None):
        if low is None:
            low = 0
        if high is None:
            high = len(arr)-1
            
        if high >= low:
            mid = (high + low) // 2
            if arr[mid].product.id == prod_id:
                return arr[mid]
            elif arr[mid].product.id > prod_id:
                return self._binary_search_id(arr,prod_id, low, mid - 1 )
            else:
                return self._binary_search_id(arr,prod_id, mid + 1, high )
        else:
            raise KeyError(f"No such product id {prod_id}")


    def __len__(self):
        return self.size

    def __str__(self):
        return str(self.tree)

    def __getitem__(self, index):
        elements = self.tree.in_order_traversal()
        return elements[index]

    def __iter__(self):
        for product in self.tree:
            yield product

    def sort_by_price(self, asc=True):
        # Convert from tree to list
        products = list(self)
        # QUICKSORT
        result = self._sort_by_price_quicksort(products, asc)

        return result

    def _sort_by_price_quicksort(self, data, asc=True):
        if len(data) <= 1:
            return data
        piv_pos = len(data)//2

        piv = data[piv_pos]

        left = []
        mid = []
        right = []

        for d in data:
            # Change compare attribute here.
            value = d.product.price
            piv_value = piv.product.price

            if asc:
                # from low to high
                if value < piv_value:
                    left.append(d)
                elif value > piv_value:
                    right.append(d)
                else:
                    mid.append(d)
            else:
                # from high to low
                if value < piv_value:
                    right.append(d)
                elif value > piv_value:
                    left.append(d)
                else:
                    mid.append(d)

        return self._sort_by_price_quicksort(left, asc) + mid + self._sort_by_price_quicksort(right, asc)

    def sort_by_alphabet(self,asc=True):
        products = list(self)
        # SELECTION SORT
        result = self._sort_by_alphabet_selectionsort(products,asc)
        return result

    def _sort_by_alphabet_selectionsort(self, data, asc=True):
        # SELECTION SORT

        # Find min
        def find_min(iter):
            result = None
            for d in iter:
                if not result:
                    result = d

                if d.product.title < result.product.title:
                    result = d
            return result

        def find_max(iter):
            if len(iter) == 1:
                return iter[0]
            result = None
            for d in iter:
                if not result:
                    result = d

                if d.product.title > result.product.title:
                    result = d
            return result

        result = []
        while len(data) != 0:
            if asc:
                result.append(data.pop(data.index(find_min(data))))
            else:
                result.append(data.pop(data.index(find_max(data))))

        return result


if __name__ == "__main__":

    # Generate testing product
    x = []
    for i in range(10):
        x.append(Product(i, "name" + str(i)))

    p = ProductStructure(x)
    # print(p.get(name='name1'))
    # print(p.get(id=1))
    # print(type(p.get(id=0,name='name1')))
    product = p.get_or_none(id=0)
