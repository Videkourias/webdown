import controller as con
import tkinter as tk
from tkinter import messagebox


# Root window (constants)
root = tk.Tk()

# Configure window
root.title('Web Down')
root.geometry("450x200")


# Clears screen of all widgets
def clearscreen():
    for widget in root.winfo_children():
        widget.destroy()


# Submits URL for verification, moves window to next stage if URL is valid
# Also clears the entrybox (urlstring) if invalid
def verifyURL(url, urlstring):
    if con.verify(url):
        clearscreen()
        optionsWindow(con.getInfo(url))
    else:
        messagebox.showwarning('Warning', 'Invalid URL')
        urlstring.set('')


def verifyOptions(info):
    if info['author'] and info['title'] and info['desc']:
        con.main(info)
        messagebox.showinfo('Information', 'Book download complete! :)')
        print("Book download complete! :)")
        back()
    else:
        messagebox.showwarning('Warning', 'Fill in all empty fields')
        print("Fill in all empty fields")


# Returns to default window
def back():
    clearscreen()
    defaultWindow()


# Defines and formats available given the URl provided
def optionsWindow(info):
    url = info['url']

    # Create data for widgets
    author = tk.StringVar()
    title = tk.StringVar()
    desc = tk.StringVar()
    author.set(info['author'])
    title.set(info['title'])
    desc.set(info['desc'].text)

    # Create widgets
    url_label = tk.Label(root, text='URL: {}'.format(url))
    chapters_label = tk.Label(root, text='Chapters: {}'.format(info['chapters']))
    author_label = tk.Label(root, text='Author: ')
    title_label = tk.Label(root, text='Title: ')
    desc_label = tk.Label(root, text='Description: ')

    author_entry = tk.Entry(root, textvariable=author, width=50)
    title_entry = tk.Entry(root, textvariable=title, width=50)
    desc_entry = tk.Entry(root, textvariable=desc, width=50)

    create_button = tk.Button(root, text='Create', command=lambda: verifyOptions({
        "url": url,
        "author": author_entry.get(),
        "title": title_entry.get(),
        "desc": desc_entry.get(),
        "chapters": info['chapters'],
        "initial": info['initial']
    }))
    back_button = tk.Button(root, text='<-', command=back)

    # Format widgets
    back_button.grid(row=0)
    url_label.grid(row=1, columnspan=2)
    chapters_label.grid(row=2, columnspan=2)

    author_label.grid(row=3, column=0)
    author_entry.grid(row=3, column=1)

    title_label.grid(row=4, column=0)
    title_entry.grid(row=4, column=1)

    desc_label.grid(row=5, column=0)
    desc_entry.grid(row=5, column=1)

    create_button.grid(row=6, columnspan=2)


# Defines the default widgets and format on startup of program
def defaultWindow():
    # Create widgets
    url = tk.StringVar()
    url_label = tk.Label(root, text='Enter a URL')
    url_entry = tk.Entry(root, textvariable=url, width=60)

    submit_button = tk.Button(root, text='Submit', command=lambda: verifyURL(url_entry.get().strip(), url))

    # Format widgets on grid
    url_label.grid(row=0, column=0)
    url_entry.grid(row=0, column=1)

    submit_button.grid(row=1, columnspan=3)

    # Convenience settings
    root.bind('<Return>', lambda event: verifyURL(url_entry.get().strip(), url))

    url_entry.focus()


# Initialize
defaultWindow()
root.mainloop()
