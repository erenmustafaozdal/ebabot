import settings
from consolemenu import SelectionMenu
import classes.log as log
from classes.model import Model

class User(Model):
    """docstring for User"""
    def __init__(self, opt_user):
        super(Model, self).__init__()
        self.opt_user = opt_user
        self._rows = []
        self.excel = self.excel(settings.users_xl)
        self.headers = self.getHeaders(self.excel.sheet)
        self.getRows(self.excel.sheet)
        # kullanıcı verilerinde float olanları düzelt
        users = []
        for row in self._rows:
            for key in self.headers:
                if isinstance(row[key], float):
                    row[key] = str(int(row[key]))
            if self.opt_user == "" or self.opt_user == False or (self.opt_user in [str(row['id']), row['name'], row['zoom_email'], row['edevlet_tc']]):
                users.append(row)
        self._rows = users

    def getSelection(self):
        # Eğer Kullanıcı sayısı 0 ise dur
        if len(self._rows) == 0:
            log.write("Kullanıcı olmadığı için program durduruldu.", "error")
            exit()

        # Kullanıcı seçimi yaptır
        users_data = self._rows
        if self.opt_user == False:
            user_ids = self.ids()
            selection_list = ["Tüm Kullanıcılar"] + self.get('name')
            selection = SelectionMenu.get_selection(selection_list, title="EBABOT - HARİCİ CANLI DERS", subtitle="Lütfen işlem yapılacak kullanıcı seçimi yapın.", show_exit_option=False)
            if selection != 0:
                users_data = [self.find(user_ids[selection-1])]

        log.write("{} kullanıcı alındı.".format(len(users_data)), "header")

        return users_data
