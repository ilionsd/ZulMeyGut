from . import model
from .exception import BadLoad
from ..utility.static_variables import static_variables


class Ignore:
    def __init__(self):
        self.__ignore = ''

    def load(self, line):
        self.__ignore = line

    def __str__(self):
        return self.__ignore

    @property
    def ignore(self):
        return self.__ignore


class Format:
    def __init__(self, fields=[]):
        if isinstance(fields, Format):
            self.__used = fields.__used
            self.__order = fields.__order
        else:
            self.__used = set()
            self.__order = list()
            self.reset(fields)

    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Format, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Format, model.PREFIX_SEPARATOR, line))
        fields = [field.strip() for field in line.split(model.FIELD_SEPARATOR)]
        self.reset(fields)

    def reset(self, fields=[]):
        fields = list(fields)
        used = set()
        order = list()
        for field in fields:
            if field not in used:
                used.add(field)
                order.append(field)
        self.__used, self.__order = used, order

    def enum_fields(self, section):
        section_fields = model.fieldsof_section(section)
        valid_fields = []
        for field in self.__order:
            if field not in section_fields:
                field = section_fields[field]
            valid_fields.append(field)
        return Format(valid_fields)

    def __repr__(self):
        return repr(self.__order)

    def __str__(self):
        fields = model.FIELD_SEPARATOR.join(self.order)
        prefix = model.Prefix.Format.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, fields)

    def __iter__(self):
        return iter(self.__order)

    def __next__(self):
        return next(self.__order)

    def __len__(self):
        return len(self.__order)

    def __contains__(self, item):
        return item in self.__used

    def __getitem__(self, index):
        return self.__order[index]

    def __setitem__(self, index, field):
        if field in self.__used:
            raise ValueError('Field {} is already used'.format(field))
        self.__used.remove(self.__order[index])
        self.__used.add(field)
        self.__order[index] = field

    def __add__(self, other):
        other = list(other)
        return Format(self.__order + other)

    def __radd__(self, other):
        other = list(other)
        return Format(other + self.__order)

    def __iadd__(self, other):
        other = list(other)
        self.__order += other

    @property
    def order(self):
        return self.__order


class Line :
    def __init__(self, fields=[]):
        self.__fields = Format(fields)
        self.__values = dict()

    def load(self, line):
        values = line.split(model.FIELD_SEPARATOR, maxsplit=len(self.fields) - 1)
        if len(values) < len(self.fields):
            raise BadLoad('Unable to extract {} values from line {}'.format(len(self.fields), line))
        values = [value.strip() for value in values]
        values = [(field, model.typeof_field(field)(value)) for field, value in zip(self.fields, values)]
        self.__values = dict(values)

    def reset(self, values=[]):
        if values is Line:
            self.__fields = values.__fields
            self.__values = values.__values
        else:
            values = list(values)
            values = zip(self.fields, values)
            self.__values = dict(values)

    def __str__(self):
        values = [self.__values[field] for field in self.__fields]
        values = model.FIELD_SEPARATOR.join(values)
        return values

    def __iter__(self):
        self.__fields.__iter__()
        return self

    def __next__(self):
        return self.__values[self.__fields.__next__()]

    def __getitem__(self, field):
        return self.__values[field]

    @property
    def fields(self):
        return self.__fields

    @property
    def values(self):
        return self.__values


class Style(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Style, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Style, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Style.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


class Dialogue(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Dialogue, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Dialogue, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Dialogue.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


class Comment(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Comment, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Comment, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Comment.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


class Picture(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Picture, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Picture, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Picture.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


class Sound(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Sound, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Sound, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Sound.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


class Movie(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Movie, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Movie, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Movie.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


class Command(Line):
    def load(self, line):
        check, line = model.checkstrip_prefix(model.Prefix.Command, line)
        if not check:
            raise BadLoad('Prefix `{}{}` not found in line {}'
                          .format(model.Prefix.Command, model.PREFIX_SEPARATOR, line))
        super.load(line)

    def __str__(self):
        prefix = model.Prefix.Command.name
        separator = model.PREFIX_SEPARATOR
        return '{}{} {}'.format(prefix, separator, super.__str__())


@static_variables(prefix_type={
    model.Prefix.IGNORE   : Ignore  ,
    model.Prefix.Format   : Format  ,
    model.Prefix.Style    : Style   ,
    model.Prefix.Dialogue : Dialogue,
    model.Prefix.Comment  : Comment ,
    model.Prefix.Picture  : Picture ,
    model.Prefix.Sound    : Sound   ,
    model.Prefix.Movie    : Movie   ,
    model.Prefix.Command  : Command ,
})
def typeof_prefix(prefix):
    prefix = model.Prefix(prefix)
    try:
        prefix = typeof_prefix.prefix_type[prefix]
    except KeyError:
        prefix = None
    return prefix


def typeof_line(line):
    prefix, _ = model.strip_prefix(line)
    return typeof_prefix(prefix)
