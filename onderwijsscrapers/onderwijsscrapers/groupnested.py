from collections import OrderedDict, MutableMapping, Hashable

class GroupNested(MutableMapping):
    """
    A nested dict indexed by ordered dicts
    Structure should be specified in advance

    TODO: maybe assume all keys are tuples? instead of type filtering
    """
    def __init__(self, struct, *args, **kwargs):
        """
        Build the empty structure from a nested dict

        For values:
            False means that this is a value
            True means that this is a dict (per_)
        """
        self.store = dict()
        self.update(dict(*args, **kwargs))  # use the free update to set keys

        self.keys = struct.keys()
        self.nest = {k: lambda: GroupNested(v) for k,v in struct.items() if v}

    def __getitem__(self, index):
        if index and type(index)==OrderedDict:
            k,v = index.popitem(last=False)
            if k not in self.store:
                    self.store[k] = {}
            if v not in self.store[k]:
                self.store[k][v] = self.nest[k]()
            if index:
                return self.store[k][v][index]
            else:
                return self.store[k][v]
        elif index:
            raise IndexError("Index to get must be an OrderedDict")
        else:
            raise IndexError("Cannot get item with empty index")

    def __setitem__(self, index, value):
        if index and type(index)==OrderedDict:
            k,v = index.popitem(last=False)
            if k in self.keys:
                if k not in self.store:
                    self.store[k] = {}
                if index:
                    if k in self.nest:
                        if v not in self.store[k]:
                            self.store[k][v] = self.nest[k]()
                        # recursive case
                        self.store[k][v][index] = value
                    else:
                        raise IndexError(
                            "The value at this key (%s) is not further nested. "
                            "This means the index had some left over:\n %s"
                            % (k,index)
                        )
                else:
                    # base case, value must be Mapping
                    if v not in self.store[k]:
                        self.store[k][v] = GroupNested({})
                    self.store[k][v].update(value)
            else:
                raise KeyError("Cannot add item: key '%s' not present" % k)
        elif index:
            # set on the root
            self.store[index] = value
        else:
            raise IndexError("Cannot add item with empty index")

    def __delitem__(self, index):
        if index and type(index)==OrderedDict:
            k,v = index.popitem(last=False)
            if index:
                del self.store[k][v][index]
                if not self.store[k][v]:
                    del self.store[k][v]
            else:
                del self.store[k][v]
            if not self.store[k]:
                del self.store[k]
        elif index:
            raise IndexError("Index to del must be an OrderedDict")
        else:
            raise IndexError("Cannot del item with empty index")

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)

    def __str__(self):
        return self.__str_nest__(0)
    def __str_nest__(self, d):
        out = ""
        for k,v in self.store.items():
            if k in self.nest:
                out += d*"\t" + str(k) + ":\n"
                for i,j in v.items():
                    out += d*"\t" + " " + str(i) + ":\n"
                    if type(j)==GroupNested:
                        out += j.__str_nest__(d+1)
                    else:
                        out += (d+1)*"\t" + str(j)
            else:
                out += d*"\t" + str(k) + ": " + str(v) + "\n"
        return out

    def struct(self, *args):
        """
        Transform into a json-ish representation
        """
        def nested_set(dic, keys, value):
            for key in keys[:-1]:
                dic = dic.setdefault(key, {})
            dic[keys[-1]] = value
        
        out = args[0] if args else {}
        for k,v in self.store.items():
            if k in self.nest:
                if type(k) == tuple:
                    m = list(k)
                    m[-1] = 'per_%s'%k[-1]
                    nested_set(out, m, 
                        [j.struct({k[-1]:i}) for i,j in v.items()])
                else:
                    out['per_%s'%k] = [j.struct({k:i}) for i,j in v.items()]
            else:
                if type(k) == tuple:
                    nested_set(out, k, v)
                else:
                    out[k] = v
        return out

if __name__ == '__main__':
    def test_gn():
        d = {'banana': 3, 'apple':4, ('pear', 'a'): 1, 'orange': 2}
        i = OrderedDict(sorted(d.items(), key=lambda t: t[0]))
        print i

        # False means that this is a value
        # True means that this is a dict (per_)
        nest = {'apple': {'kiwi': False, 'banana': {'orange': {('pear', 'a'): True } } }}
        print 'nest', nest
        gn = GroupNested(nest)
        gn[i.copy()] = {"bar":4}
        gn[OrderedDict([('apple',2), ('banana', 3)])]["kiwi"] = 0

        print gn

        print gn.__json__()

    test_gn()