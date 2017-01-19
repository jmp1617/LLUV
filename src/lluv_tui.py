import npyscreen
import lluv
import threading
from time import sleep
import multiprocessing


class ImgSel(npyscreen.MultiLine):
    def __init__(self, *args, **keywords):
        super(ImgSel, self).__init__(*args, **keywords)

    def display_value(self, vl):
        if type(vl) is str:
            return vl
        else:
            return vl.get_name()


class USBSel(npyscreen.MultiLine):
    def __init__(self, *args, **keywords):
        super(USBSel, self).__init__(*args, **keywords)

    def display_value(self, vl):
        return vl.get_name()+" - "+str(vl.get_size()/1000000000).split(".")[0]+" GB"


class CatagorySel(npyscreen.MultiLine):
    def __init__(self, *args, **keywords):
        super(CatagorySel, self).__init__(*args, **keywords)

    def display_value(self, vl):
        return vl.get_name()


class ImgSelectionBox(npyscreen.BoxTitle):
    _contained_widget = ImgSel


class UsbSelectionBox(npyscreen.BoxTitle):
    _contained_widget = USBSel


class CatSelectionBox(npyscreen.BoxTitle):
    _contained_widget = CatagorySel


class BSSlider(npyscreen.Slider):
    def __init__(self, *args, **keywords):
        super(BSSlider, self).__init__(*args, **keywords)
        self.out_of = 17  # 18 dif bs
        self.color = 'NO_EDIT'

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
        self.color = 'NO_EDIT'


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

        self.keypress_timeout = 10

        self.cat = self.add(CatSelectionBox,
                            name="Select an Category:",
                            max_width=30,
                            relx=3,
                            rely=2,
                            max_height=39,
                            values=self.parentApp.img_categories)

        self.usb = self.add(UsbSelectionBox,
                            name="Select a USB Device:",
                            max_width=40,
                            max_height=12,
                            relx=35,
                            rely=2,
                            values=self.parentApp.usb_list)

        self.img = self.add(ImgSelectionBox,
                            name="Select an Image",
                            max_width=70,
                            max_height=26,
                            relx=35,
                            rely=15)

        self.pbar = self.add(ProgressBarBox,
                             max_height=3,
                             max_width=115,
                             out_of=100,
                             name="Write Progress:",
                             relx=3, rely=42)

        self.written = self.add(NewBox,
                                name="Written:",
                                max_width=20,
                                rely=42, relx=120,
                                max_height=3,
                                value="0 / 0 MB")

        self.selected_usb_box = self.add(NewBox,
                                         name="Selected USB Device:",
                                         max_width=33,
                                         max_height=4,
                                         relx=107,
                                         rely=7, )

        self.selected_img_box = self.add(NewBox,
                                         name="Selected Image:",
                                         max_width=63,
                                         max_height=4,
                                         relx=77,
                                         rely=2)

        self.display_block = self.add(npyscreen.BoxTitle,
                                      name="Block Size",
                                      max_width=28,
                                      max_height=7,
                                      relx=77,
                                      rely=7,
                                      footer="Minimum USB Size")

        self.display_block.values = ["     ▼", "  Selected: "+self.parentApp.selected_block, "",
                                     " -Rec. Size For Image-", "                ▲"]

        self.block_check = self.add(CheckBoxBox,
                                    name="Block Size Options:",
                                    max_width=33,
                                    max_height=6,
                                    relx=107,
                                    rely=12,
                                    value=[0, ],
                                    values=["Use Default (512K)", "Auto Detect", "Use Block Size Slider"])

        self.bs_slide = self.add(SliderBox,
                                 name="Block Size Slider:",
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
        self.para.values = ["", " STEP 1:", "   │Select an Image Category.", "   │Select an Image.",
                            "   │Select an USB Device", "", " STEP 2:", "   │Configure Block Size", "   │(optional)",
                            "", " STEP 3:", "   │Select the Yellow OK", "   │Write", "   │Profit $$"]

        self.sel_widgets = [self.cat, self.usb, self.img, self.block_check, self.bs_slide]
        self.all_widgets = [self.cat, self.usb, self.img, self.block_check, self.bs_slide, self.display_block,
                            self.selected_img_box, self.selected_usb_box, self.written, self.pbar, self.img, self.usb,
                            self.cat]

        self.display_block.editable = False
        self.para.editable = False
        self.bs_slide.editable = False

        self.bs_slide.editable = self.parentApp.activate_bs_slider

        self.img.values = ["- Select a Category First -"]
        self.selected_img_box.value = "Not Yet Selected"
        self.selected_usb_box.value = "Not Yet Selected"

        # Add the handler
        self.add_event_hander("DISPLAY", self.update_prog_handler)

    # EVENT HANDLER FOR PROGRESS
    def update_prog_handler(self, event):
        if self.parentApp.selected_image is not None:
            self.written.value = str(self.parentApp.current_write) + " / " + \
                                 str(self.parentApp.selected_image.get_size())
        else:
            self.written.value = "0 / 0 MB"
        self.pbar.value = self.parentApp.percent
        self.written.display()
        self.pbar.display()

    def on_ok(self):
        if not self.parentApp.IS_WRITING:  # Disable ok button
            image = self.parentApp.selected_image
            usb = self.parentApp.selected_usb
            block = self.parentApp.selected_block
            pass1 = True
            compat = True
            # Check if everything is selected
            if image is None and usb is None:
                self.err_pop("image or usb device")
                pass1 = False
            else:
                if image is None:
                    self.err_pop("image")
                    pass1 = False
                if usb is None:
                    self.err_pop("usb device")
                    pass1 = False

            # Check if devices are compatible
            if pass1:
                compat = lluv.check_compatibility(usb.get_size(), image.get_rsize())
                if not compat:
                    self.aux_pop("The selected usb device is not large enough for the selected image. ("
                                 + image.get_name() + ") has a recommended size of " + image.get_rsize(),
                                 "Not Compatible")
            # Initialize write popup
            if pass1 and compat:
                result = self.warning_yesno(image.get_name(), usb.get_name(), block)
                # BEGIN WRITE
                if result:
                    for widget in self.all_widgets:
                        widget.editable = False
                    self.parentApp.IS_WRITING = True  # Flag as ready to write
                    if self.parentApp.IS_WRITING and not self.parentApp.running:  # If the start is seleceted and dd
                        self.parentApp.running = True
                        p = multiprocessing.Process(target=lluv_write_ex, args=(  # isn't already running
                            self.parentApp.selected_image.get_cat() + "/" + self.parentApp.selected_image.get_name(),
                            self.parentApp.selected_usb.get_path(),
                            self.parentApp.selected_block,
                            self.parentApp.selected_image.get_size(),))
                        p.start()

    def on_cancel(self):
        if not self.parentApp.IS_WRITING:  # Disable cancel button
            self.full_reset()

    def adjust_widgets(self):
        # Write complete pop
        if self.parentApp.IS_DONE_WRITE is True:
            self.aux_pop("WRITE DONE", "DONE")
        # Check
        if self.parentApp.selected_category is None:
            self.img.editable = False
        else:
            if not self.parentApp.IS_WRITING:
                self.img.editable = True
        # Set Data
        if self.parentApp.selected_image is not None:
            self.written.value = str(self.parentApp.current_write)+" / "+str(self.parentApp.selected_image.get_size())
        else:
            self.written.value = "0 / 0 MB"
        if self.cat.value is not None:
            self.parentApp.selected_category = self.parentApp.img_categories[self.cat.value]
        if self.usb.value is not None:
            self.parentApp.selected_usb = self.parentApp.usb_list[self.usb.value]
        if self.img.value is not None:
            self.parentApp.selected_image = self.parentApp.img_list[self.img.value]
        # Update Img listing
        if self.parentApp.selected_category is None:
            self.img.values = ["- Select a Category First -"]
        else:
            self.parentApp.img_list = lluv.generate_list(self.parentApp.selected_category.get_images())
            self.img.values = self.parentApp.img_list
        # update selected views

        if self.parentApp.selected_image is None:
            self.selected_img_box.value = "Not Yet Selected"
        else:
            self.selected_img_box.value = self.parentApp.selected_image.get_name()

        if self.parentApp.selected_usb is None:
            self.selected_usb_box.value = "Not Yet Selected"
        else:
            self.selected_usb_box.value = self.parentApp.selected_usb.get_name()

        # update block size
        block_sizes = ["512b", "1K", "2K", "4k", "8K", "16K", "32K", "64K", "128K", "256K", "512K", "1M", "2M",
                       "4M", "8M", "16M", "32M", "64M"]
        if self.block_check.value == [2]:
            if not self.parentApp.IS_WRITING:
                self.bs_slide.editable = True
            self.parentApp.haspoped = False
            self.parentApp.selected_block = block_sizes[int(round(self.bs_slide.value))]
        elif self.block_check.value == [1]:
            self.bs_slide.editable = False
            if not self.parentApp.haspoped:
                self.spawn_autobs_pop()
                if self.parentApp.selected_usb is not None:
                    result = lluv.calculate_block_size(self.parentApp.selected_usb.get_path())
                    if result == '':
                        self.spawn_cantauto_pop()
                    else:
                        self.spawn_canauto_pop()
                        self.parentApp.selected_block = result
                else:
                    self.spawn_nousb_pop()
                self.parentApp.haspoped = True
        elif self.block_check.value == [0]:
            self.bs_slide.editable = False
            self.parentApp.haspoped = False
            self.parentApp.selected_block = "512K"

        if self.parentApp.selected_image is None:
            self.display_block.values = ["     ▼", "  Selected: " + self.parentApp.selected_block, "",
                                         " -Rec. Size For Image-", "                ▲"]
        else:
            self.display_block.values = ["     ▼", "  Selected: " + self.parentApp.selected_block, "",
                                         "  Minimum Size: "+self.parentApp.selected_image.get_rsize(),
                                         "                ▲"]

    def while_editing(self, *args, **keywords):
        self.parentApp.refresh()
        self.cat.values = self.parentApp.img_categories
        self.usb.values = self.parentApp.usb_list

    def while_waiting(self):
        if self.parentApp.percent == 100:
                self.pbar.value = 100
                if self.parentApp.selected_image is not None:  # make sure 100 is displayed
                    self.written.value = self.written.value = \
                        str(self.parentApp.selected_image.get_size()[:len(self.parentApp.selected_image.get_size())-2]) \
                        + " / " + \
                        str(self.parentApp.selected_image.get_size())
                    self.pbar.display()
                    self.written.display()
                self.parentApp.IS_WRITING = False
                self.parentApp.running = False
                self.parentApp.IS_DONE_WRITE = True
                self.aux_pop(
                    self.parentApp.selected_image.get_name() + " was written to " +
                    self.parentApp.selected_usb.get_name() + " successfully!", "Writing Successful")
                # Begin Cancel Form
                self.full_reset()


    def full_reset(self):
        self.parentApp.reset_values()
        self.parentApp.switchForm('MAIN')
        self.selected_usb_box.value = "Not Yet Selected"
        self.selected_img_box.value = "Not Yet Selected"
        self.img.values = ["- Select a Category First -"]
        self.bs_slide.value = 0
        self.pbar.value = 0
        self.parentApp.selected_image = None
        self.parentApp.current_write = 0
        self.parentApp.selected_category = None
        self.parentApp.selected_block = "512K"
        self.parentApp.selected_usb = None
        self.parentApp.haspoped = False
        self.display_block.values = ["     ▼", "  Selected: " + self.parentApp.selected_block, "",
                                     "-Rec. Size For Image-", "                ▲"]
        for widget in self.sel_widgets:
            widget.value = None
        self.block_check.value = [0]
        self.written.value = "0 / 0 MB"
        self.bs_slide.editable = False

    def spawn_autobs_pop(self):
        message = "You have selected auto block size. This should work on your storage device if it is" \
                  "allocated and partition one is writable. LLUV will now find an optimal block size..."
        npyscreen.notify_confirm(message, title="AUTO BLOCK SIZE", wrap=True)

    def spawn_nousb_pop(self):
        message = "No USB device is selected..."
        npyscreen.notify_confirm(message, title="AUTO BLOCK SIZE", wrap=True)

    def spawn_cantauto_pop(self):
        message = "LLUV was not able to generate an optimal block size, This could be because the drive is " \
                  "un allocated or the drive is read only (ex. already a live usb)"
        npyscreen.notify_confirm(message, title="AUTO BLOCK SIZE", wrap=True)

    def spawn_canauto_pop(self):
        message = "An optimal block size was found. Setting as selected block size..."
        npyscreen.notify_confirm(message, title="AUTO BLOCK SIZE", wrap=True)

    def err_pop(self, forgot: str):
        message = "There was no "+forgot+" selected"
        npyscreen.notify_confirm(message, title="Error", wrap=True)

    def aux_pop(self, message: str, title: str):
        npyscreen.notify_confirm(message, title=title, wrap=True)

    def warning_yesno(self, image_name: str, usb_name: str, block: str) -> bool:
        message = "You are about to write:\n(" + image_name + ")\n  ▼\n(" + usb_name + ")\nWith block size: "\
                  + block + "\nThis operation can't be undone and anything on the storage device " \
                            "will be destroyed\n" \
                            "Are you sure?"
        return npyscreen.notify_yes_no(message,title="WARNING", form_color="DANGER", wrap=True)


class LluvTui(npyscreen.StandardApp):
    def __init__(self):
        super(LluvTui, self).__init__()
        # DAT
        self.img_categories = lluv.fetch_images(lluv.get_path())  # category List
        self.usb_list = lluv.generate_list(lluv.fetch_usb())   # usb list
        self.img_list = []
        # SEL
        self.selected_category = None  # Hold the objects
        self.selected_image = None
        self.selected_usb = None
        self.selected_block = "512K"  # Default BS
        self.current_write = 0
        self.percent = 0
        # FLA
        self.activate_bs_slider = True
        self.haspoped = False
        self.IS_WRITING = False
        self.IS_DONE_WRITE = False
        self.running = False
        self.waited_a_sec = False

    def onStart(self):
        # Form init
        npyscreen.setTheme(NewTheme)
        self.addForm('MAIN', TitleForm, name="The CSH L.L.U.V. Machine - Page (1/2)", )
        self.addForm('Selection', SelectForm,
                     name="Configure and Write - Page (2/2)",
                     minimum_lines=47, minimum_columns=143)

    def while_waiting(self):
            if self.selected_image is not None and self.IS_WRITING:
                self.percent = lluv.dd_status(int(self.selected_image.get_size()[:len(self.selected_image.get_size()) - 2]))
                self.current_write = round(int(self.selected_image.get_size()[:len(self.selected_image.get_size()) - 2]) *
                                           (self.percent / 100))
            self.queue_event(npyscreen.Event("DISPLAY"))


    def reset_values(self):
        self.refresh()
        # SEL
        self.selected_category = None
        self.selected_image = None
        self.selected_usb = None
        self.selected_block = "512K"  # Default BS
        self.current_write = 0
        self.percent = 0
        # FLA
        self.activate_bs_slider = True
        self.haspoped = False
        self.IS_WRITING = False
        self.IS_DONE_WRITE = False
        self.running = False
        self.waited_a_sec = False

    def refresh(self):
        self.img_categories = lluv.fetch_images(lluv.get_path())
        self.usb_list = lluv.generate_list(lluv.fetch_usb())


def lluv_write_ex(i_name, usb_path, block, i_size):
    """
    spawned as parallel process
    calls the backend dd routine
    :param i_name:
    :param usb_path:
    :param block:
    :param i_size:
    :return:
    """
    lluv.write_to_device(i_name, usb_path, block, i_size, False)


if __name__ == '__main__':
    multiprocessing.set_start_method('spawn')
    lt = LluvTui().run()
