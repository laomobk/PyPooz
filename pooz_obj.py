
class PoozRootObject:
    def __init__(self, name='<untitled object>'):
        self.__propertys = {}

        self.set_property('__name__', name)

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


class PoozNormalFunction(PoozRootObject):
    def __init__(self, opcodes, params, name='<untitled pooz function object>'):
        super(name)
        
        self.__opcodes = opcodes
        self.params = params

        self.set_property('__opcodes__', PoozListObject(self.__opcodes))

    def call(self):
        return self.__opcodes

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


