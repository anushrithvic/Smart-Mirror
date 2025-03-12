from tkinter import *
import datetime
import pytz
from time import strftime
import requests
import os
from geopy.geocoders import Nominatim
from timezonefinder import TimezoneFinder
from PIL import Image, ImageTk
from pygame import mixer
import traceback


def create_smart_mirror():
    try:
        app = Tk()
        app.geometry('1250x780')
        app.title("SMART MIRROR")
        app.resizable(width=0, height=0)
        app.config(background='black')
        newslist = []

        # FUNCTIONS
        def Time():
            newtime = strftime('%H:%M:%S %p')
            l3.config(text=newtime)
            l3.after(1000, Time)

        # to get the latest news
        def getLatestnews():
            try:
                url = "https://newsapi.org/v2/top-headlines?country=us&category=business&apiKey=e590270afeac4ce8bd99e854d39eb4f3"
                news = requests.get(url).json()
                store = news["articles"]
                my_app_articles = []

                for article in store:
                    my_app_articles.append(article['title'])

                for i in range(min(10, len(my_app_articles))):
                    my_news = str(i + 1) + " " + my_app_articles[i]
                    newslist.append(my_news)
                return True
            except Exception as e:
                print(f"Error fetching news: {e}")
                return False

        # to get weather
        def getWeather():
            try:
                city = 'Annur' # your City
                geolocator = Nominatim(user_agent="geoapiExercises")
                location = geolocator.geocode(city)
                obj = TimezoneFinder()
                result = obj.timezone_at(lng=location.longitude, lat=location.latitude)

                # Weather API
                api = "https://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=38bf033c560106770d8f2290c8873771"
                json_data = requests.get(api).json()
                condition = json_data["weather"][0]["main"]
                tempt = int(json_data["main"]["temp"] - 273.15)
                feels_like = int(json_data["main"]["feels_like"] - 273.15)
                press = json_data["main"]["pressure"]
                humid = json_data["main"]["humidity"]
                wind_1 = json_data["wind"]["speed"]

                temp.config(text=(tempt, "°"))
                cond.config(text=(condition, "|", "FEELS", "LIKE", feels_like, "°"))
                wind.config(text=wind_1)
                humidity.config(text=humid)
                pressure.config(text=press)

                # Update weather display periodically
                app.after(600000, getWeather)  # Update every 10 minutes
                return True
            except Exception as e:
                print(f"Error fetching weather: {e}")
                # Still schedule the next update even if this one failed
                app.after(600000, getWeather)
                return False

        # music player
        def musicc():
            try:
                # Initialize mixer
                mixer.init()

                playlist = Listbox(app, selectmode=SINGLE, bg='white', fg='Black', height=5, width=25)
                playlist.place(x=910, y=500)

                # Load music files
                music_dir = r'/Users/anushrithvic/Desktop/music'  # Change to your music directory
                songs = []

                if os.path.exists(music_dir):
                    os.chdir(music_dir)
                    songs = [s for s in os.listdir() if s.endswith('.mp3')]
                    for s in songs:
                        playlist.insert(END, s)
                else:
                    print(f"Music directory does not exist: {music_dir}")
                    playlist.insert(END, "No music files found")

                def playsong():
                    try:
                        selected_song = playlist.get(ACTIVE)
                        if selected_song and selected_song != "No music files found":
                            print(f"Playing: {selected_song}")
                            mixer.music.load(selected_song)
                            mixer.music.play()
                    except Exception as e:
                        print(f"Error playing song: {e}")

                def pausesong():
                    try:
                        mixer.music.pause()
                    except Exception as e:
                        print(f"Error pausing: {e}")

                def resumesong():
                    try:
                        mixer.music.unpause()
                    except Exception as e:
                        print(f"Error resuming: {e}")

                # Create default icons if images fail to load
                play_btn = Button(app, text='▶', command=playsong, bg='White', fg='Black', font=('Arial', 14))
                pause_btn = Button(app, text='⏸', command=pausesong, bg='White', fg='Black', font=('Arial', 14))
                resume_btn = Button(app, text='⏯', command=resumesong, bg='White', fg='Black', font=('Arial', 14))

                # Try to load the image icons
                try:
                    i1 = Image.open(r'Play.png')
                    resize__image1 = i1.resize((20, 20))
                    app.imga1 = ImageTk.PhotoImage(resize__image1)
                    play_btn.config(image=app.imga1, text='')
                except Exception as e:
                    print(f"Error loading play icon: {e}")

                try:
                    i2 = Image.open(r'Resume.png')
                    resize__image2 = i2.resize((20, 20))
                    app.imga2 = ImageTk.PhotoImage(resize__image2)
                    pause_btn.config(image=app.imga2, text='')
                except Exception as e:
                    print(f"Error loading resume icon: {e}")

                try:
                    i3 = Image.open(r'music.png')
                    resize__image3 = i3.resize((20, 20))
                    app.imga3 = ImageTk.PhotoImage(resize__image3)
                    resume_btn.config(image=app.imga3, text='')
                except Exception as e:
                    print(f"Error loading music icon: {e}")

                # Place buttons
                play_btn.place(x=1150, y=530)
                pause_btn.place(x=1150, y=580)
                resume_btn.place(x=1150, y=630)
            except Exception as e:
                print(f"Error setting up music player: {e}")


        # User profile # keep if you need
        '''app.user_photo = None
        try:
            ph = Image.open(r'User.jpg')
            resize__imageph = ph.resize((130, 130))
            app.user_photo = ImageTk.PhotoImage(resize__imageph)
            Label(app, image=app.user_photo).place(x=340, y=140)
        except Exception as e:
            print(f"Error loading user photo: {e}")
            # Create a fallback label if image cannot be loaded
            Label(app, text="👤", font=('Arial', 40), bg='black', fg='white').place(x=380, y=160)'''

        # User greeting
        Label(app, text='Hey Anush !', font=('helvetica', 25, 'bold'),
              bg='black', fg='white').place(x=450, y=270)
        wel = Label(app, text='WELCOME', font=('helvetica', 30, 'bold'),
                    bg='black', fg='white')
        wel.place(x=440, y=310)

        # Date and time display
        date = datetime.datetime.now()
        font1 = ('times', 20, 'bold')
        font2 = ('helvetica', 10, 'bold')
        font3 = ('helvetica', 12, 'bold')
        font4 = ('helvetica', 10, 'bold')

        l1 = Label(app, text=f'{date:%A}', font=font4, bg='black', fg='white')
        l2 = Label(app, text=f'{date:%B %d, %Y}', font="helvetica", bg='black', fg='white')
        l3 = Label(app, font=font1, bg='black', fg='white')

        # Get and display news
        news_success = getLatestnews()
        l4 = Label(app, text="News", font=font3, bg='black', fg='white')

        if news_success and newslist:
            # Create news labels
            for i in range(min(5, len(newslist))):
                Label(app, text=newslist[i], font=font2, bg='black', fg='white').place(x=20, y=530 + i * 30)
        else:
            Label(app, text="Unable to fetch news", font=font3, bg='black', fg='white').place(x=20, y=530)

        # Start time display
        Time()

        # Position date and time
        l1.place(x=20, y=90)
        l2.place(x=20, y=120)
        l3.place(x=20, y=30)
        l4.place(x=20, y=500)

        # Weather display setup
        label10 = Label(app, text="WIND", font=("Georgia", 8, "bold"), bg='black', fg='white')
        label10.place(x=900, y=200)

        label11 = Label(app, text="HUMIDITY", font=("Georgia", 8, "bold"), bg='black', fg='white')
        label11.place(x=960, y=200)

        label12 = Label(app, text="PRESSURE", font=("Georgia", 8, "bold"), bg='black', fg='white')
        label12.place(x=1050, y=200)

        # Temperature and condition labels
        temp = Label(font=("Times New Roman", 35, "bold"), bg='black', fg='white')
        temp.place(x=1035, y=100)

        cond = Label(font=("Times New Roman", 13, "bold"), bg='black', fg='white')
        cond.place(x=920, y=170)

        # Weather data labels
        wind = Label(text="....", font=("Times New Roman", 10, "bold"), bg='black', fg='white')
        wind.place(x=900, y=220)

        humidity = Label(text="....", font=("Times New Roman", 10, "bold"), bg='black', fg='white')
        humidity.place(x=980, y=220)

        pressure = Label(text="....", font=("Times New Roman", 10, "bold"), bg='black', fg='white')
        pressure.place(x=1070, y=220)

        # Load and display weather icon
        app.weather_icon = None
        try:
            i4 = Image.open(r'wheather.png')
            resize__image4 = i4.resize((150, 150))
            app.weather_icon = ImageTk.PhotoImage(resize__image4)
            weathericon = Label(app, image=app.weather_icon, borderwidth=0)
            weathericon.place(x=920, y=50)
        except Exception as e:
            print(f"Error loading weather icon: {e}")
            # Add a fallback weather icon
            Label(app, text="🌤", font=('Arial', 40), bg='black', fg='white').place(x=770, y=70)

        # Music player button
        music_btn = Button(app, text='Play Music', font=("Georgia", 10, "bold"),
                           command=musicc, bg='white', fg='Black', borderwidth=0)
        music_btn.place(x=970, y=470)


        # Start fetching weather
        app.after(1000, getWeather)  # Start weather fetch after 1 second

        return app
    except Exception as e:
        print(f"Fatal error in create_smart_mirror: {e}")
        print(traceback.format_exc())
        # Create a minimal fallback window to avoid NoneType error
        fallback = Tk()
        fallback.title("Smart Mirror (Error Recovery Mode)")
        fallback.geometry("400x200")
        fallback.config(bg="black")
        Label(fallback, text="Smart Mirror encountered an error",
              font=("Arial", 14), bg="black", fg="white").pack(pady=20)
        Label(fallback, text=str(e), font=("Arial", 10),
              bg="black", fg="red").pack(pady=10)
        Button(fallback, text="Exit", command=fallback.destroy).pack(pady=20)
        return fallback


if __name__ == "__main__":
    try:
        app = create_smart_mirror()
        if app:
            app.mainloop()
        else:
            print("Error: App creation failed, returned None")
    except Exception as e:
        print(f"Critical error: {e}")
        print(traceback.format_exc())
