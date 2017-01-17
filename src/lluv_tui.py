import npyscreen
import lluv


class TitleForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.FixedText, value="Title")

    def afterEditing(self):
        self.parentApp.setNextForm('Selection')


class SelectForm(npyscreen.ActionForm):
    def create(self):
        self.add(npyscreen.TitleText, name="word")

    def afterEditing(self):
        self.parentApp.setNextForm(None)


class LluvTui(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', TitleForm, name="The CSH L.L.U.V. Machine")
        self.addForm('Selection', SelectForm, name="Select An Image and USB Device")

if __name__ == '__main__':
    lt = LluvTui().run()
