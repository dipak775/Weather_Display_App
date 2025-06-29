import requests
import pygame
import sys
from datetime import datetime

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animated Weather Display")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 48)

# OpenWeather API settings
API_KEY = "04895bf34e0be0d59c86fc323f54efea"
CITY = "Dhupguri, India"
URL = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"

# Animation variables
rain_drops = []
sun_angle = 0

def get_weather_data():
    response = requests.get(URL)
    return response.json()

def draw_rain():
    for drop in rain_drops:
        pygame.draw.line(screen, BLUE, (drop[0], drop[1]), (drop[0], drop[1] + 10), 2)
        drop[1] += 5
        if drop[1] > HEIGHT:
            drop[1] = 0

def draw_sun():
    global sun_angle
    sun_center = (700, 100)
    pygame.draw.circle(screen, (255, 255, 0), sun_center, 40)
    for i in range(8):
        angle = sun_angle + i * 45
        end_x = sun_center[0] + 60 * pygame.math.Vector2(1, 0).rotate(angle).x
        end_y = sun_center[1] + 60 * pygame.math.Vector2(1, 0).rotate(angle).y
        pygame.draw.line(screen, (255, 255, 0), sun_center, (end_x, end_y), 4)
    sun_angle += 1

def main():
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Fetch weather data
        weather_data = get_weather_data()
        temp = weather_data['main']['temp']
        description = weather_data['weather'][0]['description']
        humidity = weather_data['main']['humidity']
        wind_speed = weather_data['wind']['speed']

        # Display weather information
        temp_text = large_font.render(f"{temp:.1f}°C", True, BLACK)
        screen.blit(temp_text, (50, 50))

        desc_text = font.render(description.capitalize(), True, BLACK)
        screen.blit(desc_text, (50, 120))

        humidity_text = font.render(f"Humidity: {humidity}%", True, BLACK)
        screen.blit(humidity_text, (50, 170))

        wind_text = font.render(f"Wind: {wind_speed} m/s", True, BLACK)
        screen.blit(wind_text, (50, 220))

        time_text = font.render(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), True, BLACK)
        screen.blit(time_text, (50, 270))

        # Animate weather conditions
        if "rain" in description.lower():
            if len(rain_drops) < 100:
                rain_drops.append([pygame.math.Vector2(pygame.math.Vector2(800, 0)).rotate(pygame.math.Vector2(-1, 1).angle_to(pygame.math.Vector2(1, 0))).x, 0])
            draw_rain()
        elif "clear" in description.lower():
            draw_sun()

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()



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
