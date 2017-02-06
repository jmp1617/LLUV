"""
TUI for lluv

author: Jacob Potter CSH:(jpotter)
"""
import npyscreen
import lluv.lluv as lluv
import multiprocessing
import sys

# WIDGET SUBCLASSES
class FilePicker(npyscreen.FilenameCombo):
    def __init__(self, *args, **keywords):
        super(FilePicker, self).__init__(*args, **keywords)
        self.must_exist=False
        self.sort_by_extansion=True
        self.select_dir=True


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
        return vl.get_name() + " - " + str(vl.get_size() / 1000000000).split(".")[0] + " GB"


class CatagorySel(npyscreen.MultiLine):
    def __init__(self, *args, **keywords):
        super(CatagorySel, self).__init__(*args, **keywords)

    def display_value(self, vl):
        return vl.get_name()


class BSSlider(npyscreen.Slider):
    def __init__(self, *args, **keywords):
        super(BSSlider, self).__init__(*args, **keywords)
        self.out_of = 17  # 18 dif bs
        self.color = 'NO_EDIT'

    def translate_value(self):
        block_sizes = ["512b", "1K", "2K", "4k", "8K", "16K", "32K", "64K", "128K", "256K", "512K", "1M", "2M",
                       "4M", "8M", "16M", "32M", "64M"]
        selval = int(round(self.value))
        return block_sizes[selval]


class ProgressBar(npyscreen.SliderPercent):
    def __init__(self, *args, **keywords):
        super(ProgressBar, self).__init__(*args, **keywords)
        self.editable = False
        self.accuracy = 0
        self.color = 'NO_EDIT'


class TextItem(npyscreen.FixedText):
    def __init__(self, *args, **keywords):
        super(TextItem, self).__init__(*args, **keywords)
        self.editable = False

# BOX WRAPPERS
class FilePickerBox(npyscreen.BoxTitle):
    _contained_widget = FilePicker


class ImgSelectionBox(npyscreen.BoxTitle):
    _contained_widget = ImgSel


class UsbSelectionBox(npyscreen.BoxTitle):
    _contained_widget = USBSel


class CatSelectionBox(npyscreen.BoxTitle):
    _contained_widget = CatagorySel


class SliderBox(npyscreen.BoxTitle):
    _contained_widget = BSSlider


class CheckBoxBox(npyscreen.BoxTitle):
    _contained_widget = npyscreen.SelectOne


class NewBox(npyscreen.BoxTitle):
    _contained_widget = TextItem


class ProgressBarBox(npyscreen.BoxTitle):
    _contained_widget = ProgressBar

# FORM THEME


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

# SPLASH SCREEN FORM


class TitleForm(npyscreen.Form):
    def create(self):
        l_space = 12

        the1 = " " * 5 + "╔╦╗┬ ┬┌─┐"
        the2 = " " * 5 + " ║ ├─┤├┤ "
        the3 = " " * 5 + " ╩ ┴ ┴└─┘"

        mac1 = " " * 75 + "╔╦╗┌─┐┌─┐┬ ┬┬┌┐┌┌─┐"
        mac2 = " " * 75 + "║║║├─┤│  ├─┤││││├┤ "
        mac3 = " " * 75 + "╩ ╩┴ ┴└─┘┴ ┴┴┘└┘└─┘"

        title_block1 = " " * l_space + "          ,gggg,          ,gggg,    ,ggg,         gg  ,ggg,         ,gg "
        title_block2 = " " * l_space + "         d8\" \"8I         d8\"  \"8I  dP\"\"Y8a        88 dP\"\"Y8a       ,8P "
        title_block3 = " " * l_space + "         88  ,dP         88  ,dP   Yb, `88        88 Yb, `88       d8' "
        title_block4 = " " * l_space + "      8888888P\"       8888888P\"     `\"  88        88  `\"  88       88  "
        title_block5 = " " * l_space + "          88              88            88        88      88       88      "
        title_block6 = " " * l_space + "          88              88            88        88      I8       8I "
        title_block7 = " " * l_space + "     ,aa,_88         ,aa,_88            88        88      `8,     ,8'  "
        title_block8 = " " * l_space + "    dP\" \"88P        dP\" \"88P            88        88       Y8,   ,8P   "
        title_block9 = " " * l_space + "    Yb,_,d88b,,_    Yb,_,d88b,,_        Y8b,____,d88,       Yb,_,dP     "
        title_block10 = " " * l_space + "     \"Y8P\"  \"Y88888  \"Y8P\"  \"Y88888      \"Y888888P\"Y8        \"Y8P\"  "
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
                      title_block10, "", " " * l_space * 3 + "( Linux Live USB Vending )", "", "", "", "", "", "", mac1,
                      mac2, mac3]
        box.editable = False

    def afterEditing(self):
        self.parentApp.setNextForm('Selection')


