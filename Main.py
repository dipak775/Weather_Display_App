import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather App")
        self.root.geometry("800x600")

        # Create a frame for the weather information
        self.weather_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.weather_frame.pack(padx=20, pady=20)

        # Create a label for the city name
        self.city_label = tk.Label(self.weather_frame, text="Dhupguri, India", font=("Arial", 24), bg="#f0f0f0")
        self.city_label.pack()

        # Create a label for the temperature
        self.temperature_label = tk.Label(self.weather_frame, text="", font=("Arial", 48), bg="#f0f0f0")
        self.temperature_label.pack()

        # Create a label for the weather description
        self.description_label = tk.Label(self.weather_frame, text="", font=("Arial", 18), bg="#f0f0f0")
        self.description_label.pack()

        # Create a label for the humidity
        self.humidity_label = tk.Label(self.weather_frame, text="", font=("Arial", 18), bg="#f0f0f0")
        self.humidity_label.pack()

        # Create a label for the wind speed
        self.wind_label = tk.Label(self.weather_frame, text="", font=("Arial", 18), bg="#f0f0f0")
        self.wind_label.pack()

        # Create a frame for the weather icon
        self.icon_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.icon_frame.pack(padx=20, pady=20)

        # Create a label for the weather icon
        self.icon_label = tk.Label(self.icon_frame, bg="#f0f0f0")
        self.icon_label.pack()

        # Get the weather data from the OpenWeatherMap API
        self.get_weather_data()

    def get_weather_data(self):
        api_key = "04895bf34e0be0d59c86fc323f54efea"
        city = "Dhupguri, IN"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

        response = requests.get(url)
        data = response.json()

        # Update the weather information labels
        self.temperature_label.config(text=f"{data['main']['temp']}°C")
        self.description_label.config(text=data['weather'][0]['description'])
        self.humidity_label.config(text=f"Humidity: {data['main']['humidity']}%")
        self.wind_label.config(text=f"Wind: {data['wind']['speed']} m/s")

        # Update the weather icon label
        icon_url = f"http://openweathermap.org/img/wn/{data['weather'][0]['icon']}@2x.png"
        response = requests.get(icon_url)
        image_data = response.content
        image = ImageTk.PhotoImage(Image.open(io.BytesIO(image_data)))
        self.icon_label.config(image=image)
        self.icon_label.image= image

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop()
