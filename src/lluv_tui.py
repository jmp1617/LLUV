import npyscreen
import lluv


class CatagorySel(npyscreen.MultiLineAction):
    def __init__(self, *args, **keywords):
        super(CatagorySel, self).__init__(*args, **keywords)

    def actionHighlighted(self, act_on_this, key_press):
        pass

    def display_value(self, vl):
        return vl.get_name()

class ImageSelectionBox(npyscreen.BoxTitle):
    _contained_widget = CatagorySel


class BSSlider(npyscreen.Slider):
    def __init__(self, *args, **keywords):
        super(BSSlider, self).__init__(*args, **keywords)
        self.out_of = 17  # 18 dif bs

    def translate_value(self):
        block_sizes = ["512b", "1K",  "2K",  "4k",  "8K",  "16K",  "32K", "64K",  "128K",  "256K", "512K",  "1M",  "2M",
                       "4M",  "8M",  "16M",  "32M", "64M"]
        selval = int(round(self.value))
        return block_sizes[selval]


class SliderBox(npyscreen.BoxTitle):
    _contained_widget = BSSlider


class CheckBoxBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne


class TextItem(npyscreen.FixedText):
    def __init__(self, *args, **keywords):
        super(TextItem, self).__init__(*args, **keywords)
        self.editable = False


class NewBox(npyscreen.BoxTitle):
    _contained_widget = TextItem


class ProgressBar(npyscreen.SliderPercent):
    def __init__(self, *args, **keywords):
        super(ProgressBar, self).__init__(*args, **keywords)
        self.editable = False
        self.accuracy = 0


class ProgressBarBox(npyscreen.BoxTitle):
    _contained_widget = ProgressBar


class NewTheme(npyscreen.ThemeManager):

    def __init__(self):
        super().__init__()

    default_colors = {
        'DEFAULT': 'WHITE_BLACK',
        'FORMDEFAULT': 'WHITE_BLACK',
        'NO_EDIT': 'BLUE_BLACK',
        'STANDOUT': 'CYAN_BLACK',
        'CURSOR': 'WHITE_BLACK',
        'CURSOR_INVERSE': 'BLACK_WHITE',
        'LABEL': 'GREEN_BLACK',
        'LABELBOLD': 'WHITE_BLACK',
        'CONTROL': 'YELLOW_BLACK',
        'IMPORTANT': 'GREEN_BLACK',
        'SAFE': 'GREEN_BLACK',
        'WARNING': 'MAGENTA_BLACK',
        'DANGER': 'RED_BLACK',
        'CRITICAL': 'BLACK_RED',
        'GOOD': 'GREEN_BLACK',
        'GOODHL': 'GREEN_BLACK',
        'VERYGOOD': 'BLACK_GREEN',
        'CAUTION': 'YELLOW_BLACK',
        'CAUTIONHL': 'BLACK_YELLOW',
    }


class TitleForm(npyscreen.Form):
    def create(self):

        l_space = 12

        the1 = " "*5+"╔╦╗┬ ┬┌─┐"
        the2 = " "*5+" ║ ├─┤├┤ "
        the3 = " "*5+" ╩ ┴ ┴└─┘"

        mac1 = " "*75+"╔╦╗┌─┐┌─┐┬ ┬┬┌┐┌┌─┐"
        mac2 = " "*75+"║║║├─┤│  ├─┤││││├┤ "
        mac3 = " "*75+"╩ ╩┴ ┴└─┘┴ ┴┴┘└┘└─┘"

        title_block1 = " "*l_space+"          ,gggg,          ,gggg,    ,ggg,         gg  ,ggg,         ,gg "
        title_block2 = " "*l_space+"         d8\" \"8I         d8\"  \"8I  dP\"\"Y8a        88 dP\"\"Y8a       ,8P "
        title_block3 = " "*l_space+"         88  ,dP         88  ,dP   Yb, `88        88 Yb, `88       d8' "
        title_block4 = " "*l_space+"      8888888P\"       8888888P\"     `\"  88        88  `\"  88       88  "
        title_block5 = " "*l_space+"          88              88            88        88      88       88      "
        title_block6 = " "*l_space+"          88              88            88        88      I8       8I "
        title_block7 = " "*l_space+"     ,aa,_88         ,aa,_88            88        88      `8,     ,8'  "
        title_block8 = " "*l_space+"    dP\" \"88P        dP\" \"88P            88        88       Y8,   ,8P   "
        title_block9 = " "*l_space+"    Yb,_,d88b,,_    Yb,_,d88b,,_        Y8b,____,d88,       Yb,_,dP     "
        title_block10 = " "*l_space+"     \"Y8P\"  \"Y88888  \"Y8P\"  \"Y88888      \"Y888888P\"Y8        \"Y8P\"      "
        box = self.add(npyscreen.BoxTitle,
                       name="Welcome To",
                       max_width=105,
                       relx=20,
                       max_height=36,
                       rely=5,
                       contained_widget_arguments={
                           'color': "WARNING",
                           'widgets_inherit_color': True, }
                       )

        box.footer = "by: Jacob Potter (jpotter)"
        box.values = ["", "", the1, the2, the3, "", "", "", "", "", "", title_block1, title_block2, title_block3,
                      title_block4, title_block5, title_block6, title_block7, title_block8, title_block9,
                      title_block10, "", " "*l_space*3+"( Linux Live USB Vending )", "", "", "", "", "", "", mac1,
                      mac2, mac3]
        box.editable = False

    def afterEditing(self):
        self.parentApp.setNextForm('Selection')


