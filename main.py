'''
This Code was created by Nickolas Martin

'''
import feedparser
import time
import sqlite3
import threading
import webbrowser
from tkinter import *
from PIL import Image, ImageTk

DB_NAME = 'blog_database.db'

def upload_sql(text_widget):  
    feeds = [
        "https://www.bleepingcomputer.com/feed/",
        "https://www.darkreading.com/rss.xml",
        "https://feeds.feedburner.com/TheHackersNews",
    ] # News sources to retrieve articles from... can add as many as needed

    while True:  
        connect = sqlite3.connect(DB_NAME)
        cursor = connect.cursor()

        for feed in feeds: # Iterates through each article and inserts new articles to gui and database
            try:
                blog_feed = feedparser.parse(feed)
                new_blog = blog_feed.entries[0]  
                
                cursor.execute("""
                    INSERT INTO blogs (title, link)
                    VALUES (?, ?)
                """, (new_blog.title, new_blog.link))

                text_widget.after(0, update_gui, text_widget, new_blog.title, new_blog.link) # Updates the GUI with the new article

            except Exception:
                pass  
        connect.commit()
        connect.close()
        time.sleep(15)

def update_gui(text_widget, title, link):
    text_widget.insert("insert", f"{title}\n") # Display title
    
    start_idx = text_widget.index("insert") # Index current position
    text_widget.insert("insert", f"{link}\n\n") # Display Link
    end_idx = text_widget.index("insert") # Get end postion of link
    
    tag_link = f"link_{start_idx}" # Tag each link to ensure proper formatting

    text_widget.tag_add(tag_link, start_idx, end_idx) 
    text_widget.tag_config(tag_link, foreground="blue", underline=True)
    text_widget.tag_bind(tag_link, "<Button-1>", lambda e, url=link: webbrowser.open(url))  # Makes link clickable

def gui():
    database() # Starts the Database
    
    window = Tk() # Initializes main gui window
    window.title('Cyber News Feed')

    bg_image = Image.open("gui_files/wallpaper.png")
    bg_image = ImageTk.PhotoImage(bg_image)  

    window_design(window, bg_image)

    frame = Frame(window)  # Frame for scrollbar and text widget
    frame.place(x=30, y=125, width=691, height=349)

    text_widget = Text(frame, wrap="word", height=15)  
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar = Scrollbar(frame, command=text_widget.yview)  
    scrollbar.pack(side="right", fill="y")
    text_widget.config(yscrollcommand=scrollbar.set)

    window.resizable(False, False) # Eventually will incorporate auto scaling

    thread = threading.Thread(target=upload_sql, args=(text_widget,), daemon=True) # Runs upload_sql in seperate function
    thread.start()

    window.mainloop()

def database():
    con = sqlite3.connect(DB_NAME)  
    con.execute(''' 
        CREATE TABLE IF NOT EXISTS blogs (
            title TEXT NOT NULL UNIQUE,
            link TEXT NOT NULL UNIQUE
        );
    ''') # Creates table if not already created
    con.close()

def window_design(window, bg_image): # Designs frame, rectangles, text for gui
    canvas = Canvas(
        window, 
        height=500, 
        width=750, 
        bd=0, 
        relief="ridge", 
        bg="#000000", 
        highlightthickness=0)  
    canvas.create_image(0, 
        0, 
        image=bg_image, 
        anchor="nw")  
    canvas.create_rectangle(
        29.0,
        27.0,
        720.0,
        112.0,
        fill="#042C3A",
        outline="")  
    canvas.create_rectangle(
        29.0,
        124.0,
        720.0,
        473.0,
        fill="#244B5A",
        outline="")  
    canvas.create_text(
        211.0,
        48.0,
        anchor="nw",
        text="Cyber News Feed",
        fill="#FFFFFF",
        font=("Impact", 48 * -1))  
    canvas.pack()

if __name__ == '__main__':
    gui()
