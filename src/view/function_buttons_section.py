import tkinter as tk

from controller.feature_controller import FeatureController
from model.services.app_state_service import AppStateService
from view.utils.feature_button_manager import FeatureButtonManager
from view.widgets.cascade_rename_widget import CascadeRenameWidget
from view.widgets.dependency_highlighting_widget import DependencyHighlightingWidget
from view.widgets.heatmap_widget import HeatmapWidget
from view.widgets.root_nodes_widget import RootNodesWidget


class FunctionButtonSection:
    def __init__(self, master, output, feature_controller: FeatureController, app_state: AppStateService, pack=True):
        self.output = output
        self.feature_controller = feature_controller
        self.app_state = app_state

        self.frame = tk.Frame(master, padx=20)
        self.frame.grid_columnconfigure(1, weight=1)

        if pack:
            self.pack()

        self.manager = FeatureButtonManager(self.app_state)

        DependencyHighlightingWidget(self.frame, self.app_state, self.feature_controller, self.output,
                                     manager=self.manager).grid(row=0, column=0, columnspan=2, sticky="ew")
        HeatmapWidget(self.frame, self.app_state, self.feature_controller, self.output, manager=self.manager).grid(
            row=1, column=0, columnspan=2, sticky="ew")
        RootNodesWidget(self.frame, self.app_state, self.feature_controller, self.output, manager=self.manager).grid(
            row=2, column=0, columnspan=2, sticky="ew")
        CascadeRenameWidget(self.frame, self.app_state, self.feature_controller, self.output,
                            manager=self.manager).grid(row=3, column=0, columnspan=2, sticky="ew")

    def pack(self):
        self.frame.pack(pady=10)
