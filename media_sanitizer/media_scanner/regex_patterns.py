import re

reg_dict = {
    'video': r'(AVI|FLV|WMV|MP4|MOV|MKV)',
    'subtitle': r'(SRT|SBV|SUB|MPSUB|LRC|CAP|SMI|SAMI|RT|VTT|TTML \
                   |DFXP|SCC|STL|TDS|CIN|ASC|CAP)',
    'name_extention': r'\.([\dA-Za-z]{1,4})$'
}


class Prepared_Regs:
    def __init__(self):
        self.video = re.compile(reg_dict['video'], re.IGNORECASE)
        self.subtitle = re.compile(reg_dict['subtitle'], re.IGNORECASE)
        self.name_extention = re.compile(reg_dict['name_extention'],
                                         re.IGNORECASE)

    def video(self):
        return self.video

    def subtitle(self):
        return self.subtitle

    def name_extention(self):
        return self.name_extention
