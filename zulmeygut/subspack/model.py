# -*- coding: utf-8 -*-
import enum

#from . import time
from ..utility.static_variables import static_variables

class AutoKeep :
    KEEPERS = dict()
    
    @staticmethod
    def keeper(name) :
        if not name in AutoKeep.KEEPERS :
            AutoKeep.KEEPERS[name] = AutoKeep()
        return AutoKeep.KEEPERS[name]
            
    def __init__(self) :
        self.__idx = None
        
    def next(self) :
        self.__idx = enum.auto()
        return self.same()
    
    def same(self) :
        return self.__idx

# Best function ever!!!
def zip_fields(*argv) :
    fields = []
    for field in zip(*argv) :
        value = enum.auto()
        for variant in field :
            fields.append( (variant, value) )
    return fields


PREFIX_SEPARATOR = ':'
FIELD_SEPARATOR = ','


Section = enum.Enum(
    value='Section',
    names=zip_fields(
            ('Script Info', 'V4+ Styles', 'Fonts', 'Events', 'Graphics'),
            ('SCRIPT_INFO', 'STYLES    ', 'FONTS', 'EVENTS', 'GRAPHICS')) )


def check_section(expected, line) :
    expected = Section(expected)
    line = line.lstrip('[').rstrip(']')
    return expected.name == line

def issection(line) :
    line = line.lstrip('[').rstrip(']')
    return line in Section


Prefix = enum.Enum( 
    value='Prefix',
    names=zip_fields(
            ('!', 
             'Title', 'Original Script', 'Original Translation', 'Original Editing', 
             'Original Timing', 'Synch Point', 'Script Updated By', 'Update Details', 'ScriptType', 
             'Collisions', 'PlayResY', 'PlayResX', 'PlayDepth', 'Timer', 
             'Format' , 'Style', 'Dialogue', 'Comment', 'Picture', 'Sound', 'Movie', 'Command'),
            ('IGNORE', 
             'TITLE', 'ORIGINAL_SCRIPT', 'ORIGINAL_TRANSLATION', 'ORIGINAL_EDITING', 
             'ORIGINAL_TIMING', 'SYNCH_POINT', 'SCRIPT_UPDATED_BY', 'UPDATE_DETAILS', 'SCRIPTTYPE', 
             'COLLISIONS', 'PLAYRESY', 'PLAYRESX', 'PLAYDEPTH', 'TIMER', 
             'FORMAT' , 'STYLE', 'DIALOGUE', 'COMMENT', 'PICTURE', 'SOUND', 'MOVIE', 'COMMAND')) ) 


def isignore(line) :
    line = str(line)
    return line.startswith(Prefix.IGNORE)

 
def check_prefix(expected, line) :
    expected = Prefix(expected)
    line = str(line)
    return line.startswith(expected.name)


def strip_prefix(line) :
    line = str(line)
    prefix, _, line = line.partition(PREFIX_SEPARATOR)
    return prefix.strip(), line.strip()

def checkstrip_prefix(expected, line) :
    expected = Prefix(expected)
    if not check_prefix(expected, line) :
        return False, line
    else :
        line = line[len(expected.name):].lstrip().lstrip(PREFIX_SEPARATOR).strip()
        return True, line


@static_variables(prefix_dict={
    Section.SCRIPT_INFO : {
        Prefix.TITLE,
        Prefix.ORIGINAL_SCRIPT,
        Prefix.ORIGINAL_TRANSLATION, 
        Prefix.ORIGINAL_EDITING,
        Prefix.ORIGINAL_TIMING, 
        Prefix.SYNCH_POINT, 
        Prefix.SCRIPT_UPDATED_BY, 
        Prefix.UPDATE_DETAILS, 
        Prefix.SCRIPTTYPE, 
        Prefix.COLLISIONS, 
        Prefix.PLAYRESY, 
        Prefix.PLAYRESX, 
        Prefix.PLAYDEPTH, 
        Prefix.TIMER,
    },
    Section.STYLES : {
        Prefix.STYLE,
    },
    Section.FONTS : {},
    Section.EVENTS : {
        Prefix.DIALOGUE, 
        Prefix.COMMENT, 
        Prefix.PICTURE, 
        Prefix.SOUND, 
        Prefix.MOVIE, 
        Prefix.COMMAND,
    },
    Section.GRAPHICS : {},
})
def prefixesof(section) :
    section = Section(section)
    return prefixesof.prefix_dict[section]


