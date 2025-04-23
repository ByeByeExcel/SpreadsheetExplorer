import tkinter as tk
from model.app_state import AppState
from controller.feature_controller import FeatureController

from view.widgets.dependency_highlighting_widget import DependencyHighlightingWidget
from view.widgets.heatmap_widget import HeatmapWidget
from view.widgets.root_nodes_widget import RootNodesWidget
from view.widgets.cascade_rename_widget import CascadeRenameWidget
from view.widgets.feature_button_manager import FeatureButtonManager

class FunctionButtonSection:
    def __init__(self, master, output, feature_controller: FeatureController, app_state: AppState, pack=True):
        self.output = output
        self.feature_controller = feature_controller
        self.app_state = app_state

        self.frame = tk.Frame(master, padx=20)
        self.frame.grid_columnconfigure(1, weight=1)

        if pack:
            self.pack()

        # Initialize the shared feature button manager
        self.manager = FeatureButtonManager(self.app_state)

        # Add modular widgets with manager support
        DependencyHighlightingWidget(self.frame, self.app_state, self.feature_controller, self.output, manager=self.manager).grid(row=0, column=0, columnspan=2, sticky="ew")
        HeatmapWidget(self.frame, self.app_state, self.feature_controller, self.output, manager=self.manager).grid(row=1, column=0, columnspan=2, sticky="ew")
        RootNodesWidget(self.frame, self.app_state, self.feature_controller, self.output, manager=self.manager).grid(row=2, column=0, columnspan=2, sticky="ew")
        CascadeRenameWidget(self.frame, self.app_state, self.feature_controller, self.output, manager=self.manager).grid(row=3, column=0, columnspan=2, sticky="ew")

    def pack(self):
        self.frame.pack(pady=10)
