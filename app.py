import glob
import os
import uuid
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import schema as sc

root = tk.Tk()
root.title("JSON Definition Schema View")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("300x200")

label = tk.Label(root, text='Definition name:')
label.config(font=('helvetica', 10))
label.place(x=10, y=10)

entry1 = tk.Entry(root)
entry1.place(x=120, y=10)

label2 = tk.Label(root, text='Directory:')
label2.config(font=('helvetica', 10))
label2.place(x=10, y=50)

entry2 = tk.Entry(root)
entry2.place(x=120, y=50)


def dump_tree(view: ttk.Treeview, parent, tree: dict):
    for key, value in tree.items():
        uid = uuid.uuid4()

        if isinstance(value, sc.SchemaEntry):
            cands_tab = '' if value.is_object_list() else '|'.join([str(elem) for elem in value.get_candidates()])
            types_tab = 'object list' if value.is_object_list() else ', '.join(value.get_types())
            view.insert(parent, 'end', uid, text=key, values=(types_tab, cands_tab))

            if value.is_object_list():
                dump_tree(view, uid, value.get_candidates()[0])
        elif isinstance(value, dict):
            view.insert(parent, 'end', uid, text=key, value='object')
            dump_tree(view, uid, value)
        elif isinstance(value, tuple) or isinstance(value, list) or isinstance(value, set):
            view.insert(parent, 'end', uid, text=key, value='list')
            dump_tree(view, uid, dict([(i, x) for i, x in enumerate(value)]))
        else:
            view.insert(parent, 'end', uid, text=key, value=value)


def display_tree_view(def_name: str, data: dict) -> None:
    root.title('Definition ' + def_name + ' Schema View')
    root.resizable(height=True, width=True)
    root.geometry("600x400")
    root.minsize(root.winfo_reqwidth(), root.winfo_reqheight())

    view = ttk.Treeview(root, columns=('t', 'c'))
    view.column('t', width=100, anchor='center')
    view.heading('t', text='Types')
    view.column('c', width=100, anchor='center')
    view.heading('c', text='Candidates')
    dump_tree(view, '', data)

    vsb = ttk.Scrollbar(root, orient="vertical", command=view.yview)
    vsb.pack(side='right', fill='y')

    hsb = ttk.Scrollbar(root, orient="horizontal", command=view.xview)
    hsb.pack(side='bottom', fill='x')

    view.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
    view.pack(fill=tk.BOTH, expand=1)


def browse_file():
    directory = filedialog.askdirectory(parent=root, title='Choose a directory')
    if directory:
        entry2.delete(0, tk.END)
        entry2.insert(0, directory)


def create_def():
    if len(entry1.get()) > 0 and len(entry2.get()) > 0 and os.path.isdir(entry2.get()):
        label.pack_forget()
        entry1.pack_forget()
        label2.pack_forget()
        entry2.pack_forget()
        browse.pack_forget()
        button1.pack_forget()

        schema = sc.create_definition_schema(entry1.get(), glob.glob(entry2.get() + '/*.json'))
        display_tree_view(entry1.get(), schema.get_entries())


browse = tk.Button(text='Browse', command=browse_file)
browse.place(x=250, y=50)

button1 = tk.Button(text='Create', command=create_def)
button1.place(x=80, y=100, height=50, width=150)

root.update_idletasks()
root.resizable(height=False, width=False)
root.mainloop()
