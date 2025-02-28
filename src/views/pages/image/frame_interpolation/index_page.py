import customtkinter

import os

from core.consts.app_const import AppConst
from core.exceptions.activation_exception import ActivationException
from core.models.option import Option
from core.utility.language import Language
from core.services.pages.image.frame_interpolation.index_service import IndexService

from domain.adapters.windows.adapter import Adapter
from domain.views.base.base_page import BasePage
from domain.utility.validate import Validate


class IndexPage(BasePage):
    def __init__(self, master, **kwargs):
        super().__init__(
            master,
            input_exts=AppConst.image_exts,
            **kwargs,
        )

    def init_widgets(self):
        super().init_widgets()

        self.provider_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.provider_label_var).grid(row=2, column=0, padx=10, pady=10, sticky="nsew")
        self.provider_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.provider_combobox.grid(row=2, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.mode_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.mode_label_var).grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        self.mode_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.mode_combobox.grid(row=3, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.scale_label_var = customtkinter.StringVar()
        customtkinter.CTkLabel(self.header_frame, textvariable=self.scale_label_var).grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.scale_combobox = customtkinter.CTkOptionMenu(self.header_frame, state="readonly")
        self.scale_combobox.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="nsew")

        self.message_textbox = customtkinter.CTkTextbox(self.run_message_frame, width=360)
        self.message_textbox.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.file_view.set_image_view_visible(True)

    def init_data(self):
        self.index_service = IndexService()
        self.index_service.get_stop = self.get_stop
        self.index_service.set_progress = self.set_progress
        self.index_service.add_message = self.add_message

    def init_language(self):
        self.input_label_var.set(Language.get("ImageFrameInterpolationIndexPageInputFolder"))
        self.input_button_var.set(Language.get("ImageFrameInterpolationIndexPageInputSelect"))
        self.output_label_var.set(Language.get("ImageFrameInterpolationIndexPageOutputFolder"))
        self.output_button_var.set(Language.get("ImageFrameInterpolationIndexPageOutputSelect"))
        self.provider_label_var.set(Language.get("ImageFrameInterpolationIndexPageProvider"))
        self.mode_label_var.set(Language.get("ImageFrameInterpolationIndexPageMode"))
        self.scale_label_var.set(Language.get("ImageFrameInterpolationIndexPageScale"))
        self.progress_label_var.set(Language.get("ImageFrameInterpolationIndexPageProgress"))
        self.start_button_var.set(Language.get("ImageFrameInterpolationIndexPageStart"))
        self.stop_button_var.set(Language.get("ImageFrameInterpolationIndexPageStop"))

        self.provider_source = Adapter.providers
        self.provider_combobox.configure(values=Option.get_text_list(self.provider_source))

        self.mode_source = [
            Option(Language.get("ImageFrameInterpolationIndexPageModeStandard"), "standard"),
        ]
        self.mode_combobox.configure(values=Option.get_text_list(self.mode_source))

        self.scale_source = [
            Option(Language.get("ImageFrameInterpolationIndexPageScaleX2"), "x2"),
            Option(Language.get("ImageFrameInterpolationIndexPageScaleX4"), "x4"),
            Option(Language.get("ImageFrameInterpolationIndexPageScaleX8"), "x8"),
        ]
        self.scale_combobox.configure(values=Option.get_text_list(self.scale_source))

        self.file_switch_source = [
            Option(Language.get("ImageFrameInterpolationIndexPageInputFolder"), "input"),
            Option(Language.get("ImageFrameInterpolationIndexPageOutputFolder"), "output"),
        ]
        self.file_switch.configure(values=Option.get_text_list(self.file_switch_source))
        self.file_switch.set(self.file_switch_source[0].text)

        self.add_message(Language.get("ImageFrameInterpolationHelp"), "success")

    def set_show(self):
        self.update()
        self.set_file_grid_view()

    def set_hide(self):
        pass

    def get_provider(self):
        item = Option.get_text_item(self.provider_source, self.provider_combobox.get())
        return item.value

    def set_provider(self, value):
        item = Option.get_value_item(self.provider_source, value)
        self.provider_combobox.set(item.text)

    def get_mode(self):
        item = Option.get_text_item(self.mode_source, self.mode_combobox.get())
        return item.value

    def set_mode(self, value):
        item = Option.get_value_item(self.mode_source, value)
        self.mode_combobox.set(item.text)

    def get_scale(self):
        item = Option.get_text_item(self.scale_source, self.scale_combobox.get())
        return item.value

    def set_scale(self, value):
        item = Option.get_value_item(self.scale_source, value)
        self.scale_combobox.set(item.text)

    def set_file_view(self):
        path = self.file_grid.get_checked_item()
        if path:
            self.file_view.set_image(path)
        else:
            self.file_view.clear_image()

    def start(self):
        try:
            self.set_file_switch_grid_view("input")
            self.start_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            input = self.input_entry_var.get()
            if not os.path.isdir(input):
                raise Exception(Language.get("ImageFrameInterpolationIndexPageInputError"))
            output = self.output_entry_var.get()
            if not os.path.isdir(output):
                raise Exception(Language.get("ImageFrameInterpolationIndexPageOutputError"))
            input_files = self.file_grid.get_file_path()
            if not input_files:
                raise Exception(Language.get("ImageFrameInterpolationIndexPageFileError"))
            provider = self.get_provider()
            if provider is None:
                raise Exception(f"{Language.get("ImageFrameInterpolationIndexPageParamError")}: provider: {provider}")
            mode = self.get_mode()
            if mode is None:
                raise Exception(f"{Language.get("ImageFrameInterpolationIndexPageParamError")}: mode: {mode}")
            scale = self.get_scale()
            if scale is None:
                raise Exception(f"{Language.get("ImageFrameInterpolationIndexPageParamError")}: scale: {scale}")
            self.index_service.start(input, output, input_files, provider, mode, scale)
            self.set_file_switch_grid_view("output")
        except ActivationException:
            Validate.license_order_window_show()
        except Exception as e:
            self.add_message(e, "error")
        finally:
            self.start_button.configure(state="normal")
            self.stop_button.configure(state="disabled")
            self.set_progress(0)