Style = enum.Enum(
    value='Style',
    names=zip_fields(
            ('Name', 
             'Fontname', 'Fontsize', 
             'PrimaryColour', 'SecondaryColour', 'OutlineColor', 'BackColour', 
             'Bold', 'Italic', 'Underline', 'StrikeOut', 
             'ScaleX', 'ScaleY', 
             'Spacing', 
             'Angle', 
             'BorderStyle', 'Outline', 'Shadow', 
             'Alignment', 
             'MarginL', 'MarginR', 'MarginV',
             'AlphaLevel', 
             'Encoding'),
            ('NAME', 
             'FONTNAME', 'FONTSIZE', 
             'PRIMARYCOLOUR', 'SECONDARYCOLOUR', 'OUTLINECOLOR', 'BACKCOLOUR', 
             'BOLD', 'ITALIC', 'UNDERLINE', 'STRIKEOUT', 
             'SCALEX', 'SCALEY', 
             'SPACING', 
             'ANGLE', 
             'BORDERSTYLE', 'OUTLINE', 'SHADOW', 
             'ALIGNMENT', 
             'MARGINL', 'MARGINR', 'MARGINV',
             'ALPHALEVEL', 
             'ENCODING')) )


Dialogue = enum.Enum(
    value='Dialogue',
    names=zip_fields(
            ('Layer', 
             'Start', 'End', 
             'Style', 'Name', 
             'MarginL', 'MarginR', 'MarginV', 
             'Effect', 
             'Text'),
            ('LAYER', 
             'START', 'END', 
             'STYLE', 'NAME', 
             'MARGINL', 'MARGINR', 'MARGINV', 
             'EFFECT', 
             'TEXT')) )


