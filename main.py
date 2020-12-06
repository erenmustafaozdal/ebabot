"""

✅ ➖ Excel kullanıcı verilerini al
✅ ➖ Tarayıcıyı varsayılan ayarlarda başlat
✅ ➖ Zoom girişini yap (tab 1)
✅ ➖ Yeni bir tab aç
✅ ➖ EBA girişini yap (tab 2)
✅ ➖ Derslerin olduğu excelde gezerek aşağıdakileri yap
    ✅ ➖ Zoom'a dersi kaydet (link ve şifre al)
    ✅ ➖ EBA'ya dersi kaydet

✅ GELECEK PARAMETRELER
👉 user: İşlem yapılacak kullanıcı
👉 delete: Silme işlemi parametresi -> [all]


import pprint
pp = pprint.PrettyPrinter(indent=2)
pp.pprint(data)
exit()

"""

import settings
import classes.log as log
import classes.browser as browser
import classes.command_options as options
import classes.process_time as processClass
import classes.user as usersClass
import classes.lesson as lessonsClass
import classes.zoom as zoomClass
import classes.eba as ebaClass
import time

# komut satırındaki argümanlar alınır
opts = options.Options()

# zaman hesabını için obje oluşturulur
process = processClass.ProcessTime()

# Excel kullanıcı verilerini al
users = usersClass.User(opts.get('user'))
users_data = users.getSelection()

# Kullanıcılar için döngüye gir
for user in users_data:

    # Tarayıcıyı varsayılan ayarlarda başlat
    web = browser.Browser(user)
    zoom = zoomClass.Zoom(web)
    eba = ebaClass.EBA(web)

    # Zoom girişini yap (tab 1)
    zoom.getSchedule()
    # eğer giriş dizini ise kullanıcının giriş yapmasını bekle
    zoom.waitForSignIn(user)

    # EBA girişini yap (tab 2)
    eba.login(user)

    # başlangıç zamanını yazdır
    process.startTime()

    log.write("Kullanıcı: {}".format(user['name']), "header")

    # eğer silme işlemi ise sadece silme yap
    if opts.get('delete') != False:
        zoom.lessonsDelete()
        eba.lessonsDelete()

        log.write("Kullanıcının dersleri silinmiştir: {}".format(user['name']), "header")

        # bitiş zamanını ver farkı yazdır
        process.finishTime(0, True)

        # tarayıcı kapatılır
        web.get().close()
        web.get().quit()
        continue

    # Derslerin olduğu excelde gezerek aşağıdakileri yap
    lessons = lessonsClass.Lesson(user['live_lessons_path'])

    # Zoom'a dersi kaydet (link ve şifre al)
    lessons_data = lessons.all()
    for lesson in lessons_data:
        if lesson['Meeting ID'] == "new" or user["pmi_link"] == "":
            zoom.lessonSave(lesson, lessons.excel)
        else:
            lesson['link'] = user['pmi_link']
            lesson['passcode'] = user['pmi_passcode']
        eba.lessonSave(lesson, lessons.excel)

    log.write("Kullanıcının dersleri bitmiştir: {}".format(user['name']), "header")

    # bitiş zamanını ver farkı yazdır
    process.finishTime(len(lessons_data))

    # tarayıcı kapatılır
    web.get().close()
    web.get().quit()

# import pprint
# pp = pprint.PrettyPrinter(indent=2)
# pp.pprint(users_data)
# exit()
