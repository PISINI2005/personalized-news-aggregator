
import io
import webbrowser
import requests
from tkinter import *
from urllib.request import urlopen
from PIL import ImageTk, Image

class NewsApp:

    def __init__(self):
        self.categories = ["business", "entertainment", "general", "health", "science", "sports", "technology"]
        self.data = None 
        self.load_gui()
        self.fetch_news_data(self.selected_category.get())
        self.load_news_item(0)

    def fetch_news_data(self, category):
        api_key = '182f07e3bf994354bee60a1fd96cbd36'  
        url = f'https://newsapi.org/v2/top-headlines?country=us&category={category}&apiKey={api_key}'
        self.data = requests.get(url).json()
    
    def load_gui(self):
        self.root = Tk()
        self.root.geometry('450x700')
        self.root.resizable(0, 0)
        self.root.title('PERSONALIZED NEWS AGGREGATOR')
        self.root.configure(background='black')
        self.selected_category = StringVar(self.root)
        self.selected_category.set("general")  
        category_menu = OptionMenu(self.root, self.selected_category, *self.categories, command=self.change_category)
        category_menu.config(width=15, font=('verdana', 12))
        category_menu.pack(pady=(10, 20))

    def clear(self):
        for widget in self.root.pack_slaves():
            widget.destroy()

    def change_category(self, category):
        self.fetch_news_data(category)
        self.load_news_item(0)

    def load_news_item(self, index):
        self.clear()
        category_menu = OptionMenu(self.root, self.selected_category, *self.categories, command=self.change_category)
        category_menu.config(width=15, font=('verdana', 12))
        category_menu.pack(pady=(10, 20))
        try:
            img_url = self.data['articles'][index].get('urlToImage', 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg')
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)
        except:
            img_url = 'https://www.hhireb.com/wp-content/uploads/2019/08/default-no-img.jpg'
            raw_data = urlopen(img_url).read()
            im = Image.open(io.BytesIO(raw_data)).resize((350, 250))
            photo = ImageTk.PhotoImage(im)

        label = Label(self.root, image=photo)
        label.image = photo  
        label.pack()

        heading = Label(self.root, text=self.data['articles'][index]['title'], bg='black', fg='white', wraplength=350, justify='center')
        heading.pack(pady=(10, 20))
        heading.config(font=('verdana', 15))

        details = Label(self.root, text=self.data['articles'][index]['description'], bg='black', fg='white', wraplength=350, justify='center')
        details.pack(pady=(2, 20))
        details.config(font=('verdana', 12))

        frame = Frame(self.root, bg='black')
        frame.pack(expand=True, fill=BOTH)

        if index != 0:
            prev_button = Button(frame, text='Prev', width=16, height=3, command=lambda: self.load_news_item(index - 1))
            prev_button.pack(side=LEFT)

        read_button = Button(frame, text='Read More', width=16, height=3, command=lambda: self.open_link(self.data['articles'][index]['url']))
        read_button.pack(side=LEFT)

        if index != len(self.data['articles']) - 1:
            next_button = Button(frame, text='Next', width=16, height=3, command=lambda: self.load_news_item(index + 1))
            next_button.pack(side=LEFT)

        self.root.mainloop()

    def open_link(self, url):
        webbrowser.open(url)
obj = NewsApp()
