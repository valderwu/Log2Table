import pandas as pd
import copy
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

class LC:
    def __init__(self, win):
        self.conf_df = pd.read_excel("cmds.xlsx")
        self._funcs = self.conf_df["Cmd_Chi"].unique()
        self._opts = (0,)
        self.widgets = {}
        self.create_widgets(win)
        self.script = []
        self.cmd_chi = ''
        self.opt_chi = ''
        self.selected_row = ''
        self.args = {}
        self.cmd = ""

    #Cmd_chi 下拉框
    def create_list1(self, parent):
        def set_cmdchi(event):
            self.cmd_chi = event.widget.get()
            self._opts = self.conf_df[self.conf_df["Cmd_Chi"]== self.cmd_chi]["Opt_Chi"]
            self.widgets['comboxlist2']["values"]=tuple(self._opts)
            self.widgets['comboxlist2'].current(0)
            self.opt_chi = self.widgets["comboxlist2"].get()
            self.create_args_entry(parent)
        comvalue1 = StringVar()
        comboxlist1 = ttk.Combobox(win, textvariable=comvalue1)
        comboxlist1["values"]=tuple(self._funcs)
        comboxlist1.current(0)  #选择第一个  
        comboxlist1.bind("<<ComboboxSelected>>", set_cmdchi) #绑定事件,(下拉列表框被选中时，绑定go()函数)  
        comboxlist1.pack()
        self.widgets["comboxlist1"] = comboxlist1

    #Opt_chi 下拉框
    def create_list2(self, parent):
        def set_optchi(event):
            self.opt_chi = event.widget.get()
            comboxlist2["values"]=tuple(self._opts)
            self.create_args_entry(parent)

        comvalue2 = StringVar()
        comboxlist2 = ttk.Combobox(win, textvariable=comvalue2)
        comboxlist2["values"]=tuple(self._opts)
        comboxlist2.current(0)  #选择第一个  
        comboxlist2.bind("<<ComboboxSelected>>", set_optchi) #绑定事件,(下拉列表框被选中时，绑定go()函数)
        comboxlist2.pack()
        self.widgets["comboxlist2"] = comboxlist2

    #参数输入框
    def create_args_entry(self, parent):
        widgets_c = copy.copy(self.widgets)
        for name, widget in widgets_c.items():
            if isinstance(name, tuple):
                widget['widget'].destroy()
                self.widgets.pop(name)
        del widgets_c
        self.selected_row = self.conf_df[ (self.conf_df["Cmd_Chi"]==self.cmd_chi) & (self.conf_df["Opt_Chi"]==self.opt_chi) ]
        args_info = self.selected_row.iloc[0].loc["Arg_Chi"]
        args_dict = {args_info.split(':')[0].strip():args_info.split(':')[1].strip() for args_info in args_info.split("；")}
        arg_count = 0
        for arg, description in args_dict.items():
            arg_count += 1
            entry_name = (arg,)
            e = Variable()
            entry = Entry(parent, textvariable=e)
            e.set("~"+description+"~")
            entry.pack()       
            self.widgets[entry_name] = {'widget':entry, 'var':e}

    def create_submit_button(self, parent):
        def submit():
            for name, widget in self.widgets.items():
                if isinstance(name, tuple):
                    print(widget['var'].get())
                    arg_value = widget['var'].get()
                    if arg_value.startswith("~") and arg_value.endswith("~"):
                        messagebox.showwarning("请输入参数")
                        return
                    self.args[name[0]] = widget['var'].get() #将输入框内容写入参数字典
            self.generate_cmd()
            # self.cmd_chi = ''
            # self.opt_chi = ''
            # self.selected_row = ''
            # self.args = {}
            # self.cmd = ""
        submit_button = Button(win, text='提交',
                         command=submit,
                         width=10,
                         height=1)
        submit_button.pack()

    def create_widgets(self, win):
        #=============wigets=====================
        #Up
        frm_U = Frame(win)
        self.create_list1(frm_U)
        self.create_list2(frm_U)
        #参数编辑框(动态生成)
        #提交button
        self.create_submit_button(frm_U)
        #执行button
        frm_U.pack(side=TOP)

        #----------------------------------------
        #Middle
        frm_M = Frame(win)
        #解释框
        frm_M.pack()

        #----------------------------------------      
        #Down
        frm_D = Frame(win)
        #script 显示text框
        frm_D.pack(side=BOTTOM)

    def generate_cmd(self):
        cmd = self.selected_row.iloc[0].loc["Cmd"]
        #预处理命令中的\{\}
        cmd = cmd.replace("\{", '((').replace("\}", "))")
        #填充参数组成命令
        print(self.args)
        cmd = cmd.format(**self.args)
        #还原{}
        self.cmd = cmd.replace("((", '{').replace("))", "}")
        self.script.append(self.cmd)
        print(self.cmd)


import tkinter as tk

win = Tk()
win.title("Log Master")
win.geometry('400x600')
lc = LC(win)
win.mainloop()

lc = LC()
cmd = lc.gen_cmd("拆分文件", "倒数列号")
print(cmd)