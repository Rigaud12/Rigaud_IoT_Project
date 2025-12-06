import wx
import pandas as pd
import matplotlib
matplotlib.use("WXAgg")      # REQUIRED ON MAC FOR WX + MATPLOTLIB
import matplotlib.pyplot as plt

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

from iot_step1_generate_data import generate_users_and_sensors


# -----------------------------------------------------
# Simple window wrapper for Matplotlib plots
# -----------------------------------------------------
class PlotWindow(wx.Frame):
    def __init__(self, parent, title="Plot"):
        super().__init__(parent, title=title, size=(800, 600))

        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.figure = Figure()
        self.canvas = FigureCanvas(panel, -1, self.figure)

        vbox.Add(self.canvas, 1, wx.EXPAND)
        panel.SetSizer(vbox)

        self.Show()


# -----------------------------------------------------
# Main Application Class
# -----------------------------------------------------
class IoTApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="IoT Data Generator - wxPython Application", size=(800, 500))
        self.data = None
        self.panel = wx.Panel(self)

        self.CreateMenu()
        self.Show()

    # -----------------------------------------------------
    # MENU BAR
    # -----------------------------------------------------
    def CreateMenu(self):
        menubar = wx.MenuBar()

        # FILE MENU
        fileMenu = wx.Menu()
        gen_item = fileMenu.Append(wx.ID_ANY, "Generate IoT Data")
        save_json = fileMenu.Append(wx.ID_ANY, "Save JSON")
        save_csv = fileMenu.Append(wx.ID_ANY, "Save CSV")
        menubar.Append(fileMenu, "File")

        # STATISTICS MENU
        statsMenu = wx.Menu()
        desc_item = statsMenu.Append(wx.ID_ANY, "Descriptive Statistics")
        plotA = statsMenu.Append(wx.ID_ANY, "Plot A - Outside Temp Histogram")
        plotB = statsMenu.Append(wx.ID_ANY, "Plot B - Outside vs Room Temp Line Graph")
        plotC = statsMenu.Append(wx.ID_ANY, "Plot C - Combined Temp & Humidity Histogram")
        menubar.Append(statsMenu, "Statistics")

        self.SetMenuBar(menubar)

        # BIND EVENTS
        self.Bind(wx.EVT_MENU, self.OnGenerate, gen_item)
        self.Bind(wx.EVT_MENU, self.OnSaveJSON, save_json)
        self.Bind(wx.EVT_MENU, self.OnSaveCSV, save_csv)
        self.Bind(wx.EVT_MENU, self.OnDescStats, desc_item)
        self.Bind(wx.EVT_MENU, self.OnPlotA, plotA)
        self.Bind(wx.EVT_MENU, self.OnPlotB, plotB)
        self.Bind(wx.EVT_MENU, self.OnPlotC, plotC)

    # -----------------------------------------------------
    # DATA GENERATION
    # -----------------------------------------------------
    def OnGenerate(self, event):
        wx.MessageBox("Generating IoT Data, please wait...", "Working")
        self.data = generate_users_and_sensors()
        wx.MessageBox("Data Generation Complete!", "Success")

    # -----------------------------------------------------
    # SAVE JSON
    # -----------------------------------------------------
    def OnSaveJSON(self, event):
        if self.data is None:
            wx.MessageBox("No data generated yet.", "Error")
            return

        dlg = wx.FileDialog(self, "Save JSON", wildcard="JSON files (*.json)|*.json",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            self.data.to_json(dlg.GetPath(), orient="records")
            wx.MessageBox("Saved JSON!", "Success")

    # -----------------------------------------------------
    # SAVE CSV
    # -----------------------------------------------------
    def OnSaveCSV(self, event):
        if self.data is None:
            wx.MessageBox("No data generated yet.", "Error")
            return

        dlg = wx.FileDialog(self, "Save CSV", wildcard="CSV files (*.csv)|*.csv",
                            style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)

        if dlg.ShowModal() == wx.ID_OK:
            self.data.to_csv(dlg.GetPath(), index=False)
            wx.MessageBox("Saved CSV!", "Success")

    # -----------------------------------------------------
    # DESCRIPTIVE STATISTICS
    # -----------------------------------------------------
    def OnDescStats(self, event):
        if self.data is None:
            wx.MessageBox("Generate data first.", "Error")
            return

        desc = self.data.describe().to_string()

        dlg = wx.MessageDialog(self, desc, "Descriptive Statistics", wx.OK)
        dlg.ShowModal()
        dlg.Destroy()

    # -----------------------------------------------------
    # PLOT A – Histogram of Outside Temperature
    # -----------------------------------------------------
    def OnPlotA(self, event):
        if self.data is None:
            wx.MessageBox("Generate data first.", "Error")
            return

        win = PlotWindow(self, "Plot A - Outside Temperature Histogram")
        ax = win.figure.add_subplot(111)

        ax.hist(self.data["outside_temp"], bins=30, color="blue")
        ax.set_title("Outside Temperature Histogram")
        ax.set_xlabel("Temperature (°F)")
        ax.set_ylabel("Frequency")
        win.canvas.draw()

    # -----------------------------------------------------
    # PLOT B – Outside vs Room Temperature Line Graph
    # -----------------------------------------------------
    def OnPlotB(self, event):
        if self.data is None:
            wx.MessageBox("Generate data first.", "Error")
            return

        win = PlotWindow(self, "Plot B - Outside vs Room Temperature")
        ax = win.figure.add_subplot(111)

        ax.plot(self.data["outside_temp"][:500], label="Outside Temp")
        ax.plot(self.data["room_temp"][:500], label="Room Temp")
        ax.set_title("Outside vs Room Temperature (First 500 Samples)")
        ax.set_xlabel("Sample #")
        ax.set_ylabel("Temperature (°F)")
        ax.legend()
        win.canvas.draw()

    # -----------------------------------------------------
    # PLOT C – Combined Temperature & Humidity Histogram
    # -----------------------------------------------------
    def OnPlotC(self, event):
        if self.data is None:
            wx.MessageBox("Generate data first.", "Error")
            return

        win = PlotWindow(self, "Plot C - Combined Temp & Humidity Histogram")
        ax = win.figure.add_subplot(111)

        ax.hist(self.data["outside_temp"], bins=30, alpha=0.5, label="Outside Temp")
        ax.hist(self.data["room_temp"], bins=30, alpha=0.5, label="Room Temp")
        ax.hist(self.data["outside_humidity"], bins=30, alpha=0.5, label="Outside Humidity")
        ax.hist(self.data["room_humidity"], bins=30, alpha=0.5, label="Room Humidity")

        ax.set_title("Combined Histogram")
        ax.set_xlabel("Value")
        ax.set_ylabel("Frequency")
        ax.legend()
        win.canvas.draw()


# -----------------------------------------------------
# RUN APP
# -----------------------------------------------------
if __name__ == "__main__":
    app = wx.App()
    IoTApp()
    app.MainLoop()
