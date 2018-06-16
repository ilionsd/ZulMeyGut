# -*- coding: utf-8 -*-
import numpy as np

from . import model
from . import line
from .exception import BadLoad


class Info:
    def __init__(self):
        self.__fields = list()
        self.__values = dict()

    def add(self, info):
        info = str(info)
        info_type, _, info = info.partition(model.LINETYPE_SEPARATOR)
        info_type, info = info_type.strip(), info.strip()
        if info_type not in self.__values:
            self.__fields.append(info_type)
            self.__values[info_type] = info


class FormattedSection:
    @staticmethod
    def make_from_dict():
        
    
    def __init__(self, section, fields=[]):
        self.__section = model.Section(section)
        self.__prefixes = np.array([])
        self.__fields = line.Format(fields).enum_fields(self.__section)
        self.__entries = {field: np.array([], dtype=model.typeof_field(field)) for field in self.fields}
        self.__length = 0

    def reset(self, fields=[]):
        fields = line.Format(fields)
        entries = dict()
        for field in fields:
            try:
                entries[field] = self.entries[field]
            except KeyError:
                entries[field] = np.full(self.length, model.typeof_field(field)())
        self.__fields, self.__entries = fields, entries

    def load(self, lines):
        if lines is not iter:
            lines = iter(lines)
        current_line = ''
        while not model.check_section(self.fields.section, current_line):
            try:
                current_line = next(lines).strip()
            except StopIteration:
                raise BadLoad('Section {} not found in {}'.format(self.fields.section, lines))
        fields = line.Format(self.fields.section)
        current_line = ''
        while not current_line or model.isignore(current_line):
            try:
                current_line = next(lines).strip()
            except StopIteration:
                raise BadLoad('Unexpected end of lines {}'.format(lines))
            else:
                if model.issection(current_line):
                    raise BadLoad('Unexpected end of section {} in lines {}'
                                  .format(self.fields.section, lines))
        try:
            fields.load(current_line)
        except BadLoad as err:
            raise BadLoad('First prefix line of section {} is not a Format in {}. Nested {}'
                          .format(fields.section, lines, err))
        prefixes = np.array([])
        entries = {field: np.array([], dtype=model.typeof_field(field)) for field in fields}
        length = 0
        next_section = False
        eof = False
        while not next_section and not eof:
            try:
                current_line = next(lines).strip()
            except StopIteration:
                eof=True
            else:
                if current_line and not model.isignore(current_line):
                    if model.issection(current_line):
                        next_section = True
                    else:
                        prefix, stripped_line = model.strip_prefix(current_line)
                        prefix = model.Prefix[prefix]
                        if prefix in model.prefixesof(fields.section):
                            entry = stripped_line.split(model.FIELD_SEPARATOR, maxsplit=len(fields) - 1)
                            entry = [item.strip() for item in entry]
                            entry = dict(zip(fields, entry))
                            prefixes = np.append(prefixes, line.typeof_prefix(prefix))
                            for field in fields:
                                entries[field] = np.append(entries[field], entry[field])
                            length += 1
        self.__fields.reset(fields)
        self.__prefixes, self.__entries, self.__length = prefixes, entries, length

    class EntryIterator:
        def __init__(self, section):
            self.__section = section
            self.__index = 0

        def __iter__(self):
            return self

        def __next__(self):
            if self.__index >= len(self.__section):
                raise StopIteration()
            entry = self.__section[self.__index]
            self.__index += 1
            return entry

    def __repr__(self):
        return repr(self.__entries)

    def __iter__(self):
        return self.EntryIterator(self)

    def __len__(self):
        return self.__length

    def column(self, key):
        return self.__entries[key]

    def select(self, *args):
        selected_fields = line.Format(self.fields.section)
        section_fields = model.fieldsof_section(self.fields.section)
        for arg in args:
            if arg is not section_fields:
                arg = section_fields[arg]
            if arg in self.__entries:
                selected_fields += arg
        selected_section = FormattedSection(self.fields.section)
        selected_section.reset(section_fields)
        for arg in args:
            if arg is not section_fields:
                arg = section_fields[arg]
            if arg in self.__entries:
                selection[arg] = self.__entries[arg]
        return selection

    def where(self, mask):
        here = dict()
        for field, values in self.__entries:
            here[field] = values[mask]
        return here

    def __getitem__(self, index):
        if index in self.fields:
            return self.__entries[index]
        else:
            if index >= len(self):
                raise IndexError('Index {} is out of bounds {}.'.format(index, len(self)))
            entry = self.__prefixes[index](self.__fields)
            entry.reset([self.__entries[field][index] for field in self.fields])
            return entry

    def __setitem__(self, index, entry):
        if index in self.fields:
            self.__entries[index] = entry
        else:
            if index >= len(self):
                raise IndexError('Index {} is out of bounds {}.'.format(index, len(self)))
            if type(entry) not in line.typeof_prefix.prefix_type.values():
                raise ValueError('Unexpected type {} of entry {}'.format(type(entry), entry))
            for field in self.fields:
                self.__entries[field][index] = entry[field]
            self.__prefixes[index] = type(entry)

    @property
    def fields(self):
        return self.__fields


class Script:
    def __init__(self):
        self.info = Info()
        self.styles = FormattedSection(model.Section.STYLES)
        self.events = FormattedSection(model.Section.EVENTS)





















