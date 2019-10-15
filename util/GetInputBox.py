from tkinter import *



def getInputGUI(title, message):
    def return_callback(event):
        print('quit...')
        root.quit()

    root = Tk(className=title)
    root.wm_attributes('-topmost', 1)
    screenwidth, screenheight = root.maxsize()
    width = 300
    height = 100
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
    root.resizable(0, 0)
    lable = Label(root, height=2)
    lable['text'] = message
    lable.pack()
    entry = Entry(root)
    entry.bind('<Return>', return_callback)
    entry.pack()
    entry.focus_set()
    root.mainloop()
    str = entry.get()
    root.destroy()
    return str



if __name__ == '__main__':
    str = getInputGUI("新建人脸特征", "新输入用户名字")
    print(str)



