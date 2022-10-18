from kivy.config import Config
# import android

Config.set('graphics', 'width', 720)
Config.set('graphics', 'height', 1280)
Config.set('graphics', 'resizable', False)


from kivy.app import App
from kivymd.app import MDApp
from kivy.properties import StringProperty
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
import os
from data.db_session import create_session, global_init
from data.users import User

from data.connected import Connected

global_init("sql.freedb.tech:3306/freedb_users_vasyz")
session = create_session()


class Login(Screen):

    def on_focus(self, value):
        if value:
            print('User focused', self)
        else:
            print('User defocused', self)

    def do_login(self, loginText, passwordText, dsp):
        app = App.get_running_app()
        app.username = loginText
        app.password = passwordText
        users = session.query(User).filter(User.login == loginText).all()
        if users:
            print("Find user")
            user_ = users[0]
            if user_.check_password(passwordText):
                print("Correct password")
                self.manager.transition = SlideTransition(direction="left")
                self.manager.current = 'connected'
                dsp.text = ""

                app.config.read(app.get_application_config())
                app.config.write()
            else:
                dsp.text = "Неверные данные"
        else:
            dsp.text = "Неверные данные"
        # else:
        #     print("No User")
        #     dsp.text = "Неверные данные"
        #     if input("create? : ") == 'y':
        #         user_ = User()
        #         user_.login = loginText
        #         user_.name = loginText
        #         user_.set_password(passwordText)
        #         session.add(user_)
        #         session.commit()
        # user = input("Пользователь существует? : y : n : ")
        # if user == 'y':
        #     print("Find user")
        #     correct_pass = input("Пароль верный? : y : n : ")
        #     if correct_pass == 'y':
        #         print("Correct password")
        #         self.manager.transition = SlideTransition(direction="left")
        #         self.manager.current = 'connected'
        #
        #         app.config.read(app.get_application_config())
        #         app.config.write()
        #     else:
        #         dsp.text = "Неверные данные"
        # else:
        #     print("No User")
        #     dsp.text = "Неверные данные"
        #     if input("create? : ") == 'y':
        #         print("create user")
                # user_ = User()
                # user_.login = loginText
                # user_.name = loginText
                # user_.set_password(passwordText)
                # session.add(user_)
                # session.commit()

    def resetForm(self):
        self.ids['login'].text = ""
        self.ids['password'].text = ""




class LoginApp(App):
    username = StringProperty(None)
    password = StringProperty(None)

    def build(self):
        manager = ScreenManager()

        manager.add_widget(Login(name='login'))
        manager.add_widget(Connected(name='connected'))

        return manager

    def get_application_config(self):
        if (not self.username):
            return super(LoginApp, self).get_application_config()

        conf_directory = self.user_data_dir + '/' + self.username

        if (not os.path.exists(conf_directory)):
            os.makedirs(conf_directory)

        return super(LoginApp, self).get_application_config(
            '%s/config.cfg' % (conf_directory)
        )

if __name__ == '__main__':
    LoginApp().run()
