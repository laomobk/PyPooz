'''

    $&&&                    $$$$$$$$$
    $    $                         $
    $   $                        $
    $$      $$$$$   $$$$$$      $
    $       $   $   $    $     $       $
    $       $$$$$   $$$$$$  $$$$$$$$$$$

'''

#TODO : Finish this machine in 3 days...

import shlex

#status:
STATE_FUNCTION = 0
STATE_NORMAL = 1

_input_file = None
_op_blocks = {}

def collect_functions():
    temp_line = []

def to_string(*ch):
    return ''.join(((chr(int(x)) for x in ch)))

import pooz_error
from pooz_error import raise_interpreter_error as error
import pooz_obj as pobj

def cause_error(line, info):
    pooz_error.raise_interpreter_error(line, info)

class PoozInterpreter:
    def __init__(self):
        self.consts = []
        self.frames = []
        self.lnptr = 0

        self.__now_line_obj = None

        self.error_pool = pobj.PoozListObject(name='__ERROR_ITEMS__') #it is a pooz list object

        self.opblock_stack = [] # Push opcodes of the function which will be invoke. 

        self.opblock_max_line_num = 0

        self.state = STATE_NORMAL

    def run(self, opblock):
        '''opblock should be PoozOpBlock object'''

        max_line_num = opblock.last_line.line_no

        func_op_lnptr = 0

        #mainloop
        while True:
            if self.state == STATE_NORMAL and self.lnptr <= max_line_num: #normal mode
                if self.lnptr in opblock:
                    self.execute_instructions(opblock[self.lnptr])
                self.lnptr += 1

            elif self.state == STATE_FUNCTION: #function mode
                if func_op_lnptr in self.top_opblock and func_op_lnptr <= self.opblock_max_line_num:
                    self.execute_instructions(self.top_opblock[func_op_lnptr])

                elif func_op_lnptr > self.opblock_max_line_num:
                    error(self.__now_line, 
                        'line number out of opblock ({0} but now is {1})'
                            .format(self.opblock_max_line_num, func_op_lnptr))

                func_op_lnptr += 1
    
    @property
    def __now_line(self):
        return self.__now_line_obj.origin_line

    def top_frame(self):
        return self.frames[-1]

    def global_frame(self):
        return self.frames[0]

    def push_frame(self, frame):
        self.frames.append(frame)

    def pop_frame(self):
        self.frames.pop()

    def add_global(self, name, value):
        self.top_frame().local_var[name] = value

    def push_error(self, error):
        self.error_pool.add_item(error)
    
    '''
    def del_global(self, name):
        del self.top_frame().local_var[name]
    '''

    def execute_instructions(self, line):
        pass

    @property
    def top_opblock(self):
        return self.opblock_stack[-1]

    def to_number(self, value, v_type='int'):
        try:
            if v_type == 'float':
                return float(value)

            elif v_type == 'int':
                return int(value)

        except:
            cause_error(self.__now_line, 'Required {0}')

    def get_arguments(self):
        args = []

        while not self.top_frame().stack:
            args.append(self.pop_top_frame_stack)

        return args

    def get_const(self, index):
        index = self.to_number(index)
        try:
            return self.consts[index]
        except IndexError:
            error(self.__now_line, 'Index {0}'.format(index))

    def get_var(self, name, location='local'):
        try:
            if location == 'global':
                self.global_frame.local_vars[name]

            elif location == 'local':
                '''search order: <local -> global>'''
                try:
                    self.top_frame.local_vars[name]
                except:
                    self.global_frame.local_vars[name]

        except KeyError:
            error(self.__now_line, 'name {0} is not defind')

    def push_top_frame_stack(self, value):
        self.top_frame.stack.append(value)

    def pop_top_frame_stack(self):
        self.top_frame.stack.pop()

    def general_operation(self, mode):
        l = self.pop_top_frame_stack()
        r = self.pop_top_frame_stack()

        return {
                'add' : lambda l, r:l + r,
                'sub' : lambda l, r:r - l,
                'muit': lambda l, r:l * r,
                'div' : lambda l, r:r / l,
                'floor' : lambda l, r : r // l
               }.get(mode, lambda _, __ : error(self.__now_line, 'Unknown mode:{0}'.format(mode)))(l, r)


    # ----Instructions----

    def const_str(self, args):
        str_temp = to_string(*args)
        self.consts.append(str_temp)

    def const_int(self, args):
        self.consts.append(self.to_number(args, 'int'))

    def const_float(self, args):
        self.consts.append(self.to_number(args, 'float'))

    def load_const(self, index):
        self.push_top_frame_stack(self.get_const(self.to_number(index)))

    def load_fast(self, index):
        self.get_var(self.get_const(index))

    def load_global(self, index):
        self.get_var(self.get_const(index), 'global')

    def add(self, _):
        self.general_operation('add')

    def sub(self, _):
        self.general_operation('sub')

    def div(self, _):
        self.general_operation('div')

    def muit(self, _):
        self.general_operation('muit')

    def floor(self, _):
        self.general_operation('floor')

    def comp_op(self, argv):
        a = self.pop_top_frame_stack()
        b = self.pop_top_frame_stack()

        res = {
               1 : lambda a, b : a >  b, # >
               2 : lambda a, b : a <  b, # <
               3 : lambda a, b : a >= b, # >=
               4 : lambda a, b : a <= b, # <=
               5 : lambda a, b : a == b, # ==
              }.get(self.to_number(argv), 
                    lambda : error(self.__now_line, 'Operater index {0}'.format(argv)))

        self.push_top_frame_stack(res)

    def jump(self, argv):
        self.lnptr = self.to_number(argv)

    def if_else_jump(self, argv):
        cmp_res = self.pop_top_frame_stack()
        if cmp_res == 0:
            self.jump(self.to_number(argv))

    def raise_item(self, _):
        info = self.pop_top_frame_stack()

        self.push_error(pobj.PoozErrorObject(info))

    def call_native(self, args):
        func_name = self.consts[self.to_number(args)]
        func_obj = None #native func obj
        #find func object location in local then global
        #python 'function' object is just like a normal object in pooz

        import inspect

        if func_name in self.top_frame().local_var:
            temp_fobj = self.top_frame().local_var[func_name]

            if not inspect.isfunction(temp_fobj):
                self.push_error(pobj.PoozErrorObject('{0} is not a python function object'.format(func_name)))
                return

            func_obj = temp_fobj
        
        elif func_name in self.global_frame().local_var:
            temp_fobj = self.global_frame().local_var[func_name]
            
            if not inspect.isfunction(temp_fobj):
                self.push_error(pobj.PoozErrorObject('{0} is not a python function object'.format(func_name)))
                return
            
            func_obj = temp_fobj

        else:
            self.push_error(pobj.PoozErrorObject('{0} is not define!'.format(func_name)))
            return

        args = self.get_arguments()

        rtn = func_obj.call(*args)
        rtn_cover = pobj.PoozNativeObject(rtn, '<return value of {0} function>'.format(func_name))

        self.push_top_frame_stack(rtn)

    def call_func(self, argv):
        func_obj = self.pop_top_frame_stack()
        
        if isinstance(func_obj, pobj.PoozNormalFunction):
            error(self.__now_line, 'target is not a pooz function!')

        self.opblock_stack.append(func_obj.call())
        self.state = STATE_FUNCTION
        
        args = self.get_arguments() #get arguments from top stack

        if len(args) != len(func_obj.params):
            self.push_error(pobj.PoozErrorObject('Need {0} but found {1}'.format(len(func_obj.params), len(args))))
            return

        #push new frame
        self.push_frame(PoozFrame(func_obj))

        #push var into top frame
        for i in range(len(args)):
            self.top_frame.local_var[func_obj.params[i]] = args[i] 
        

class PoozFrame:
    __slots__ = ('func_master', 'stack', 'local_var')

    def __init__(self, func_master):
        self.func_master = func_master
        self.stack = self.local_var = []

class PoozOpBlock:
    def __init__(self, lines):
        self.__lines = lines
        self.__final_lines = {}

    def __deal_with__lines(self):
        for ln in self.__lines:
            self.__final_lines[ln.line_no] = ln

    def __getitem__(self, line):
        return self.__final_lines[line]

    def __contains__(self, value):
        return value in self.__final_lines

    @property
    def last_line(self):
        return self.__final_lines.items()[1]


class PoozSingleLine:
    __slots__ = ('origin_line', 'args', 'instruction')

    def __init__(self, origin_line):
        self.origin_line = origin_line
        
        self.line_no = self.args = self.instruction = None

        self.__parse_line(origin_line)

    def __repr__(self):
        return 'PoozSingleLine({0.origin_line})'.format(self)

    def __parse_line(self, line):
        self.line_no, \
        self.instruction, \
        *self.args = shlex.split(line)
        
        try:
            self.line_no = int(self.line_no)
        except:
            cause_error(self.origin_line, 'line number should be int')