@static_variables(field_type={
    #############
    ### Style ###
    #############
    # The name of the Style. Case sensitive. Cannot include commas
    Style.Name : str, 
                
    # The fontname as used by Windows. Case-sensitive
    Style.Fontname : str, 
    #
    Style.Fontsize : int, 
    
    ### Colors ###
    # A long integer BGR (blue-green-red)  value. 
    # ie. the byte order in the hexadecimal equivelent of this number is BBGGRR
    # The color format contains the alpha channel, too. (AABBGGRR)
    
    # This is the colour that a subtitle will normally appear in.
    Style.PrimaryColour   : str, 
    # This colour may be used instead of the Primary colour 
    # when a subtitle is automatically shifted to prevent an onscreen collsion, 
    # to distinguish the different subtitles.
    Style.SecondaryColour : str, 
    # This colour may be used instead of the Primary or Secondary colour 
    # when a subtitle is automatically shifted to prevent an onscreen collsion, 
    # to distinguish the different subtitles
    Style.OutlineColor  : str, 
    # 
    Style.BackColour      : str, 
    
    ### Text ###
    # -1 is True, 0 is False
    Style.Bold      : bool, 
    Style.Italic    : bool, 
    Style.Underline : bool, 
    Style.StrikeOut : bool, 
    
    ### Scale ###
    # Modifies the width and height of the font. [percent]
    Style.ScaleX : int, 
    Style.ScaleY : int, 
    
    # Extra space between characters. [pixels]
    Style.Spacing : int, 
    
    # The origin of the rotation is defined by the alignment. 
    # Can be a floating point number. [degrees]
    Style.Angle : float, 
    
    ### Outline ###
    # 1=Outline + drop shadow, 3=Opaque box
    Style.BorderStyle : int, 
    # If BorderStyle is 1, then this specifies the width of the outline around the text, 
    # in pixels. Values may be 0, 1, 2, 3 or 4. 
    Style.Outline     : int, 
    # If BorderStyle is 1, then this specifies the depth of the drop shadow behind the text,
    # in pixels. Values may be 0, 1, 2, 3 or 4. 
    # Drop shadow is always used in addition to an outline, 
    # SSA will force an outline of 1 pixel if no outline width is given.
    Style.Shadow      : int, 
    
    # This sets how text is "justified" within the Left/Right onscreen margins, 
    # and also the vertical placing. Values may be 1=Left, 2=Centered, 3=Right. 
    # Add 4 to the value for a "Toptitle". Add 8 to the value for a "Midtitle". 
    # eg. 5 = left-justified toptitle
    Style.Alignment : int, 
    
    ### Margins ###
    # The three onscreen margins (MarginL, MarginR, MarginV) define areas 
    # in which the subtitle text will be displayed.
    
    # This defines the Left Margin in pixels. 
    # It is the distance from the left-hand edge of the screen
    Style.MarginL : int, 
    # This defines the Right Margin in pixels. 
    # It is the distance from the right-hand edge of the screen
    Style.MarginR : int, 
    # This defines the vertical Left Margin in pixels.
    # For a subtitle, it is the distance from the bottom of the screen.
    # For a toptitle, it is the distance from the top of the screen.
    # For a midtitle, the value is ignored - the text will be vertically centred
    Style.MarginV : int, 
    
    # This defines the transparency of the text. SSA does not use this yet.
    Style.AlphaLevel : int, 
    
    # This specifies the font character set or encoding and 
    # on multi-lingual Windows installations it provides access to characters 
    # used in multiple than one languages. 
    # It is usually 0 (zero) for English (Western, ANSI) Windows.
    # When the file is Unicode, this field is useful during file format conversions.
    Style.Encoding : int,
    
    ################
    ### Dialogue ###
    ################
	# Subtitles having different layer number will be ignored during the collusion detection.
    # Higher numbered layers will be drawn over the lower numbered. 
    # (any integer)
    Dialogue.Layer : int,
    
    # Start Time of the Event, in 0:00:00:00 format ie. Hrs:Mins:Secs:hundredths. 
    # This is the time elapsed during script playback at which the text will appear onscreen. 
    # Note that there is a single digit for the hours!
    Dialogue.Start : str,
    
    # End Time of the Event, in 0:00:00:00 format ie. Hrs:Mins:Secs:hundredths. 
    # This is the time elapsed during script playback at which the text will disappear offscreen. 
    # Note that there is a single digit for the hours!
    Dialogue.End : str,
    
    # Style name. If it is "Default", then your own *Default style will be subtituted.
    # However, the Default style used by the script author IS stored in the script 
    # even though SSA ignores it - so if you want to use it, the information is there - 
    # you could even change the Name in the Style definition line, 
    # so that it will appear in the list of "script" styles.
    Dialogue.Style : str,
    
    # Character name. This is the name of the character who speaks the dialogue. 
    # It is for information only, to make the script is easier to follow when editing/timing.
    Dialogue.Name : str,
    
    # Margin override. The values are in pixels. 
    # All zeroes means the default margins defined by the style are used.
    Dialogue.MarginL : int,
    Dialogue.MarginR : int,
    Dialogue.MarginV : int,
    
    # Transition Effect. 
    # This is either empty, or contains information for one of the three transition effects 
    # implemented in SSA v4.x
	# The effect names are case sensitive and must appear exactly as shown. 
    # The effect names do not have quote marks around them.
    Dialogue.Effect : str,
    
    # Subtitle Text. This is the actual text which will be displayed as a subtitle onscreen. 
    # Everything after the 9th comma is treated as the subtitle text, so it can include commas.
	# The text can include \n codes which is a line break, 
    # and can include Style Override control codes, which appear between braces { }.
    Dialogue.Text : str,
})
def typeof_field(field) :
    try :
        field = typeof_field.field_type[field]
    except KeyError :
        field = None
    return field


@static_variables(section_fields={
    Section.SCRIPT_INFO : None,
    Section.STYLES      : Style, 
    Section.FONTS       : None,
    Section.EVENTS      : Dialogue,
    Section.GRAPHICS    : None
})
def fieldsof_section(section) :
    try :
        section = fieldsof_section.section_fields[section]
    except KeyError :
        section = None
    return section
































