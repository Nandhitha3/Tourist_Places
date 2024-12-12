import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

os.chdir('C:\\Users\\nithy\\Desktop')

class TouristGuide:
    def __init__(self, root):
        self.root = root
        self.root.title("Tourist Guide and Planner")
        self.places = {
            'Maharashtra': {
                'attractions': {
                    'Harihar Fort': 'https://maps.app.goo.gl/bPHsEm8mggJR9UUz5',
                    'The Shri Trimbakeshwar Shiva Temple': 'https://maps.app.goo.gl/q2uEYF6KWix6Dmtu8',
                    'Dugarwadi': 'https://maps.app.goo.gl/Zb1xJQ6qcfbbAMtE8'
                },
                'hotels': {
                    'Three leaves hotel': 'https://maps.app.goo.gl/8bduSrbey7btCHaB7',
                    'Hotel sal yathri': 'https://maps.app.goo.gl/Fr6gLhRHN1BNhRGM6',
                }
            },
           'Udaipur': {
               'attractions': {
                   'Saheliyon ki bari': 'https://maps.app.goo.gl/DipH9w9wjGMSUBUu6',
                   'Chetak Samadhi Haldighati': 'https://maps.app.goo.gl/bYZGVmM7JAkWC7Pu5',
                   'Bhartiya Lok Kala MandalBhartiya Lok Kala Mandal': 'https://maps.app.goo.gl/mCUfYTsHrhd28Zsa9'
               },
               'hotels': {
                   'Hotel The Archi': 'https://maps.app.goo.gl/1YDvkTG6BVjQwLC89',
                   'Hotel Vacation Vibes': 'https://maps.app.goo.gl/Qm8AL8DUn1PhFEne6'
                }
            },
            'Delhi': {
                'attractions': {
                    'Humayun’s Tomb': 'https://maps.app.goo.gl/DqpnQoriSSNRVKjZ8',
                    'Akshardham': 'https://maps.app.goo.gl/F3ze2X1Cf5KgK4Ek9',
                    'Purana Qila': 'https://maps.app.goo.gl/e75WhKsrqiG9EK149'
                },
                'hotels': {
                    'Hotel The Archi': 'https://maps.app.goo.gl/1YDvkTG6BVjQwLC89',
                    'Hotel Vacation Vibes': 'https://maps.app.goo.gl/Qm8AL8DUn1PhFEne6'
                }
            },
            'Jammu_Kashmir': {
                 'attractions': {
                     'Hall of Fame , Leh': 'https://maps.app.goo.gl/snS3G9NT67SoYFQk6',
                     'The Kargil War Memorial': 'https://maps.app.goo.gl/ZBrGxtjj5GZCSA5f7',
                     'Tiger Hill': 'https://maps.app.goo.gl/EBdYMkcV72saBh2o6'
                 },
                 'hotels': {
                     'Golden Metroho': 'https://maps.app.goo.gl/yuo2j1sKzv5Exqw37',
                     'The Tololing Inn': 'https://maps.app.goo.gl/xTRPYfjpU1oYJTZy6'    
                 }   
             },
            }

        self.city_label = tk.Label(self.root, text="Select City:")
        self.city_label.pack()

        self.city_var = tk.StringVar()
        self.city_dropdown = tk.OptionMenu(self.root, self.city_var, *self.places.keys())
        self.city_dropdown.pack()

        self.budget_label = tk.Label(self.root, text="Enter Budget (Rs) :")
        self.budget_label.pack()
        self.budget_entry = tk.Entry(self.root)
        self.budget_entry.pack()

        self.days_label = tk.Label(self.root, text="Enter Number of Days:")
        self.days_label.pack()
        self.days_entry = tk.Entry(self.root)
        self.days_entry.pack()

        self.submit_button = tk.Button(self.root, text="Generate Itinerary", command=self.generate_itinerary)
        self.submit_button.pack()


    def generate_itinerary(self):
        city_choice = self.city_var.get()

        if city_choice in self.places:
            attractions = self.places[city_choice]['attractions']
            hotels = self.places[city_choice]['hotels']
            budget = float(self.budget_entry.get())
            days_to_stay = int(self.days_entry.get())

            itinerary = f"City: {city_choice}\nBudget: Rs {budget}\nDays of Stay: {days_to_stay}\n\nAttractions:\n"

            text_widget = tk.Text(self.root, wrap=tk.WORD, height=30, width=50)
            text_widget.pack()

            for attraction, link in attractions.items():
                itinerary += f"{attraction}: {link}\n"
                
                text_widget.insert(tk.END, f"{attraction}: ")
                text_widget.insert(tk.END, link, ('link', link))
                text_widget.insert(tk.END, '\n')

            itinerary += "\nHotels:\n"
            for hotel, link in hotels.items():
                itinerary += f"{hotel}: {link}\n"
                
                text_widget.insert(tk.END, f"{hotel}: ")
                text_widget.insert(tk.END, link, ('link', link))
                text_widget.insert(tk.END, '\n')

            img = Image.new('RGB', (400, 500), color=(255, 255, 255))
            d = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            d.text((10, 10), itinerary, fill=(0, 0, 0), font=font)

            img.save('itinerary.jpg')

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=4,
                border=2,
            )
            qr.add_data(itinerary)
            qr.make(fit=True)

            qr_img = qr.make_image(fill_color="black", back_color="white")
            qr_img.save('itinerary_qr.png')

            tk.Label(self.root, text="Itinerary created and saved as 'itinerary.jpg' and QR code as 'itinerary_qr.png'").pack()

            text_widget.tag_configure('link', foreground='blue', underline=True)
            text_widget.tag_bind('link', '<Button-1>', self.open_link)

        else:
            tk.Label(self.root, text="City not found in our database. Please choose another city.").pack()

    def open_link(self, event):
        if event.widget.tag_ranges(tk.SEL):
            link = event.widget.get(tk.SEL_FIRST, tk.SEL_LAST)
            if link:
                os.system(f'start {link}')

root = tk.Tk()
tourist_guide = TouristGuide(root)
root.mainloop()