from win10toast import ToastNotifier
import tools

to_do = int(input('What to do:\n[1]: Paste Image\n[2]: Text Tool\n'))
match to_do:
    case 1:
        im = tools.paste_image()
        done = False
        while not done:
            options = input('[r]: Repeat\n[n]: New image\n[q]: Quit\n')
            match options:
                case 'r':
                    tools.painter(im[0], im[1], im[2], 5, 3)
                case 'n':
                    im = tools.paste_image()
                case 'q':
                    done = True
                case _:
                    print('get gud! try again.')
    case 2:
        tools.write_text()

toast = ToastNotifier()
toast.show_toast('OWOP', '"Our world of pixels" task is finished!',
                 icon_path='D:/Pictures/PNG & Clipart/Icon/owop.ico', duration=2)
