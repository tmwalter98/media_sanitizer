import os
import re
import hashlib

import media_scanner.regex_patterns as Reg_Utils


class Scanner:
    def __init__(self, hooks):
        self.regs = Reg_Utils.Prepared_Regs()
        self.hooks = hooks
        return

    def scan_files(self, dirs):
        def get_path_sha256(abs_path):
            # Use files' absolute paths to calculate unique key
            file_sha256 = hashlib.sha256(abs_path.encode('utf-8')).hexdigest()
            return file_sha256

        def gen_doc(dirpath, title, extension):
            file_doc = dict()

            if re.search(self.regs.video, extension):
                file_doc['type'] = 'video'
                # print('VIDEO: {}'.format(title))
            elif re.search(self.regs.subtitle, extension):
                file_doc['type'] = 'subtitle'
            else:
                return None

            file_abs_path = '{}/{}.{}'.format(dirpath, title, extension)
            file_doc['_key'] = get_path_sha256(file_abs_path)
            file_doc['abs_path'] = file_abs_path
            file_doc['title'] = title
            file_doc['extension'] = extension
            return file_doc

        db = self.hooks.get('arango')
        arango_col = db.get_async_col('local_movies')
        arango_jobs = []

        for dir in dirs:
            for dirpath, dirnames, files in os.walk(dir):

                for file_name in files:
                    try:
                        name_ext = re.split(self.regs.name_extention,
                                            file_name)
                        title = name_ext[0]
                        extension = name_ext[1]
                        # print('{}.{}'.format(title, extension))

                        # Handles files that have container extension
                        doc = gen_doc(dirpath, title, extension)
                        if doc is not None:
                            arango_jobs.append(arango_col.insert(doc))

                    except re.error:
                        print('Malformed file: ', file_name)
            return
