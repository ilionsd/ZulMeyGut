# -*- coding: utf-8 -*-

from . import model
from . import line
from ..utility.static_variables import static_variables


class Info :
    def __init__(self) :
        self.__fields = list()
        self.__values = dict()
        
    def add(self, info) :
        info = str(info)
        info_type, _, info = info.partition(model.LINETYPE_SEPARATOR)
        info_type, info = info_type.strip(), info.strip()
        if info_type not in self.__values :
            self.__fields.append(info_type)
            self.__values[info_type] = info


class V4PStyles :
    pass
        
        
class Events :
    def __init__(self) :
        self.__lines = list()
        
    def load(self, lines) :
        if lines is not iter :       
            lines = iter(lines)
        while not model.check_section(model.Section.Events, next(lines)) :
            pass
        fields = line.Format()
        while not fields.load(next(lines)) :
            pass
        lines_list = list()
        next_section = False
        while not next_section :
            current_line = next(lines)
            if not model.isignore(current_line) :
                if model.issection(current_line) :
                    next_section = True
                else :
                    prefix, stripped_line = model.strip_prefix(current_line)
                    prefix = line.typeof_prefix(prefix)
                    if prefix is not None :
                        instance = prefix()
                        instance.fields.reset(fields)
                        if instance.load(stripped_line) :
                            lines_list.append(instance)
        self.__lines = lines_list
            

class Script :
    def __init__(self) :
        self.info   = Info()
        self.styles = V4PStyles()
        self.events = Events()




@static_variables(section_type={
    model.Section.SCRIPT_INFO : Info,
    model.Section.V4P_STYLES  : V4PStyles,
    model.Section.EVENTS      : Events,
})
def typeof_section(section) :
    section = model.Section(section)
    try :
        section = typeof_section.section_type[section]
    except KeyError :
        section = None
    return section

    
        
        
            

















