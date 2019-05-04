
def pooz_new_obj(cls, as_this, name='<untitled pooz obj>'):
    obj = cls(name)

    for field, value in as_this.items():
        obj.set_property(field, value)


class PoozNULL:
    def __init__(self, name='<untitled pooz NULL type>'):
        self.__v = None


class PoozRootObject:
    def __init__(self, name='<untitled object>'):
        self.__propertys = {}

        self.set_property('__name__', name)
        self.set_property('__super__')

    def set_property(self, name, value, vm):
        self.__propertys[name] = value

    def del_property(self, name, vm):
        if name not in self.__propertys:
            vm.push_error(PoozErrorObject('{0} property is not exists'.format(name)))
            return

        del self.__propertys[name]

    def get_property(self, name, vm):
        if name not in self.__propertys:
            vm.push_error(PoozErrorObject('{0} property is not exists'.format(name)))
            return

        return self.__propertys[name]

class PoozListObject(PoozRootObject):
    def __init__(self, pylist=[], name='<untitled list object>'):
        super(name)

        self.__pylist = pylist
        self.__real_index = 0

        if not pylist:
            for i in pylist:
                self.add_item(i)

    def add_item(self, item, vm):
        self.__pylist.append(item)

    def del_item(self, item, vm):
        if name not in self.__pylist:
            vm.push_error(PoozErrorObject('{0} is not in '.format(name)))
            return 
        
        self.__pylist.remove(item)

    def __iter__(self):
        return iter(self.__pylist)

    def __next__(self):
        if self.__real_index >= len(self.__pylist):
            raise StopIteration('Index out of range')

        v = self.__pylist[self.__real_index]
        self.__real_index += 1


class PoozNormalFunction(PoozRootObject):
    def __init__(self, opcodes, params, name='<untitled pooz function object>'):
        super(name)
        
        self.__opcodes = opcodes
        self.params = params

        self.set_property('__opcodes__', PoozListObject(self.__opcodes))

    def call(self):
        return self.__opcodes


class PoozStringObject(PoozRootObject):
    def __init__(self, value, name='<untitled pooz string object>'):
        super(name)

        self.__str = value
    
    @property
    def value(self):
        return self.__str


class PoozNativeObject(PoozRootObject):
    def __init__(self, pyobj, name='<untitled python object cover>'):
        super(name)

        self.__pyobj = pyobj

        self.set_property('__native_obj__', self.__pyobj)


class PoozNativeFunction(PoozRootObject):
    def __init__(self, pyfunc, name='<untitled pyfunc cover obj>'):
        super(name)

        self.pyfunc = pyfunc
        
        self.set_property('__pyfuncobj__', pyfunc)

    def call(self, *args):
        return self.pyfunc(*args) #return the return value of pyfunc to vm


class PoozErrorObject(PoozRootObject):
    def __init__(self, error_info='<unknown error type>', name='<untitled error object>'):
        super(name)
        self.set_error_info(info)

    def set_error_info(self, info):
        self.set_property('__error_info__', info)


import pooz_funcs as pfunc

class PoozIntObject(PoozRootObject):
    def __init__(self, pyint, name='<untitled pooz int object>'):
        super(name)

        self._pyint = pyint

    def __initialize(self):
        self.set_property('__add__', 
            PoozNativeFunction(pfunc.pooz_int_add))

        self.set_property('__sub__',
            PoozNativeFunction(pfunc.pooz_int_sub))

        self.set_property('__div__',
            PoozNormalFunction(pfunc.pooz_int_div))

        self.set_property('__muit__',
            PoozNormalFunction(pfunc.pooz_int_muit))

        self.set_property('__surp__',
            PoozNativeFunction(pfunc.pooz_int_surp))


