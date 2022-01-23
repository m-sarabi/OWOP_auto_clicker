from win10toast import ToastNotifier
import tools

to_do = int(input('What to do:\n[1]: Painter\n[2]: Text Tool\n'))
match to_do:
    case 1:
        tools.painter()
    case 2:
        # text_tool()
        print('adding text tool soon!')

toast = ToastNotifier()
toast.show_toast('OWOP', '"Our world of pixels" task is finished!',
                 icon_path='D:/Pictures/PNG & Clipart/Icon/owop.ico', duration=2)
