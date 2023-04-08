from App.Revision import Revision
from App.StudioSetup import StudioSetup
import pickle
import copy


class Mix:
    def __init__(self, studio: StudioSetup):
        self.name = ''
        self._file_name = ''
        self.studio = studio
        self.current_revision = 0
        self.revisions: list[Revision] = []

    def set_studio(self, studio: StudioSetup):
        self.studio = studio
        for r in self.revisions:
            r.set_studio(self.studio)

    def set_filename(self, filename):
        self._file_name = filename

    def get_filename(self):
        return self._file_name

    def is_empty(self):
        return len(self.revisions) == 0

    def new_revision(self, revision_name):
        self.revisions.append(Revision(revision_name, self.studio))
        self.current_revision = len(self.revisions)-1

    def duplicate_revision(self, name):
        new_rev = copy.deepcopy(self.get_current_revision())
        new_rev.name = name
        self.revisions.append(new_rev)
        self.current_revision = len(self.revisions)-1

    def delete_selected_revision(self):
        self.revisions.remove(self.get_current_revision())
        self.current_revision = len(self.revisions)-1
        if self.current_revision < 0:
            self.current_revision = 0

    def get_current_revision(self) -> Revision:
        if len(self.revisions) > 0:
            return self.revisions[self.current_revision]
        return None

    def get_current_revision_name(self) -> str:
        if len(self.revisions) > 0:
            return self.revisions[self.current_revision].name
        return ''

    def get_revisions_names_list(self):
        return [n.name for n in self.revisions]

    def select_revision_by_name(self, name):
        for index in range(len(self.revisions)):
            if self.revisions[index].name == name:
                self.current_revision = index
                return

    def save(self):
        with open(self.get_filename(), 'wb') as f:
            pickle.dump(self, f)
        self.save_txt()

    def save_txt(self):
        txt_filename = self.get_filename()[:-4] + '.txt'
        with open(txt_filename, 'w') as f:
            txt = ''
            for r in self.revisions:
                txt += r.get_str()
            f.write(txt)
