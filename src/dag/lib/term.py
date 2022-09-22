import re, os, abc
from typing import Optional
from functools import reduce

from dag.lib import platforms


# If ever want to make more portable: Look into using terminfo, py-terminfo

class Terminal():

	def strip_escape_codes(text: str) -> str:
		return text

	def resize_window(rows, cols):
		return


class ANSI(Terminal):
	COLOR_TEXT_BASE = "\x1b[38;5;{xterm_value}m"
	COLOR_BG_TEXT_BASE = "\x1b[48;5;{xterm_value}m"

	COLOR_TEXT_BASE_24B = "\x1b[38;2;{xterm_value}m"
	COLOR_BG_TEXT_BASE_24B = "\x1b[48;2;{xterm_value}m"


	stylemap = {
		"close": "\x1b[0m",
		"bold": "\x1b[1m",
		"b": "\x1b[1m",
		"dim": "\x1b[2m",
		"underline": "\x1b[4m",
		"u": "\x1b[4m",
		"invert": "\x1b[7m",
	}


	# A mapping between hex color values  and their associated ansi color code number
	rgb = {"#000000": "0", "#800000": "1", "#008000": "2", "#808000": "3", "#000080": "4", "#800080": "5", "#008080": "6", "#c0c0c0": "7", "#808080": "8", "#ff0000": "9", "#00ff00": "10", "#ffff00": "11", "#0000ff": "12", "#ff00ff": "13", "#00ffff": "14", "#ffffff": "15"}

	colormap = {"black": "0", "maroon": "1", "green": "2", "olive": "3", "navy": "4", "purple": "5", "teal": "6", "silver": "7", "grey": "8", "red": "9", "lime": "10", "yellow": "11", "blue": "12", "fuchsia": "13", "aqua": "14", "white": "15"}

	ESCAPE_CODE_REGEX = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')


	@classmethod
	def strip_escape_codes(cls, text: str) -> str:
		return cls.ESCAPE_CODE_REGEX.sub('', str(text))


	def resize_window(rows, cols):
		print("\x1b[8;{rows};{cols}t".format(rows=rows, cols=cols))




