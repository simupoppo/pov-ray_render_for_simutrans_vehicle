import numpy as np
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import os
import povray_render_for_simutrans_vehicle as prfs



def make_window():
    def ask_files():
        path=filedialog.askopenfilename(filetype=[("pov-ray files","*.pov")],defaultextension=".pov")
        file_path.set(path)
    def ask_template():
        output_file_template = filedialog.asksaveasfilename(
            filetype=[("pov-ray files","*.pov")],defaultextension=".pov"
        )
        print(output_file_template)
        prfs.povray_template(output_file_template).make_template()
        file_path.set(output_file_template)
    def set_paksize(input_int):
        if input_int[3:5]=="64":
            return 64
        elif input_int[3:6]=="128":
            return 128
        elif input_int[3:6]=="192":
            return 192
        elif input_int[3:5]=="48":
            return 48
        else:
            try:
                temp_int=int(input_int)
            except:
                try:
                    temp_int=int(input_int[3:])
                except:
                    temp_int=128
            return temp_int
    def app():
        pakstr=(input_pak_box.get())
        paksize=set_paksize(pakstr)
        input_file = file_path.get()
        with_dat=int(makedat_var.get())

        output_file = filedialog.asksaveasfilename(
            filetype=[("PNG Image Files","*.png")],defaultextension=".png"
        )
        print(output_file)
        if not input_file or not output_file or not paksize :
            return
        if (int(paksize))%4!=0 or int(paksize)<0:
            messagebox.showinfo("エラー","4の倍数を指定してください")
            return
        print(pakstr)
        afterfile = prfs.render_povray(input_file,output_file,paksize,pakstr=pakstr)
        temp_flag=afterfile.flag()
        if temp_flag ==0:
            messagebox.showinfo("エラー","画像がありません")
        elif temp_flag ==1:
            makedat_var.set(False)
            messagebox.showinfo("完了","完了しました。")
        elif temp_flag ==2:
            messagebox.showinfo("エラー","画像サイズまたは数値の入力が正しくありません")
        elif temp_flag ==3:
            messagebox.showinfo("エラー","画像出力に失敗しました")
    main_win = tk.Tk()
    main_win.title("simutrans vehicle addon maker with pov-ray")
    main_win.geometry("700x200")
    main_frm = ttk.Frame(main_win)
    main_frm.grid(column=0, row=0, sticky=tk.NSEW, padx=10, pady=10)
    file_path=tk.StringVar()
    folder_label = ttk.Label(main_frm, text="pov-rayファイルを選択")
    folder_box = ttk.Entry(main_frm,textvariable=file_path)
    folder_btn = ttk.Button(main_frm, text="選択",command=ask_files)
    template_btn = ttk.Button(main_frm, text=".povファイルを作成",command=ask_template)
    input_pak_label = ttk.Label(main_frm, text="pak size")
    pak_options=["pak128japan","pak128","pak64","pak192"]
    input_pak_box = ttk.Combobox(main_frm, values=pak_options, state="normal")
    input_pak_box.set("pak128japan")
    makedat_var = tk.BooleanVar()
    makedat_var.set(False)
    makedat_checkbutton = ttk.Checkbutton(main_frm,variable=makedat_var, text="datファイル作成")
   

    app_btn=ttk.Button(main_frm, text="変換を実行",command=app)
    folder_label.grid(column=0,row=0,pady=10)
    folder_box.grid(column=1,columnspan=5,row=0,sticky=tk.EW, padx=5)
    folder_btn.grid(column=6,row=0)
    template_btn.grid(column=4,columnspan=3,row=1)
    input_pak_box.grid(column=1,columnspan=2,row=1,sticky=tk.EW,padx=5)
    input_pak_label.grid(column=0,row=1)
    # makedat_checkbutton.grid(column=4,columnspan=3,row=3,padx=5)
    app_btn.grid(column=1,columnspan=5,row=5)
    #main_win.columnconfigure(0, wieght=1)
    #main_win.rowconfigure(0, wieght=1)
    #main_frm.columnconfigure(1, wieght=1)
    main_win.mainloop()
    