class SelectForm(npyscreen.ActionForm):
    def create(self):
        self.add(ImageSelectionBox,
                 name="Select an Category:",
                 max_width=60,
                 relx=3,
                 rely=2,
                 max_height=39,
                 values=self.parentApp.img_categories)
        self.add(npyscreen.BoxBasic,
                 name="Select a USB Device:",
                 max_width=40,
                 max_height=39,
                 relx=65,
                 rely=2)
        self.pbar = self.add(ProgressBarBox,
                             max_height=3,
                             max_width=115,
                             out_of=100,
                             value=0,
                             name="Write Progress:",
                             relx=3, rely=42)
        self.written = self.add(NewBox,
                                name="Written:",
                                max_width=20,
                                rely=42, relx=120,
                                max_height=3,
                                value="3000 / 3077 MB")
        self.selected_usb_box = self.add(NewBox,
                                         name="Selected USB Device:",
                                         max_width=33,
                                         max_height=4,
                                         relx=107,
                                         rely=2,
                                         value="Not Selected")
        self.selected_img_box = self.add(NewBox,
                                         name="Selected Image:",
                                         max_width=33,
                                         max_height=4,
                                         relx=107,
                                         rely=7,
                                         value="Not Selected")
        self.block_check = self.add(CheckBoxBox,
                                    name="Block Size Options:",
                                    max_width=33,
                                    max_height=6,
                                    relx=107,
                                    rely=12,
                                    value=[0, ],
                                    values=["Use Default (512K)", "Auto Detect ( -- )", "Use BS Slider"])
        self.bs_slide = self.add(SliderBox,
                                 name="BS Selector:",
                                 max_width=33,
                                 max_height=3,
                                 relx=107,
                                 rely=19)

        self.para = self.add(npyscreen.BoxTitle,
                             name="How To:",
                             max_width=33,
                             max_height=18,
                             relx=107,
                             rely=23,
                             contained_widget_arguments={
                                 'color': "WARNING",
                                 'widgets_inherit_color': True, }
                             )
        self.para.values = ["", " STEP 1:", "   │Select an Image Category.", "   │Select an Image.", "", " STEP 2:",
                            "   │Select an USB Device", "", " STEP 3:", "   │Configure Block Size", "   │(optional)",
                            "", " STEP 4:", "   │Select the Yellow OK", "   │Profit $$"]
        self.para.editable = False

        self.bs_slide.editable = self.parentApp.activate_bs_slider

    def on_ok(self):
        self.parentApp.switchForm('MAIN')

    def on_cancel(self):
        self.parentApp.switchForm('MAIN')


class LluvTui(npyscreen.NPSAppManaged):
    # DAT
    img_categories = lluv.fetch_images(lluv.get_path())
    master_list = lluv.generate_image_master(img_categories)
    usb_devices = lluv.fetch_usb()
    # SEL
    selected_image = None
    selected_usb = None
    selfselected_block = "512K"  # Default BS
    # FLA
    activate_bs_slider = True

    def onStart(self):
        # Form init
        npyscreen.setTheme(NewTheme)
        self.addForm('MAIN', TitleForm, name="The CSH L.L.U.V. Machine - Page (1/2)", )
        self.addForm('Selection', SelectForm, name="Select An Image and USB Device - Page (2/2)")
        #

    def reset_values(self):
        img_categories = lluv.fetch_images(lluv.get_path())
        master_list = lluv.generate_image_master(img_categories)
        usb_devices = lluv.fetch_usb()
        # SEL
        selected_image = None
        selected_usb = None
        selected_block = "512K"  # Default BS
        # FLA
        activate_bs_slider = True


if __name__ == '__main__':
    lt = LluvTui().run()