# MAIN FORM


class SelectForm(npyscreen.ActionForm):
    def create(self):
        self.keypress_timeout = 10

        # CREATE WIDGETS
        # category selection
        self.cat = self.add(CatSelectionBox,
                            name="Select an Category:",
                            max_width=30,
                            relx=3,
                            rely=2,
                            max_height=39,
                            values=self.parentApp.img_categories)
        # usb device selection
        self.usb = self.add(UsbSelectionBox,
                            name="Select a USB Device:",
                            max_width=40,
                            max_height=12,
                            relx=35,
                            rely=2,
                            values=self.parentApp.usb_list)
        # image selection box - becomes editable once a category
        self.img = self.add(ImgSelectionBox,
                            name="Select an Image",
                            max_width=70,
                            max_height=22,
                            relx=35,
                            rely=15,
                            values=["- Select a Category First -"])
        # isodir path selection widget
        self.file_pick = self.add(FilePickerBox,
                            name="Change which image directory the config points to :",
                            max_width=70,
                            relx=35,
                            rely=38,
                            max_height=3,
                            value=lluv.get_path(),
                            footer="Selection will be saved to the config")
        # progress bar - an altered slider widget
        self.pbar = self.add(ProgressBarBox,
                             max_height=3,
                             max_width=115,
                             out_of=100,
                             name="Write Progress:",
                             relx=3, rely=42)
        # box to show how much data has been written
        self.written = self.add(NewBox,
                                name="Written:",
                                max_width=20,
                                rely=42, relx=120,
                                max_height=3,
                                value="0 / 0 MB")
        # box to show selected usb
        self.selected_usb_box = self.add(NewBox,
                                         name="Selected USB Device:",
                                         max_width=33,
                                         max_height=4,
                                         relx=107,
                                         rely=7,
                                         value="Not Yet Selected")
        # box to show selected image
        self.selected_img_box = self.add(NewBox,
                                         name="Selected Image:",
                                         max_width=63,
                                         max_height=4,
                                         relx=77,
                                         rely=2,
                                         value="Not Yet Selected")
        # box to show block size and minimum recommended usb size
        self.display_block = self.add(npyscreen.BoxTitle,
                                      name="Block Size",
                                      max_width=28,
                                      max_height=7,
                                      relx=77,
                                      rely=7,
                                      footer="Minimum USB Size")
        self.display_block.values = ["     ▼", "  Selected: " + self.parentApp.selected_block, "",
                                     " -Rec. Size For Image-", "                ▲"]
        # box to display block options - check box field
        self.block_check = self.add(CheckBoxBox,
                                    name="Block Size Options:",
                                    max_width=33,
                                    max_height=6,
                                    relx=107,
                                    rely=12,
                                    value=[0, ],
                                    values=["Use Default (512K)", "Auto Detect", "Use Block Size Slider"])
        # slider to choose block size
        self.bs_slide = self.add(SliderBox,
                                 name="Block Size Slider:",
                                 max_width=33,
                                 max_height=3,
                                 relx=107,
                                 rely=19)
        # How to box
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

        # Lists of widgets sel_widgets: widgets that can have states
        self.sel_widgets = [self.cat, self.usb, self.img, self.block_check, self.bs_slide]
        self.all_widgets = [self.cat, self.usb, self.img, self.block_check, self.bs_slide, self.display_block,
                            self.selected_img_box, self.selected_usb_box, self.written, self.pbar, self.img, self.usb,
                            self.cat]

        # set certain widgets as un editable
        self.display_block.editable = False  # Block
        self.para.editable = False           # How to box
        self.bs_slide.editable = False       # Temp block size slider
        self.img.editable = False            # Temp image box

        # Add the handler - handles progressbar and written value changes
        self.add_event_hander("DISPLAY", self.update_prog_handler)

    # EVENT HANDLER FOR PROGRESS
    def update_prog_handler(self, event):
        if self.parentApp.IS_WRITING:  # Double check that the write process is active
            self.written.value = str(self.parentApp.current_write) + " / " + \
                                 str(self.parentApp.selected_image.get_size())  # current write out of img size
            self.pbar.value = self.parentApp.percent    # update the progress bar
            self.written.display()  # redraw both widgets
            self.pbar.display()

    # IF OK IS PRESSED
    def on_ok(self):
        if not self.parentApp.IS_WRITING:  # Disable ok button
            # fetch selected data
            image = self.parentApp.selected_image
            usb = self.parentApp.selected_usb
            block = self.parentApp.selected_block
            everything_selected = True  # all selected flag
            compat = True               # all compatible flag
            # Check if everything is selected
            if image is None and usb is None:
                self.err_pop("image or usb device")
                everything_selected = False
            else:
                if image is None:
                    self.err_pop("image")
                    everything_selected = False
                if usb is None:
                    self.err_pop("usb device")
                    everything_selected = False

            # Check if devices are compatible
            if everything_selected:
                compat = lluv.check_compatibility(usb.get_size(), image.get_rsize())
                if not compat:
                    self.aux_pop("The selected usb device is not large enough for the selected image. ("
                                 + image.get_name() + ") has a recommended size of " + image.get_rsize(),
                                 "Not Compatible")
            # Initialize write popup
            if everything_selected and compat:
                result = self.warning_yesno(image.get_name(), usb.get_name(), block)  # ask the user if they are sure
                # BEGIN WRITE
                if result:  # if they confirmed
                    for widget in self.all_widgets:  # disable all widgets
                        widget.editable = False
                    self.parentApp.IS_WRITING = True  # Flag as ready to write
                    p = multiprocessing.Process(target=lluv_write_ex, args=(  # spawn write process
                        self.parentApp.selected_image.get_cat() + "/" + self.parentApp.selected_image.get_name(),
                        self.parentApp.selected_usb.get_path(),
                        self.parentApp.selected_block,
                        self.parentApp.selected_image.get_size(),))
                    p.start()

    # IF CANCEL IS CLICKED
    def on_cancel(self):
        if not self.parentApp.IS_WRITING:  # Disable cancel button
            if self.parentApp.is_kiosk:
                self.full_reset()   # reset the form # only if kiosk mode
            else:
                sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=24, cols=80))
                print("Exiting TUI")
                exit()  # if not kiosk mode, exit the app after resizing

    # CALLED EVERY TIME THE USER PRESSES A BUTTON
    # will only update values to avoid slow down
    # no redraws except path update
    def adjust_widgets(self):
        # Check to see if the file path has been changed
        if self.file_pick.value != lluv.get_path():  # if the path was changed
            lluv.set_image_path(self.file_pick.value)
            self.parentApp.img_categories = lluv.fetch_images(self.file_pick.value)
            self.cat.values = self.parentApp.img_categories
            self.cat.display()
        # The category has been selected and the parent isn't writing allow images to be altered
        if self.parentApp.selected_category is not None and not self.parentApp.IS_WRITING:
            self.img.editable = True
        # Set the size of the image in the written box
        if self.parentApp.selected_image is not None:
            self.written.value = str(self.parentApp.current_write) + " / " + str(
                self.parentApp.selected_image.get_size())
        # Update the selected values in the parent
        if self.cat.value is not None:
            self.parentApp.selected_category = self.parentApp.img_categories[self.cat.value]
        if self.usb.value is not None:
            self.parentApp.selected_usb = self.parentApp.usb_list[self.usb.value]
        if self.img.value is not None:
            self.parentApp.selected_image = self.parentApp.img_list[self.img.value]
        # Update image listing
        if self.parentApp.selected_category is not None:
            self.parentApp.img_list = lluv.generate_list(self.parentApp.selected_category.get_images())
            self.img.values = self.parentApp.img_list
        # Update selected views
        if self.parentApp.selected_image is not None:
            self.selected_img_box.value = self.parentApp.selected_image.get_name()
        if self.parentApp.selected_usb is not None:
            self.selected_usb_box.value = self.parentApp.selected_usb.get_name()
        # Update block size
        self.update_block_selection()
        # Update the block display
        if self.parentApp.selected_image is not None:
            self.display_block.values = ["     ▼", "  Selected: " + self.parentApp.selected_block, "",
                                         "  Minimum Size: " + self.parentApp.selected_image.get_rsize(),
                                         "                ▲"]

    # FUNCTION TO UPDATE BLOCK SELECTION
    def update_block_selection(self):
        block_sizes = ["512b", "1K", "2K", "4k", "8K", "16K", "32K", "64K", "128K", "256K", "512K", "1M", "2M",
                       "4M", "8M", "16M", "32M", "64M"]
        if self.block_check.value == [2]:       # If use slider is selected
            if not self.parentApp.IS_WRITING:   # If the parent is not writing
                self.bs_slide.editable = True   # Activate the slider
            self.parentApp.haspoped = False     # Flag so that use auto pop will pop again
            self.parentApp.selected_block = block_sizes[int(round(self.bs_slide.value))]  # Get the value of the slider
        elif self.block_check.value == [1]:  # If auto bs is selected
            self.bs_slide.editable = False   # Shut off the slider
            if not self.parentApp.haspoped:  # If the popup has not poped up already
                self.spawn_autobs_pop()      # Spawn the popup
                if self.parentApp.selected_usb is not None:
                    result = lluv.calculate_block_size(self.parentApp.selected_usb.get_path())  # Backend find optimal
                    if result == '':  # if cant find an optimal
                        self.spawn_cantauto_pop()
                    else:             # if can find an optimal
                        self.spawn_canauto_pop()
                        self.parentApp.selected_block = result  # set optimal as selected block
                else:   # if there is no usb selected
                    self.spawn_nousb_pop()
                self.parentApp.haspoped = True  # tell the parent that this has popped so it doesnt do it infinitely
        elif self.block_check.value == [0]:  # if selected is use default
            self.bs_slide.editable = False
            self.parentApp.haspoped = False
            self.parentApp.selected_block = "512K"  # set to default

    # CALLED WHEN THE FORM IS WAITING FOR A EVENT
    # called less frequently so can be used for redraws
    # however, will never be called if the user likes spamming keys at alarming rates
    def while_waiting(self):
        # Refresh usb listing and image listing then redisplay specified widgets
        self.parentApp.refresh()    # refresh parent
        self.usb.values = self.parentApp.usb_list
        self.update_displays()
        # Check to see if the write process was complete
        if self.parentApp.percent == 100:  # Writing process complete
            self.pbar.value = 100
            # Make sure 100 is displayed
            if self.parentApp.selected_image is not None:
                self.written.value = self.written.value = \
                    str(self.parentApp.selected_image.get_size()[:len(self.parentApp.selected_image.get_size()) - 2]) \
                    + " / " + \
                    str(self.parentApp.selected_image.get_size())
                self.pbar.display()
                self.written.display()
            # Reset Flags
            self.parentApp.IS_WRITING = False
            self.parentApp.running = False
            # Alert the user that the write was successful
            self.aux_pop(
                self.parentApp.selected_image.get_name() + " was written to " +
                self.parentApp.selected_usb.get_name() + " successfully!", "Writing Successful")
            # Begin Cancel Form
            self.full_reset()

    # FUNCTION TO REDRAW SELECTED WIDGETS
    def update_displays(self):
        self.selected_usb_box.display()
        self.selected_img_box.display()
        self.display_block.display()
        self.usb.display()

    # FUNCTION TO RESET THE FORM FOR REUSE
    def full_reset(self):
        # Switch the form to title screen
        self.parentApp.switchForm('MAIN')
        # Reset parent
        self.parentApp.reset_values()
        # Reset values
        self.selected_usb_box.value = "Not Yet Selected"
        self.selected_img_box.value = "Not Yet Selected"
        self.img.values = ["- Select a Category First -"]
        self.bs_slide.value = 0
        self.pbar.value = 0
        self.written.value = "0 / 0 MB"
        self.display_block.values = ["     ▼", "  Selected: " + self.parentApp.selected_block, "",
                                     "-Rec. Size For Image-", "                ▲"]
        # Reset all of the widgets states
        for widget in self.sel_widgets:
            widget.value = None
        # Reset default check
        self.block_check.value = [0]
        # Unlock the form
        self.unlock()

    # FUNCTION TO SET INITIALLY EDITABLE WIDGETS AS EDITABLE TO UNLOCK THE FORM
    def unlock(self):
        self.cat.editable = True
        self.usb.editable = True
        self.block_check.editable = True

    # A BUNCH OF POPUPS
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
        message = "There was no " + forgot + " selected"
        npyscreen.notify_confirm(message, title="Error", wrap=True)

    def aux_pop(self, message: str, title: str):
        npyscreen.notify_confirm(message, title=title, wrap=True)

    def warning_yesno(self, image_name: str, usb_name: str, block: str) -> bool:
        message = "You are about to write:\n(" + image_name + ")\n  ▼\n(" + usb_name + ")\nWith block size: " \
                  + block + "\nThis operation can't be undone and anything on the storage device " \
                            "will be destroyed\n" \
                            "Are you sure?"
        return npyscreen.notify_yes_no(message, title="WARNING", form_color="DANGER", wrap=True)


