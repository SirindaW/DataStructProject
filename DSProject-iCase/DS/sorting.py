def sort_by_price(data, reverse=False):

    if len(data) <= 1:
        return data
    piv_pos = len(data)//2

    piv = data[piv_pos]

    left = []
    mid = []
    right = []

    for d in data:
        # Change compare attribute here.
        value = d.price
        piv_value = piv.price

        if not reverse:
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

    return sort_by_price(left, reverse) + mid + sort_by_price(right, reverse)

def sort_by_alphabet(data,reverse=False):
    # Selection sort
    data = [d for d in data]

    # Find min
    def find_min(iter):
        result = None
        for d in iter:
            if not result:
                result = d

            if d.title < result.title:
                result = d
        return result

    def find_max(iter):
        if len(iter) == 1:
            return iter[0]
        result = None
        for d in iter:
            if not result:
                result = d

            if d.title > result.title:
                result = d
        return result


    result = []
    while len(data) != 0:
        if not reverse:
            result.append(data.pop(data.index(find_min(data))))
        else:
            result.append(data.pop(data.index(find_max(data))))
    
    return result
