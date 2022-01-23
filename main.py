from win10toast import ToastNotifier
import tools

to_do = int(input('What to do:\n[1]: Paste Image\n[2]: Text Tool\n'))
match to_do:
    case 1:
        tools.paste_image()
    case 2:
        tools.write_text()

toast = ToastNotifier()
toast.show_toast('OWOP', '"Our world of pixels" task is finished!',
                 icon_path='D:/Pictures/PNG & Clipart/Icon/owop.ico', duration=2)