# THE APPLICATION CLASS
class LluvTui(npyscreen.StandardApp):
    def __init__(self):
        super(LluvTui, self).__init__()
        # DATA
        self.img_categories = lluv.fetch_images(lluv.get_path())  # category List
        self.usb_list = lluv.generate_list(lluv.fetch_usb())  # usb list - lluv.fetch_usb by default returns a dict
        self.img_list = []  # to be populated after the category has been selected
        # SELECTIONS AND STATUS
        self.selected_category = None  # Hold the objects
        self.selected_image = None
        self.selected_usb = None
        self.selected_block = "512K"  # Default BS
        self.current_write = 0
        self.percent = 0
        # FLAGS
        self.haspoped = False
        self.IS_WRITING = False
        self.is_kiosk = lluv.isKiosk() # Check to see if the kiosk option was selected in the config

    def onStart(self):
        # Form initialization
        npyscreen.setTheme(NewTheme)  # set the theme
        if(self.is_kiosk):
            self.addForm('MAIN', TitleForm, name="The L.L.U.V. Machine - Page (1/2)", )  # Title form
            name_for_second = "Configure and Write - Page (2/2)"
            title = "Selection"
        else:
            name_for_second = "Configure and Write"
            title = "MAIN"

        self.addForm(title, SelectForm, name=name_for_second, ) # 47 x 143   Main selection form

    # while the form is waiting, if DD is working, send the event to update the progress
    def while_waiting(self):
        if self.IS_WRITING:
            # update parent percent
            self.percent = lluv.dd_status(int(self.selected_image.get_size()[:len(self.selected_image.get_size()) - 2]))
            # update parent current_write
            self.current_write = round(int(self.selected_image.get_size()[:len(self.selected_image.get_size()) - 2]) *
                                       (self.percent / 100))
        # send the event to the child
        self.queue_event(npyscreen.Event("DISPLAY"))

    # function to reset all values for form loop
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
        self.haspoped = False
        self.IS_WRITING = False

    # function to refresh the usb devices
    def refresh(self):
        self.usb_list = lluv.generate_list(lluv.fetch_usb())


# USED TO SPAWN AND PERFORM DD
def lluv_write_ex(i_name, usb_path, block, i_size):
    """
    spawned as parallel process
    calls the backend dd routine
    :param i_name: image name and category
    :param usb_path: usb device
    :param block: selected block
    :param i_size: size of image
    :return:
    """
    lluv.write_to_device(i_name, usb_path, block, i_size, False, "")  # Backend Write


def start():
    LluvTui().run()


if __name__ == '__main__':
    start()