class XTERM(ANSI):
	# A 256-color mapping between hex values and their associated xterm control sequence number
	rgb = {"#000000": "0", "#800000": "1", "#008000": "2", "#808000": "3", "#000080": "4", "#800080": "5", "#008080": "6", "#c0c0c0": "7", "#808080": "8", "#ff0000": "9", "#00ff00": "10", "#ffff00": "11", "#0000ff": "12", "#ff00ff": "13", "#00ffff": "14", "#ffffff": "15", "#000000": "16", "#00005f": "17", "#000087": "18", "#0000af": "19", "#0000d7": "20", "#0000ff": "21", "#005f00": "22", "#005f5f": "23", "#005f87": "24", "#005faf": "25", "#005fd7": "26", "#005fff": "27", "#008700": "28", "#00875f": "29", "#008787": "30", "#0087af": "31", "#0087d7": "32", "#0087ff": "33", "#00af00": "34", "#00af5f": "35", "#00af87": "36", "#00afaf": "37", "#00afd7": "38", "#00afff": "39", "#00d700": "40", "#00d75f": "41", "#00d787": "42", "#00d7af": "43", "#00d7d7": "44", "#00d7ff": "45", "#00ff00": "46", "#00ff5f": "47", "#00ff87": "48", "#00ffaf": "49", "#00ffd7": "50", "#00ffff": "51", "#5f0000": "52", "#5f005f": "53", "#5f0087": "54", "#5f00af": "55", "#5f00d7": "56", "#5f00ff": "57", "#5f5f00": "58", "#5f5f5f": "59", "#5f5f87": "60", "#5f5faf": "61", "#5f5fd7": "62", "#5f5fff": "63", "#5f8700": "64", "#5f875f": "65", "#5f8787": "66", "#5f87af": "67", "#5f87d7": "68", "#5f87ff": "69", "#5faf00": "70", "#5faf5f": "71", "#5faf87": "72", "#5fafaf": "73", "#5fafd7": "74", "#5fafff": "75", "#5fd700": "76", "#5fd75f": "77", "#5fd787": "78", "#5fd7af": "79", "#5fd7d7": "80", "#5fd7ff": "81", "#5fff00": "82", "#5fff5f": "83", "#5fff87": "84", "#5fffaf": "85", "#5fffd7": "86", "#5fffff": "87", "#870000": "88", "#87005f": "89", "#870087": "90", "#8700af": "91", "#8700d7": "92", "#8700ff": "93", "#875f00": "94", "#875f5f": "95", "#875f87": "96", "#875faf": "97", "#875fd7": "98", "#875fff": "99", "#878700": "100", "#87875f": "101", "#878787": "102", "#8787af": "103", "#8787d7": "104", "#8787ff": "105", "#87af00": "106", "#87af5f": "107", "#87af87": "108", "#87afaf": "109", "#87afd7": "110", "#87afff": "111", "#87d700": "112", "#87d75f": "113", "#87d787": "114", "#87d7af": "115", "#87d7d7": "116", "#87d7ff": "117", "#87ff00": "118", "#87ff5f": "119", "#87ff87": "120", "#87ffaf": "121", "#87ffd7": "122", "#87ffff": "123", "#af0000": "124", "#af005f": "125", "#af0087": "126", "#af00af": "127", "#af00d7": "128", "#af00ff": "129", "#af5f00": "130", "#af5f5f": "131", "#af5f87": "132", "#af5faf": "133", "#af5fd7": "134", "#af5fff": "135", "#af8700": "136", "#af875f": "137", "#af8787": "138", "#af87af": "139", "#af87d7": "140", "#af87ff": "141", "#afaf00": "142", "#afaf5f": "143", "#afaf87": "144", "#afafaf": "145", "#afafd7": "146", "#afafff": "147", "#afd700": "148", "#afd75f": "149", "#afd787": "150", "#afd7af": "151", "#afd7d7": "152", "#afd7ff": "153", "#afff00": "154", "#afff5f": "155", "#afff87": "156", "#afffaf": "157", "#afffd7": "158", "#afffff": "159", "#d70000": "160", "#d7005f": "161", "#d70087": "162", "#d700af": "163", "#d700d7": "164", "#d700ff": "165", "#d75f00": "166", "#d75f5f": "167", "#d75f87": "168", "#d75faf": "169", "#d75fd7": "170", "#d75fff": "171", "#d78700": "172", "#d7875f": "173", "#d78787": "174", "#d787af": "175", "#d787d7": "176", "#d787ff": "177", "#d7af00": "178", "#d7af5f": "179", "#d7af87": "180", "#d7afaf": "181", "#d7afd7": "182", "#d7afff": "183", "#d7d700": "184", "#d7d75f": "185", "#d7d787": "186", "#d7d7af": "187", "#d7d7d7": "188", "#d7d7ff": "189", "#d7ff00": "190", "#d7ff5f": "191", "#d7ff87": "192", "#d7ffaf": "193", "#d7ffd7": "194", "#d7ffff": "195", "#ff0000": "196", "#ff005f": "197", "#ff0087": "198", "#ff00af": "199", "#ff00d7": "200", "#ff00ff": "201", "#ff5f00": "202", "#ff5f5f": "203", "#ff5f87": "204", "#ff5faf": "205", "#ff5fd7": "206", "#ff5fff": "207", "#ff8700": "208", "#ff875f": "209", "#ff8787": "210", "#ff87af": "211", "#ff87d7": "212", "#ff87ff": "213", "#ffaf00": "214", "#ffaf5f": "215", "#ffaf87": "216", "#ffafaf": "217", "#ffafd7": "218", "#ffafff": "219", "#ffd700": "220", "#ffd75f": "221", "#ffd787": "222", "#ffd7af": "223", "#ffd7d7": "224", "#ffd7ff": "225", "#ffff00": "226", "#ffff5f": "227", "#ffff87": "228", "#ffffaf": "229", "#ffffd7": "230", "#ffffff": "231", "#080808": "232", "#121212": "233", "#1c1c1c": "234", "#262626": "235", "#303030": "236", "#3a3a3a": "237", "#444444": "238", "#4e4e4e": "239", "#585858": "240", "#626262": "241", "#6c6c6c": "242", "#767676": "243", "#808080": "244", "#8a8a8a": "245", "#949494": "246", "#9e9e9e": "247", "#a8a8a8": "248", "#b2b2b2": "249", "#bcbcbc": "250", "#c6c6c6": "251", "#d0d0d0": "252", "#dadada": "253", "#e4e4e4": "254", "#eeeeee": "255"
	}

	# A 256-color mapping between xterm color names and their associated xterm control sequence number
	colormap = {"black": "0", "maroon": "1", "green": "2", "olive": "3", "navy": "4", "purple": "5", "teal": "6", "silver": "7", "grey": "8", "red": "9", "lime": "10", "yellow": "11", "blue": "12", "fuchsia": "13", "aqua": "14", "white": "15", "grey0": "16", "navyblue": "17", "darkblue": "18", "blue3": "19", "blue3": "20", "blue1": "21", "darkgreen": "22", "deepskyblue4": "23", "deepskyblue4": "24", "deepskyblue4": "25", "dodgerblue3": "26", "dodgerblue2": "27", "green4": "28", "springgreen4": "29", "turquoise4": "30", "deepskyblue3": "31", "deepskyblue3": "32", "dodgerblue1": "33", "green3": "34", "springgreen3": "35", "darkcyan": "36", "lightseagreen": "37", "deepskyblue2": "38", "deepskyblue1": "39", "green3": "40", "springgreen3": "41", "springgreen2": "42", "cyan3": "43", "darkturquoise": "44", "turquoise2": "45", "green1": "46", "springgreen2": "47", "springgreen1": "48", "mediumspringgreen": "49", "cyan2": "50", "cyan1": "51", "darkred": "52", "deeppink4": "53", "purple4": "54", "purple4": "55", "purple3": "56", "blueviolet": "57", "orange4": "58", "grey37": "59", "mediumpurple4": "60", "slateblue3": "61", "slateblue3": "62", "royalblue1": "63", "chartreuse4": "64", "darkseagreen4": "65", "paleturquoise4": "66", "steelblue": "67", "steelblue3": "68", "cornflowerblue": "69", "chartreuse3": "70", "darkseagreen4": "71", "cadetblue": "72", "cadetblue": "73", "skyblue3": "74", "steelblue1": "75", "chartreuse3": "76", "palegreen3": "77", "seagreen3": "78", "aquamarine3": "79", "mediumturquoise": "80", "steelblue1": "81", "chartreuse2": "82", "seagreen2": "83", "seagreen1": "84", "seagreen1": "85", "aquamarine1": "86", "darkslategray2": "87", "darkred": "88", "deeppink4": "89", "darkmagenta": "90", "darkmagenta": "91", "darkviolet": "92", "purple": "93", "orange4": "94", "lightpink4": "95", "plum4": "96", "mediumpurple3": "97", "mediumpurple3": "98", "slateblue1": "99", "yellow4": "100", "wheat4": "101", "grey53": "102", "lightslategrey": "103", "mediumpurple": "104", "lightslateblue": "105", "yellow4": "106", "darkolivegreen3": "107", "darkseagreen": "108", "lightskyblue3": "109", "lightskyblue3": "110", "skyblue2": "111", "chartreuse2": "112", "darkolivegreen3": "113", "palegreen3": "114", "darkseagreen3": "115", "darkslategray3": "116", "skyblue1": "117", "chartreuse1": "118", "lightgreen": "119", "lightgreen": "120", "palegreen1": "121", "aquamarine1": "122", "darkslategray1": "123", "red3": "124", "deeppink4": "125", "mediumvioletred": "126", "magenta3": "127", "darkviolet": "128", "purple": "129", "darkorange3": "130", "indianred": "131", "hotpink3": "132", "mediumorchid3": "133", "mediumorchid": "134", "mediumpurple2": "135", "darkgoldenrod": "136", "lightsalmon3": "137", "rosybrown": "138", "grey63": "139", "mediumpurple2": "140", "mediumpurple1": "141", "gold3": "142", "darkkhaki": "143", "navajowhite3": "144", "grey69": "145", "lightsteelblue3": "146", "lightsteelblue": "147", "yellow3": "148", "darkolivegreen3": "149", "darkseagreen3": "150", "darkseagreen2": "151", "lightcyan3": "152", "lightskyblue1": "153", "greenyellow": "154", "darkolivegreen2": "155", "palegreen1": "156", "darkseagreen2": "157", "darkseagreen1": "158", "paleturquoise1": "159", "red3": "160", "deeppink3": "161", "deeppink3": "162", "magenta3": "163", "magenta3": "164", "magenta2": "165", "darkorange3": "166", "indianred": "167", "hotpink3": "168", "hotpink2": "169", "orchid": "170", "mediumorchid1": "171", "orange3": "172", "lightsalmon3": "173", "lightpink3": "174", "pink3": "175", "plum3": "176", "violet": "177", "gold3": "178", "lightgoldenrod3": "179", "tan": "180", "mistyrose3": "181", "thistle3": "182", "plum2": "183", "yellow3": "184", "khaki3": "185", "lightgoldenrod2": "186", "lightyellow3": "187", "grey84": "188", "lightsteelblue1": "189", "yellow2": "190", "darkolivegreen1": "191", "darkolivegreen1": "192", "darkseagreen1": "193", "honeydew2": "194", "lightcyan1": "195", "red1": "196", "deeppink2": "197", "deeppink1": "198", "deeppink1": "199", "magenta2": "200", "magenta1": "201", "orangered1": "202", "indianred1": "203", "indianred1": "204", "hotpink": "205", "hotpink": "206", "mediumorchid1": "207", "darkorange": "208", "salmon1": "209", "lightcoral": "210", "palevioletred1": "211", "orchid2": "212", "orchid1": "213", "orange1": "214", "sandybrown": "215", "lightsalmon1": "216", "lightpink1": "217", "pink1": "218", "plum1": "219", "gold1": "220", "lightgoldenrod2": "221", "lightgoldenrod2": "222", "navajowhite1": "223", "mistyrose1": "224", "thistle1": "225", "yellow1": "226", "lightgoldenrod1": "227", "khaki1": "228", "wheat1": "229", "cornsilk1": "230", "grey100": "231", "grey3": "232", "grey7": "233", "grey11": "234", "grey15": "235", "grey19": "236", "grey23": "237", "grey27": "238", "grey30": "239", "grey35": "240", "grey39": "241", "grey42": "242", "grey46": "243", "grey50": "244", "grey54": "245", "grey58": "246", "grey62": "247", "grey66": "248", "grey70": "249", "grey74": "250", "grey78": "251", "grey82": "252", "grey85": "253", "grey89": "254", "grey93": "255"}



def get_terminal() -> Terminal:
	term = os.environ.get("TERM", "")

	if "xterm" in term.lower():
		return XTERM

	return ANSI