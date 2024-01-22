import datetime
import json
import random
from kivy.clock import Clock
from kivy.logger import Logger
from kivy.lang import Builder
import plyer
import os
from kivy.properties import partial
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
from gtts import gTTS
from kivy.core.audio import SoundLoader
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.effects.fadingedge import FadingEdgeEffect
from kivymd.uix.boxlayout import MDBoxLayout
from discord_webhook import DiscordWebhook, DiscordEmbed
import socket
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelThreeLine
from kivymd.uix.label import MDLabel
from kivymd.uix.pickers import MDColorPicker
from typing import Union
from kivymd.uix.list import OneLineAvatarIconListItem
from plyer import vibrator
import threading
from kivy.core.window import Window
from kivymd.uix.scrollview import MDScrollView
class AutoDismissPopup:
    pass

class MyPopup2:
    pass
class MyPopup1:
    pass

class MyDialogg:
    pass


class MainWidget(MDBoxLayout):
    def __init__(self, **kwargs):
        super(MainWidget, self).__init__(**kwargs)
        self.client_socket = None
        self.elevation = 1
        self.dialog = None
        self.primary_color1 = self.load_color(12)
        self.primary_color2 = self.load_color(13)
        self.count = 0
        self.selected_color = [1, 0, 0, 1]
    def battery(self, *args):
        try:
            battery = plyer.battery()
            percentage = battery.percent
            power_plugged = battery.power_plugged
            self.ids.progress.value = percentage
            if power_plugged:
                print('is charging')
                if 10 <= percentage <= 20:
                    icon_name = "battery-charging-10"
                elif 20 < percentage <= 30:
                    icon_name = "battery-charging-20"
                elif 30 < percentage <= 40:
                    icon_name = "battery-charging-30"
                elif 40 < percentage <= 50:
                    icon_name = "battery-charging-40"
                elif 50 < percentage <= 60:
                    icon_name = "battery-charging-50"
                elif 60 < percentage <= 70:
                    icon_name = "battery-charging-60"
                elif 70 < percentage <= 80:
                    icon_name = "battery-charging-70"
                elif 80 < percentage <= 90:
                    icon_name = "battery-charging-80"
                elif 90 < percentage < 100:
                    icon_name = "battery-charging-90"
                elif percentage == 100:
                    icon_name = 'battery-charging'
            else:
                print('not charging')
                if 10 <= percentage <= 20:
                    icon_name = "battery-10"
                elif 20 < percentage <= 30:
                    icon_name = "battery-20"
                elif 30 < percentage <= 40:
                    icon_name = "battery-30"
                elif 40 < percentage <= 50:
                    icon_name = "battery-40"
                elif 50 < percentage <= 60:
                    icon_name = "battery-50"
                elif 60 < percentage <= 70:
                    icon_name = "battery-60"
                elif 70 < percentage <= 80:
                    icon_name = "battery-70"
                elif 80 < percentage <= 90:
                    icon_name = "battery-80"
                elif 90 < percentage < 100:
                    icon_name = "battery-90"
                elif percentage == 100:
                    icon_name = 'battery'

            self.ids.battery_icon.icon = icon_name


        except Exception as e:
            print(f"Fout bij het ophalen van de batterijstatus: {str(e)}")
            self.foutmelding_widget(f'Batterij kon niet worden geüpdatet: {e}', 2)


    def check_password(self):
        if self.ids.text_field.text == "stekeltje":
            self.ids.main_screenmanager.current = 'dev_mainscreen'
        else:
            pass

    def random_text(self):
        random_sentences = [
            "zie hier wat er gebeurd!",
            "welkom!",
            "hey!",
            "heb jij hem al getest?",
            'kijk een keer naar de instructies!',
            'heb jij je telefoon al gevibreerd;)',
            'stuur ons een bericht met tips!',
            'laat de text voorlezen!\nklik er op!',
            'heb jij al de hele app ontdekt?',
            'zie de status van je opdracht',
            'probeer eens een ander kleurtje!'
        ]

        # Kies een willekeurige zin bij het opstarten
        chosen_sentence = random.choice(random_sentences)

        # Druk de gekozen zin af
        self.ids.confirm1.text = chosen_sentence
    def send_message(self):
        try:
            ip = '' + self.ids.ipText.text + ''
            port = int(self.ids.portText.text)

            if not self.client_socket:
                # Create a UDP socket
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Create a dictionary with the jsondata
            data_dict = self.ids.message_to_server.text

            # Convert the dictionary to a JSON-encoded string
            data_str = json.dumps(data_dict)

            # Send the JSON-encoded string to the server
            self.client_socket.sendto(data_str.encode(), (ip, port))

            print(f'Sent message to server: {data_dict}')
            self.ids.dev_use.text = 'Bericht verzonden!'

            # Wacht op een bevestigingsbericht van de server
            confirmation_data, server_address = self.client_socket.recvfrom(1024)
            confirmation_message = confirmation_data.decode()
            self.ids.dev_use.text = (f'{confirmation_message}')

        except Exception as e:
            print(f'Error sending/receiving message to/from the server: {e}')
            self.ids.dev_use.text = f'Error sending/receiving message: {e}'

    def remove_text(self):
        self.ids.message_to_server.text = ''
        self.ids.dev_use.text = 'waar is de text?!'

    button_select_list = []

    text = ''

    def on_checkbox_active(self, checkbox, label_text):
        if checkbox.active:
            print(label_text)
            self.text2 = label_text
            if label_text == '':
                self.ids.check2.active = False  # Stel active in op False in plaats van on_active
                del self.text2
            else:
                pass

    def show_dialog(self):
        dialog = MyDialogg()
        dialog.open()
    def open_download(self):
        self.save_data()
        dialog = MDDialog(
            title="alle aanpassingen zijn opgeslagen!",
            text="klik om te sluiten",
            radius=[50, 5, 50, 5],
            buttons=[
                MDFlatButton(
                    text="sluit popup",
                    on_release=lambda x: self.dismiss_dialog(dialog)
                )
            ]
        )
        dialog.open()
    def open_taal(self):
        dialog = MDDialog(
            shadow_color='black',
            title="hey, change the language of the app!",
            text="choose:",
            radius=[20, 7, 20, 7],
            buttons=[
                MDFlatButton(
                    text="nederlands"
                ),
                MDFlatButton(
                    text="English"
                ),
                MDFlatButton(
                    text="deutch"
                )
            ]
        )
        dialog.open()
    def listen(self, client_socket):
        while True:
            confirmation_data, server_address = client_socket.recvfrom(1024)
            confirmation_message = confirmation_data.decode()
            self.ids.zie_hier.text = f'{confirmation_message}'
            self.ids.dev_use.text = f'{confirmation_message}'
            self.ids.zie_hier.font_size = 30
            plyer.notification.notify(
                title='proces',
                message=f'bericht van de wire cutter: \n{confirmation_message}.',
                app_name='wirecutter',
                timeout=10)
            try:
                vibrator.vibrate(0.5)
            except:
                pass
    def start_thread(self):
        threading.Thread(target=self.RUN).start()

    def RUN(self):
        try:
            plyer.notification.notify(
                title='opdracht verzonden!',
                message='je opdracht is verzonden!',
                app_name='wirecutter',
                timeout=10)
            datalist = [
                int(self.ids.insulation_length.text),
                int(self.ids.left_stripping_length.text),
                int(self.ids.right_stripping_length.text),
                int(self.ids.quantity.text),
                int(self.text2)
            ]
            server_ip = '' + self.ids.ipText.text + ''
            server_port = int(self.ids.portText.text)
            data_str = json.dumps(datalist)

            # Create a UDP socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

            # Send the jsondata to the server
            client_socket.sendto(data_str.encode(), (server_ip, server_port))
            self.ids.zie_hier.text = f'Je hebt verstuurd: {datalist}'
            self.ids.dev_use.text = f'Je hebt verstuurd: {datalist}'
            try:
                vibrator.vibrate(0.5)
            except:
                pass
            threading.Thread(target=self.listen(client_socket)).start()

        except Exception as e:
            self.ids.main_screenmanager.current = 'wirescreen'
            error_message = str(e)
            print(error_message)
            try:
                vibrator.vibrate(5)
            except:
                pass
            try:
                if error_message == "'MainWidget' object has no attribute 'text2'":
                    self.ids.zie_hier.text = 'de opdracht word NIET uitgevoerd\nvul de dikte van de draad in'
                    self.ids.dev_use.text = 'de opdracht word NIET uitgevoerd\nvul de dikte van de draad in'
                    self.ids.zie_hier.font_size = 34
                    self.foutmelding_widget('de opdracht word NIET uitgevoerd vul de dikte van de draad in', 0)

                elif "[Errno 11001] getaddrinfo failed" in error_message:
                    self.ids.zie_hier.text = 'vul het juiste\nip en port in!'
                    self.ids.dev_use.text = 'de opdracht word NIET uitgevoerd\nvul alles in!'
                    self.foutmelding_widget('de opdracht word NIET uitgevoerd vul alles in!', 0)
                    self.ids.zie_hier.font_size = 34
                else:
                    self.ids.zie_hier.text = f'er is het volgende fout gegaan: {error_message}'
                    self.ids.dev_use.text = f'er is het volgende fout gegaan: {error_message}'
                    self.foutmelding_widget(f'er is het volgende fout gegaan: {error_message}', 0)
                    self.ids.zie_hier.font_size = 20

            except:
                self.ids.zie_hier.text = f'er is het volgende fout gegaan: {error_message}'
                self.ids.dev_use.text = f'er is het volgende fout gegaan: {error_message}'
                self.foutmelding_widget(f'er is het volgende fout gegaan: {error_message}', 0)
                self.ids.zie_hier.font_size = 20
    def vibreer(self, hoeveel):
        try:
            time = hoeveel
            vibrator.vibrate(time)
        except:
            pass
    def vibratie(self):
        try:
            print(f'er word {self.ids.vib_slider.value}sec gevribreerd!')
            vibrator.vibrate(self.ids.vib_slider.value)
        except Exception as e:
            self.foutmelding_widget(f'vibratie werkt niet op je telefoon foutmelding:{e}', 0)

    def change_button_color1(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color2(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color3(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color4(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color5(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color6(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color7(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color8(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color9(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color10(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color11(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)
    def change_button_color12(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)

    def change_button_color13(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)

    def change_button_color14(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)

    def change_button_color15(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)

    def change_button_color16(self, button, source_layout, target_layout):
        if button.md_bg_color == [0/255, 150/255, 0/255, 1]:
            button.md_bg_color = [40 / 255, 148 / 255, 244 / 255]
            target_layout.remove_widget(button)
            source_layout.add_widget(button)
        else:
            button.md_bg_color = [0/255, 150/255, 0/255, 1]
            source_layout.remove_widget(button)
            target_layout.add_widget(button)





    def print_id(self, button):

        if button not in self.button_select_list:
            self.button_select_list.append(button)
        elif button in self.button_select_list:
            self.button_select_list.remove(button)
        print(self.button_select_list)
    def send_message_to_discord(self):
        try:
            xname = self.ids.Name.text
            xemail = self.ids.email.text
            xexplanation = self.ids.explanation.text
            message_to_discord = f"vraag vanuit de kivy.MD app: \n\nuitleg:{xexplanation}"
            print(message_to_discord)
            f = self.button_select_list
            Subjects = ""
            firstrun = True
            for i in f:
                if firstrun:
                    Subjects = f"\n# {i}"
                    firstrun = False
                else:
                    Subjects = f"{Subjects}\n# {i}"
                print(i)
            print(Subjects)
            embed = DiscordEmbed(title=f'email: {xemail}',
                                 description=f'naam: {xname}\n geselecteerde onderwerpen: {Subjects}')
            webhook = DiscordWebhook(
                url="https://discord.com/api/webhooks/1176132253160587275/6EmKPhQZU2MZSrQevvHPAVa0wHcf0uuxVlqLnUnBnC5Z3dpZ-pc0iQnfh2t_RoNwxlDG",
                content=message_to_discord,
                username=f'by:{xname}')
            webhook.add_embed(embed)

            response = webhook.execute()
            self.ids.main_screenmanager.current = 'sended_screen'
        except Exception as e:
            self.foutmelding_widget(f'je bericht is niet veronden foutmelding: {e}', 0)
    def speak(self, text):
        try:
            if self.ids.switchs.active:
                tts = gTTS(text=text, lang='nl')
                audio_file_path = 'output.mp3'
                tts.save(audio_file_path)
                sound = SoundLoader.load(audio_file_path)
                if sound:
                    sound.play()
                    try:
                        os.remove(audio_file_path)
                        print(f"{audio_file_path} is verwijderd.")
                    except:
                        pass
        except Exception as e:
            print(f"Fout bij het afspelen van tekst-naar-spraak: {str(e)}")
            self.foutmelding_widget(f'het afspelen van geluid mislukt foutmelding: {e}', 0)
    def speaksettings(self, text):
        try:
            tts = gTTS(text=text, lang='nl')
            audio_file_path = 'output.mp3'
            tts.save(audio_file_path)
            sound = SoundLoader.load(audio_file_path)
            if sound:
                sound.play()
                try:
                    os.remove(audio_file_path)
                    print(f"{audio_file_path} is verwijderd.")
                except:
                    pass
        except Exception as e:
            print(f"Fout bij het afspelen van tekst-naar-spraak: {str(e)}")
            self.foutmelding_widget(f'het afspelen van geluid mislukt foutmelding: {e}', 0)
    def show_popup1(self):
        popup = MyPopup1()
        popup.open()
    def show_popup2(self):
        popup = MyPopup2()
        popup.open()

    def open_website(self, instance=None):
        print('bezig..')
        website_url = "https://sites.google.com/view/alaproject/homepage?authuser=0"  # Vervang dit met de URL van de gewenste website
        try:
            if platform == 'android':
                from jnius import autoclass
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                Uri = autoclass('android.net.Uri')

                intent = Intent(Intent.ACTION_VIEW, Uri.parse(website_url))
                PythonActivity.mActivity.startActivity(intent)

            elif platform == 'ios':
                import webbrowser
                webbrowser.open(website_url)

            else:
                Logger.warning("Unsupported platform for opening website.")
                try:
                    import webbrowser
                    webbrowser.open(website_url)
                except:
                    pass

        except Exception as e:
            Logger.error(f"Error opening website: {e}")
            self.foutmelding_widget(f'kan website niet openen foutmelding: {e}', 0)

    def remove_color_from_json(self, button_instance=None):
        try:
            with open('jsondata/color_data.json', 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    # Als het bestand leeg is, gebruik een leeg dictonary.
                    data = {}
        except FileNotFoundError:
            data = {}

        # Verwijder de kleurinformatie als deze bestaat
        for i in range(1, 14):
            color_key = f'color{i}'
            if color_key in data:
                del data[color_key]

        with open('jsondata/color_data.json', 'w') as json_file:
            json.dump(data, json_file)

        print("Alle kleuren verwijderd")

        # Code van reload_all_colors
        for i in range(1, 14):
            color_key = f'color{i}'
            if color_key in data:
                getattr(self, f"load_color")(i)
            else:
                # Als de kleur niet in de JSON staat, laad de standaardkleur in
                getattr(self, f"load_color")(i)
        print("Alle kleuren geupdate")
        for i in range(1, 14):
            color_r_key = f'color{i}'
            if color_r_key in data:
                getattr(self, f"reload_color{i}")()
            else:
                # Als de kleur niet in de JSON staat, laad de standaardkleur in
                getattr(self, f"reload_color{i}")()
    def reload_color1(self):
        self.ids.homescreentop.md_bg_color = self.load_color(1)
        self.ids.ga_errormailtop.md_bg_color = self.load_color(1)
        self.ids.instructionstop.md_bg_color = self.load_color(1)
        self.ids.creditstop.md_bg_color = self.load_color(1)
        self.ids.passtop.md_bg_color = self.load_color(1)
        self.ids.sendscreentop.md_bg_color = self.load_color(1)
        self.ids.ontwikkelaartop.md_bg_color = self.load_color(1)
        self.ids.errormailtop.md_bg_color = self.load_color(1)
        self.ids.vibreertop.md_bg_color = self.load_color(1)
        self.ids.batterijtop.md_bg_color = self.load_color(1)
        self.ids.assistenttop.md_bg_color = self.load_color(1)
        self.ids.foutcodetop.md_bg_color = self.load_color(1)
    def reload_color2(self):
        self.ids.homescreenbottom.md_bg_color = self.load_color(2)
        self.ids.ga_errormailbottom.md_bg_color = self.load_color(2)
        self.ids.instructionsbottom.md_bg_color = self.load_color(2)
        self.ids.instructionsbottom.md_bg_color = self.load_color(2)
        self.ids.passbottom.md_bg_color = self.load_color(2)
        self.ids.sendscreenbottom.md_bg_color = self.load_color(2)
        self.ids.ontwikkelaarbottom.md_bg_color = self.load_color(2)
        self.ids.errormailbottom.md_bg_color = self.load_color(2)
        self.ids.vibreerbottom.md_bg_color = self.load_color(2)
        self.ids.batterijbottom.md_bg_color = self.load_color(2)
        self.ids.assistentbottom.md_bg_color = self.load_color(2)
        self.ids.foutcodebottom.md_bg_color = self.load_color(2)
    def reload_color3(self):
        self.ids.zie_hier.color = self.load_color(3)
        self.ids.confirm1.color = self.load_color(3)
        self.ids.label_1.color = self.load_color(3)
        self.ids.label_3.color = self.load_color(3)
        self.ids.lab1.color = self.load_color(3)
        self.ids.dev_use.color = self.load_color(3)
        self.ids.uitleg_s.color = self.load_color(3)
        self.ids.battery_icon.color = self.load_color(3)
        self.ids.namelabel1.color = self.load_color(3)
        self.ids.namelabel2.color = self.load_color(3)
        self.ids.namelabel3.color = self.load_color(3)
        self.ids.namelabel4.color = self.load_color(3)
        self.ids.namelabel5.color = self.load_color(3)
        self.ids.namelabel6.color = self.load_color(3)
        self.ids.namelabel7.color = self.load_color(3)
        self.ids.namelabel8.color = self.load_color(3)
        self.ids.foutmelding.color = self.load_color(3)
        self.ids.credit_label1.color = self.load_color(3)


    def reload_color4(self):
        self.ids.wirescreen.md_bg_color = self.load_color(4)
        self.ids.go_errormail.md_bg_color = self.load_color(4)
        self.ids.instructions.md_bg_color = self.load_color(4)
        self.ids.credits.md_bg_color = self.load_color(4)
        self.ids.devpassscreen.md_bg_color = self.load_color(4)
        self.ids.sended_screen.md_bg_color = self.load_color(4)
        self.ids.dev_mainscreen.md_bg_color = self.load_color(4)
        self.ids.errormail.md_bg_color = self.load_color(4)
        self.ids.vibratie.md_bg_color = self.load_color(4)
        self.ids.battery.md_bg_color = self.load_color(4)
        self.ids.speakscreen.md_bg_color = self.load_color(4)
        self.ids.foutcode.md_bg_color = self.load_color(4)
    def reload_color5(self):
        self.ids.ipText.text_color_focus = self.load_color(5)
        self.ids.portText.text_color_focus = self.load_color(5)
        self.ids.quantity.text_color_focus = self.load_color(5)
        self.ids.insulation_length.text_color_focus = self.load_color(5)
        self.ids.right_stripping_length.text_color_focus = self.load_color(5)
        self.ids.left_stripping_length.text_color_focus = self.load_color(5)
        self.ids.dikte.text_color_focus = self.load_color(5)
        self.ids.Name.text_color_focus = self.load_color(5)
        self.ids.email.text_color_focus = self.load_color(5)
        self.ids.explanation.text_color_focus = self.load_color(5)
        self.ids.message_to_server.text_color_focus = self.load_color(5)
        self.ids.anders.text_color_focus = self.load_color(5)

    def reload_color6(self):
        self.ids.ipText.text_color_normal = self.load_color(6)
        self.ids.portText.text_color_normal = self.load_color(6)
        self.ids.quantity.text_color_normal = self.load_color(6)
        self.ids.insulation_length.text_color_normal = self.load_color(6)
        self.ids.right_stripping_length.text_color_normal = self.load_color(6)
        self.ids.left_stripping_length.text_color_normal = self.load_color(6)
        self.ids.dikte.text_color_normal = self.load_color(6)
        self.ids.Name.text_color_normal = self.load_color(6)
        self.ids.email.text_color_normal = self.load_color(6)
        self.ids.explanation.text_color_normal = self.load_color(6)
        self.ids.message_to_server.text_color_normal = self.load_color(6)
        self.ids.anders.text_color_normal = self.load_color(6)

    def reload_color7(self):
        self.ids.ipText.line_color_focus = self.load_color(7)
        self.ids.portText.line_color_focus = self.load_color(7)
        self.ids.quantity.line_color_focus = self.load_color(7)
        self.ids.insulation_length.line_color_focus = self.load_color(7)
        self.ids.right_stripping_length.line_color_focus = self.load_color(7)
        self.ids.left_stripping_length.line_color_focus = self.load_color(7)
        self.ids.dikte.line_color_focus = self.load_color(7)
        self.ids.Name.line_color_focus = self.load_color(7)
        self.ids.email.line_color_focus = self.load_color(7)
        self.ids.explanation.line_color_focus = self.load_color(7)
        self.ids.message_to_server.line_color_focus = self.load_color(7)
        self.ids.anders.line_color_focus = self.load_color(7)
    def reload_color8(self):
        self.ids.ipText.line_color_normal = self.load_color(8)
        self.ids.portText.line_color_normal = self.load_color(8)
        self.ids.quantity.line_color_normal = self.load_color(8)
        self.ids.insulation_length.line_color_normal = self.load_color(8)
        self.ids.right_stripping_length.line_color_normal = self.load_color(8)
        self.ids.left_stripping_length.line_color_normal = self.load_color(8)
        self.ids.dikte.line_color_normal = self.load_color(8)
        self.ids.Name.line_color_normal = self.load_color(8)
        self.ids.email.line_color_normal = self.load_color(8)
        self.ids.explanation.line_color_normal = self.load_color(8)
        self.ids.message_to_server.line_color_normal = self.load_color(8)
        self.ids.anders.line_color_normal = self.load_color(8)

    def reload_color9(self):
        self.ids.check1.color_active = self.load_color(9)
        self.ids.check2.color_active = self.load_color(9)
        self.ids.check3.color_active = self.load_color(9)

    def reload_color10(self):
        self.ids.homescreentop.specific_text_color = self.load_color(10)
        self.ids.ga_errormailtop.specific_text_color = self.load_color(10)
        self.ids.instructionstop.specific_text_color = self.load_color(10)
        self.ids.creditstop.specific_text_color = self.load_color(10)
        self.ids.passtop.specific_text_color = self.load_color(10)
        self.ids.sendscreentop.specific_text_color = self.load_color(10)
        self.ids.ontwikkelaartop.specific_text_color = self.load_color(10)
        self.ids.errormailtop.specific_text_color = self.load_color(10)
        self.ids.vibreertop.specific_text_color = self.load_color(10)
        self.ids.batterijtop.specific_text_color = self.load_color(10)
        self.ids.assistenttop.specific_text_color = self.load_color(10)
        self.ids.foutcodetop.specific_text_color = self.load_color(10)
        self.ids.homescreenbottom.specific_text_color = self.load_color(10)
        self.ids.ga_errormailbottom.specific_text_color = self.load_color(10)
        self.ids.instructionsbottom.specific_text_color = self.load_color(10)
        self.ids.instructionsbottom.specific_text_color = self.load_color(10)
        self.ids.passbottom.specific_text_color = self.load_color(10)
        self.ids.sendscreenbottom.specific_text_color = self.load_color(10)
        self.ids.ontwikkelaarbottom.specific_text_color = self.load_color(10)
        self.ids.errormailbottom.specific_text_color = self.load_color(10)
        self.ids.vibreerbottom.specific_text_color = self.load_color(10)
        self.ids.batterijbottom.specific_text_color = self.load_color(10)
        self.ids.assistentbottom.specific_text_color = self.load_color(10)
        self.ids.foutcodebottom.specific_text_color = self.load_color(10)

    def reload_color11(self):
        self.ids.DrawerClickable1.text_color = self.load_color(11)
        self.ids.DrawerClickable1.icon_color = self.load_color(11)
        self.ids.DrawerClickable2.text_color = self.load_color(11)
        self.ids.DrawerClickable2.icon_color = self.load_color(11)
        self.ids.DrawerClickable3.text_color = self.load_color(11)
        self.ids.DrawerClickable3.icon_color = self.load_color(11)
        self.ids.DrawerClickable4.text_color = self.load_color(11)
        self.ids.DrawerClickable4.icon_color = self.load_color(11)
        self.ids.DrawerClickable5.text_color = self.load_color(11)
        self.ids.DrawerClickable5.icon_color = self.load_color(11)
        self.ids.DrawerClickable6.text_color = self.load_color(11)
        self.ids.DrawerClickable6.icon_color = self.load_color(11)
        self.ids.DrawerClickable7.text_color = self.load_color(11)
        self.ids.DrawerClickable7.icon_color = self.load_color(11)
        self.ids.DrawerClickable8.text_color = self.load_color(11)
        self.ids.DrawerClickable8.icon_color = self.load_color(11)
        self.ids.DrawerClickable9.text_color = self.load_color(11)
        self.ids.DrawerClickable9.icon_color = self.load_color(11)
        self.ids.DrawerClickable10.text_color = self.load_color(11)
        self.ids.DrawerClickable10.icon_color = self.load_color(11)
        self.ids.progress.color = self.load_color(11)
        self.ids.battery_icon.color = self.load_color(11)

    def reload_color12(self):
        self.ids.header.text_color = self.load_color(12)
        self.ids.header.title_color = self.load_color(12)
        self.ids.DrawerLabel3.markup_text = self.load_color(12)
        self.ids.DrawerLabel3.text_color = self.load_color(12)
        self.ids.DrawerLabel3.color = self.load_color(12)
        self.ids.kloklabel.color = self.load_color(12)
        self.primary_color1 = self.load_color(12)

    def reload_color13(self):
        self.ids.nav_drawer.md_bg_color = self.load_color(13)
        self.primary_color2 = self.load_color(13)
        self.reload_dark()
        self.ids.DrawerClickable1.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable2.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable3.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable4.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable5.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable6.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable7.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable8.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable9.unfocus_color = self.load_color(13)
        self.ids.DrawerClickable10.unfocus_color = self.load_color(13)
    def reload_dark(self):
        self.load_color(13)
        if self.load_color(13) == [1, 1, 1, 1]:
            self.dark = [0.7, 0.7, 0.7, 1]
        else:
            self.dark = [x + 0.5 if i < 3 else x for i, x in enumerate(self.load_color(13))]

        self.ids.DrawerClickable1.focus_color = self.dark
        self.ids.DrawerClickable2.focus_color = self.dark
        self.ids.DrawerClickable3.focus_color = self.dark
        self.ids.DrawerClickable4.focus_color = self.dark
        self.ids.DrawerClickable5.focus_color = self.dark
        self.ids.DrawerClickable6.focus_color = self.dark
        self.ids.DrawerClickable7.focus_color = self.dark
        self.ids.DrawerClickable8.focus_color = self.dark
        self.ids.DrawerClickable9.focus_color = self.dark
        self.ids.DrawerClickable10.focus_color = self.dark

    def open_color_picker1(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color1,
            on_release=self.get_selected_color1,
            )
    def open_color_picker2(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color2,
            on_release=self.get_selected_color2,
            )
    def open_color_picker3(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color3,
            on_release=self.get_selected_color3,
            )

    def open_color_picker4(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color4,
            on_release=self.get_selected_color4,
        )
    def open_color_picker5(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color5,
            on_release=self.get_selected_color5,
            )

    def open_color_picker6(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color6,
            on_release=self.get_selected_color6,
    )
    def open_color_picker7(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color7,
            on_release=self.get_selected_color7,
    )
    def open_color_picker8(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color8,
            on_release=self.get_selected_color8,
    )
    def open_color_picker9(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color9,
            on_release=self.get_selected_color9,
    )
    def open_color_picker10(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color10,
            on_release=self.get_selected_color10,
    )

    def open_color_picker11(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color11,
            on_release=self.get_selected_color11,
        )
    def open_color_picker12(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color12,
            on_release=self.get_selected_color12,
    )
    def open_color_picker13(self, button_instance=None):
        color_picker = MDColorPicker(size_hint=(0.45, 0.85))
        color_picker.open()
        color_picker.bind(
            on_select_color=self.on_select_color13,
            on_release=self.get_selected_color13,
    )

    def get_selected_color1(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color2(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''

    def get_selected_color3(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''

    def get_selected_color4(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color5(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color6(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color7(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color8(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color9(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''

    def get_selected_color10(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color11(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color12(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''
    def get_selected_color13(
            self,
            instance_color_picker: MDColorPicker,
            type_color: str,
            selected_color: Union[list, str],
    ):
        '''Return selected color.'''


    def on_select_color1(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 1)
        self.reload_color1()

    def on_select_color2(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 2)
        self.reload_color2()
    def on_select_color3(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 3)
        self.reload_color3()
        self.selected_color = color
    def on_select_color4(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 4)
        self.reload_color4()
    def on_select_color5(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 5)
        self.reload_color5()
    def on_select_color6(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 6)
        self.reload_color6()
    def on_select_color7(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 7)
        self.reload_color7()
    def on_select_color8(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 8)
        self.reload_color8()
    def on_select_color9(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 9)
        self.reload_color9()
    def on_select_color10(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 10)
        self.reload_color10()
    def on_select_color11(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 11)
        self.reload_color11()
    def on_select_color12(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 12)
        self.reload_color12()
    def on_select_color13(self, instance_gradient_tab, color: list) -> None:
        self.save_color_to_json(color, 13)
        self.reload_color13()


    def save_color_to_json(self, color, num):
        try:
            with open('jsondata/color_data.json', 'r') as json_file:
                try:
                    data = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    # Als het bestand leeg is, gebruik een leeg dictonary.
                    data = {}
        except FileNotFoundError:
            data = {}

        data[f'color{num}'] = color

        with open('jsondata/color_data.json', 'w') as json_file:
            json.dump(data, json_file)

        print(f"Color 1 saved: {color}")
    def load_color(self, num):
        if num == 1:
            ret = [0.20, 0.20, 0.20, 1]
        if num == 2:
            ret = [40 / 255, 148 / 255, 244 / 255, 255 / 255]
        if num == 3:
            ret = [0, 0, 0, 255 / 255]
        if num == 4:
            ret = [1, 1, 1, 1]
        if num == 5:
            ret = [40/255, 70/255, 230/255, 1]
        if num == 6:
            ret = [40/255, 70/255, 230/255, 1]
        if num == 7:
            ret = [40 / 255, 148 / 255, 244 / 255, 255 / 255]
        if num == 8:
            ret = [40 / 255, 148 / 255, 244 / 255, 255 / 255]
        if num == 9:
            ret = [0/255, 220/255, 0/255, 1]
        if num == 10:
            ret = [1, 1, 1, 1]
        if num == 11:
            ret = [0, 0, 0, 1]
        if num == 12:
            ret = [0, 0, 0, 1]
        if num == 13:
            ret = [1, 1, 1, 1]


        try:
            with open('jsondata/color_data.json', 'r') as json_file:
                data = json.load(json_file)
                return data.get(f'color{num}', ret)
        except FileNotFoundError:
            # Als het bestand niet wordt gevonden, retourneer een standaardwaarde.
            print(f"JSON-bestand {num} niet gevonden. Gebruik standaardkleur.")
            return [0.20, 0.20, 0.20, 1]
        except Exception as e:
            self.foutmelding_widget(f'fout bij het laden van kleuren foutmelding: {e}', 0)
    def update_label(self, dt):
        new_text = datetime.datetime.now().strftime('%H:%M:%S')
        self.ids.kloklabel.text = new_text

    def start(self):
        Clock.schedule_interval(self.battery, 60)
        self.battery()
        Clock.schedule_interval(self.update_label, 1)
        self.reload_color1()
        self.reload_color2()
        self.reload_color3()
        self.reload_color4()
        self.reload_color5()
        self.reload_color6()
        self.reload_color7()
        self.reload_color8()
        self.reload_color9()
        self.reload_color10()
        self.reload_color11()
        self.reload_color12()
        self.reload_color13()
        self.random_text()
        self.load_data()
        self.load_data_widget()
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon= 'assets/A.png',
                content=Content1(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='hoe stel ik de lengte van mijn draad in?',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content2(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='ik krijg een error melding?',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content3(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='de lampjes en de display staan uit?',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content4(),
                panel_cls=MDExpansionPanelThreeLine(
                    text=(f'er staat "verstuurd:" maar er gebreurd niks?'),
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content5(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='waar kan ik het ip en port zien?',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content6(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='dingen die ik moet doen voor het gebruik?',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content7(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='er is iets kapot',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content8(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='de wire cutter loopt vast',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content9(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='waarom zit er een omhuizing om de wire cutter heen?',
                    secondary_text='ALA Projecten',
                    tertiary_text='vraag',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content10(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='hoeveel lijnen aan code zijn er gebruikt voor de app?',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content11(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='hoeveel tijd heeft er in het project gezeten?',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content12(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='hoeveel condensators zijn er ontploft?',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content13(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='hoeveel tijd zit er in deze app?',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content14(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='wie hebben er mee geholpen?',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content15(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='wanneer word dit project gepresenteerd?!',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        self.ids.box.add_widget(
            MDExpansionPanel(
                opening_transition='out_circ',
                opening_time=1,
                closing_transition='in_out_cubic',
                closing_time=0.8,
                icon='assets/A.png',
                content=Content16(),
                panel_cls=MDExpansionPanelThreeLine(
                    text='is een app nodig voor een draadknipper?',
                    secondary_text='ALA Projecten',
                    tertiary_text='weetjes en feitjes',
                )
            )
        )
        try:
            with open('jsondata/app_data.json', 'r') as file:
                data = json.load(file)
                self.ids.ipText.text = data.get('ip_address')
                self.ids.portText.text = data.get('port_number')
        except FileNotFoundError as e:
            self.foutmelding_widget(f'Fout bij laden van ip en port text foutmelding: {e}', 0)
        except KeyError as e:
            self.foutmelding_widget(f'KeyError bij laden van ip en port text foutmelding: {e}', 0)

    def show_confirmation_dialog(self):
        if not self.dialog:
            box = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
            box.bind(minimum_height=box.setter('height'))
            button_info = [
                {"text": "toptoolbar color", "on_release": self.open_color_picker1},
                {"text": "bottomtoolbar color", "on_release": self.open_color_picker2},
                {"text": "text color", "on_release": self.open_color_picker3},
                {"text": "background color", "on_release": self.open_color_picker4},
                {"text": "textfielt text color focus", "on_release": self.open_color_picker5},
                {"text": "textfielt text color normal", "on_release": self.open_color_picker6},
                {"text": "textflielt line color focus", "on_release": self.open_color_picker7},
                {"text": "textflielt line color normal", "on_release": self.open_color_picker8},
                {"text": "checkbox color", "on_release": self.open_color_picker9},
                {"text": "toolbar widget color", "on_release": self.open_color_picker10},
                {"text": "menu button color", "on_release": self.open_color_picker11},
                {"text": "menu label color", "on_release": self.open_color_picker12},
                {"text": "menu background color", "on_release": self.open_color_picker13},
                {"text": "reset colors", "on_release": self.remove_color_from_json},
            ]

            for info in button_info:
                button = ExampleButton(
                    text=info["text"],
                    size_hint_y=None,
                    height=30,
                    width=200  # Adjust the width as needed
                )
                button.bind(on_release=info["on_release"])
                box.add_widget(button)

            scroll_view = MDScrollView(size_hint=(None, None), size=(400, 200))
            scroll_view.add_widget(box)

            self.dialog = MDDialog(
                title="color picker",
                type="custom",
                content_cls=scroll_view,
                buttons=[
                    MDRaisedButton(
                        text="OK",
                        on_release=self.dismiss_dialog
                    ),
                ],
            )
        self.dialog.open()

    def dismiss_dialog(self, instance):
        self.dialog.dismiss()

    def save_data(self):
        ip_address = self.ids.ipText.text.strip()
        port_number = self.ids.portText.text.strip()
        if ip_address or port_number:
            data = {'ip_address': ip_address, 'port_number': port_number}
            with open('jsondata/app_data.json', 'w') as file:
                json.dump(data, file)
            print(f"IP-adres opgeslagen: {ip_address}")
            print(f"Poortnummer opgeslagen: {port_number}")

    def load_data(self):
        try:
            with open('jsondata/app_data.json', 'r') as file:
                data_list = json.load(file)

            if isinstance(data_list, list) and len(data_list) > 0:
                # Als het een lijst is, selecteer het eerste element (een dictionary) uit de lijst
                data = data_list[0]
            else:
                data = {}

            ip_address = data.get('ip_address', '')
            port_number = data.get('port_number', '')

            # Update de waarden van de widgets
            self.ids.ipText.text = ip_address
            self.ids.portText.text = port_number

            print(f"IP-adres geladen: {ip_address}")
            print(f"Poortnummer geladen: {port_number}")

        except FileNotFoundError:
            print("Geen opgeslagen gegevens gevonden.")

    def foutmelding_widget(self, text, time):
        vp_height = self.ids.scroll.viewport_size[1]
        sv_height = self.ids.scroll.height

        # add a new widget (must have preset height)
        if time == 0:
            clock = datetime.datetime.now().strftime('%H:%M:%S')
            daytime = datetime.datetime.now().strftime('%D')
            time = f'datum:{daytime}\ntijd:{clock}'
            self.save_data_widget(text, time)
        if time == 2:
            clock = datetime.datetime.now().strftime('%H:%M:%S')
            daytime = datetime.datetime.now().strftime('%D')
            time = f'datum:{daytime}\ntijd:{clock}'
        else:
            time = time

        time_label = MDLabel(
            text=f'{time}',
            size_hint=(1, None),
            height=30,
            font_style='H6',
            halign='left',
            valign='center',
            padding=(30, 0),
            id='time_label',
            text_color=self.selected_color
        )

        label = MDLabel(
            text=f'foutmelding:{text}',
            size_hint=(1, None),
            height=300,
            font_style='H5',
            halign='left',
            valign='center',
            padding=(50, 0),
            id='fout_label',
            color= (1, 0, 0, 1)
        )

        self.ids.box1.add_widget(time_label)
        self.ids.box1.add_widget(label)
        self.count += 1

        if vp_height > sv_height:  # otherwise there is no scrolling
            # calculate y value of bottom of scrollview in the viewport
            scroll = self.ids.scroll.scroll_y
            bottom = scroll * (vp_height - sv_height)

            # use Clock.schedule_once because we need updated viewport height
            # this assumes that new widgets are added at the bottom
            # so the current bottom must increase by the widget height to maintain position
            Clock.schedule_once(partial(self.adjust_scroll, bottom + label.height), -1)

    def adjust_scroll(self, bottom, dt):
        vp_height = self.ids.scroll.viewport_size[1]
        sv_height = self.ids.scroll.height
        self.ids.scroll.scroll_y = bottom / (vp_height - sv_height)

    def save_data_widget(self, text, time):
        try:
            with open('jsondata/widget_data.json', 'r') as file:
                data = json.load(file)
                if not isinstance(data, list):
                    raise ValueError("Ongeldige structuur in JSON-bestand")
        except (FileNotFoundError, json.JSONDecodeError, ValueError):
            data = {}

        data.append({'text': text, 'time': time})

        with open('jsondata/widget_data.json', 'w') as file:
            json.dump(data, file)

        print(f"text opgeslagen: {text}")
        print(f"time opgeslagen: {time}")

    def load_data_widget(self):
        try:
            with open('jsondata/widget_data.json', 'r') as file:
                data = json.loads(file.read())

            if not isinstance(data, list):
                raise ValueError("Ongeldige structuur in JSON-bestand")

            for entry in data:
                text = entry.get('text', '')
                time = entry.get('time', '')
                self.foutmelding_widget(text, time)
                print(f"time geladen: {time}")
                print(f"text geladen: {text}")

        except (FileNotFoundError, json.JSONDecodeError, ValueError) as e:
            print(f"Fout bij laden gegevens: {e}")
            print("Geen opgeslagen gegevens gevonden.")
    def clear_data_widget(self):
        try:
            with open('jsondata/widget_data.json', 'w') as file:
                file.write('{}')  # Schrijf een lege lijst terug naar het bestand
            print("Alle gegevens zijn verwijderd.")
        except Exception as e:
            print(f"Fout bij het verwijderen van gegevens: {e}")
        self.load_data_widget()
        self.ids.box1.clear_widgets()

class Content1(MDBoxLayout):
    '''Custom content.'''
class Content2(MDBoxLayout):
    pass
class Content3(MDBoxLayout):
    pass
class Content4(MDBoxLayout):
    pass
class Content5(MDBoxLayout):
    pass
class Content6(MDBoxLayout):
    pass
class Content7(MDBoxLayout):
    pass
class Content8(MDBoxLayout):
    pass
class Content9(MDBoxLayout):
    pass
class Content10(MDBoxLayout):
    pass
class Content11(MDBoxLayout):
    pass
class Content12(MDBoxLayout):
    pass
class Content13(MDBoxLayout):
    pass
class Content14(MDBoxLayout):
    pass
class Content15(MDBoxLayout):
    pass
class Content16(MDBoxLayout):
    pass
class ExampleButton(MDRaisedButton):
    pass
class Item(OneLineAvatarIconListItem):
    divider = None
class FadeScrollView(FadingEdgeEffect, ScrollView):
    pass
    def on_button_click(self):
        print(f"Button clicked: {self.text}")

class MyApp(MDApp):
    dialog = None
    theme_style = 'Dark'
    def build(self):
        Window.size = (500, 640)
        self.count = 0
        return


    def on_button_click_1(self, instance):
        print(f"Button 1 clicked")

    def on_button_click_2(self, instance):
        print(f"Button 2 clicked")

    def dismiss_dialog(self, *args):
        self.dialog.dismiss()

    def on_start(self):
        self.root.start()
    def popup_callback(self, instance_button):
        selected_option = instance_button.text
        print(f"Gekozen optie uit de popup: {selected_option}")

if __name__ == "__main__":
    MyApp().run()