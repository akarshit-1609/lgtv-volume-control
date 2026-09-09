import customtkinter as ctk
import tkinter as tk
import math
import sys
import ipaddress
import threading
import platform
from pathlib import Path
from lgtv_volume import LGTVVolumeControl


def resource_path(relative_path: str) -> Path:
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        base_path = Path(sys._MEIPASS)
    else:
        base_path = Path(__file__).resolve().parent
    return base_path / relative_path


class VolumeControlApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("LG TV Volume Control")
        self.geometry("480x440")
        self.configure(fg_color="#212328")
        self.resizable(False, False)

        system = platform.system()
        if system == "Windows":
            icon_path = resource_path("icons/icon.ico")
            self.iconbitmap(str(icon_path))
        elif system in ("Linux", "Darwin"):
            icon_path = resource_path("icons/icon_64x64.png")
            icon = tk.PhotoImage(file=str(icon_path))
            self.iconphoto(True, icon)
            self._icon = icon

        self.device = LGTVVolumeControl()

        self.volume = 0
        self.is_muted = False

        self.build_ui()
        self.update_ui()

    def build_ui(self):
        top_controls_frame = ctk.CTkFrame(self, fg_color="transparent")
        top_controls_frame.pack(fill="x", padx=30, pady=20)

        pm_bg = ctk.CTkFrame(top_controls_frame, fg_color="#181A1F", corner_radius=5, width=90, height=40)
        pm_bg.pack(side="left")
        pm_bg.pack_propagate(False)

        self.btn_plus = ctk.CTkButton(pm_bg, width=35, height=35, text="+", font=("Helvetica", 24), 
                                      fg_color="#2A2D35", hover_color="#3A3D46", text_color="#FFFFFF",
                                      corner_radius=5, cursor="hand2", command=lambda: threading.Thread(target=self.volume_up, daemon=True).start())
        self.btn_plus.place(relx=0.25, rely=0.5, anchor="center")

        self.btn_minus = ctk.CTkButton(pm_bg, width=35, height=35, text="−", font=("Helvetica", 24), 
                                       fg_color="#2A2D35", hover_color="#3A3D46", text_color="#FFFFFF",
                                       corner_radius=5, cursor="hand2", command=lambda: threading.Thread(target=self.volume_down, daemon=True).start())
        self.btn_minus.place(relx=0.75, rely=0.5, anchor="center")

        self.ip_bg = ctk.CTkFrame(top_controls_frame, fg_color="#2A2D35", corner_radius=8, height=30)
        self.ip_bg.pack(side="left", expand=True, padx=10)
        
        self.ip_entry = ctk.CTkEntry(self.ip_bg, width=120, height=30, fg_color="transparent", border_width=0,
                                     text_color="#FFFFFF", font=("Helvetica", 12), justify="center",
                                     placeholder_text="IPv4 Address")
        self.ip_entry.pack(padx=5, pady=2)
        ip_addr = self.device.getIP()
        if (ip_addr != ""):
            self.ip_entry.insert(0, ip_addr)
        self.ip_entry.bind("<Return>", lambda e: threading.Thread(target=self.on_ip_enter, daemon=True).start())

        input_container = ctk.CTkFrame(top_controls_frame, fg_color="transparent")
        input_container.pack(side="right")
        
        lbl_set_vol = ctk.CTkLabel(input_container, text="SET VOLUME:", text_color="#8F939D", font=("Helvetica", 10, "bold"))
        lbl_set_vol.pack(anchor="e")

        input_bg = ctk.CTkFrame(input_container, fg_color="#2A2D35", corner_radius=8, width=45, height=30)
        input_bg.pack(anchor="e", pady=2)
        input_bg.pack_propagate(False)

        self.vol_entry = ctk.CTkEntry(input_bg, width=45, height=30, fg_color="transparent", border_width=0, 
                                      text_color="#FFFFFF", font=("Helvetica", 14), justify="center")
        self.vol_entry.pack(side="left")
        self.vol_entry.bind("<Return>", lambda e: threading.Thread(target=self.set_volume, daemon=True).start())

        arrows_frame = ctk.CTkFrame(input_bg, fg_color="transparent", width=20)
        arrows_frame.pack(side="right", fill="y", padx=2)

        self.canvas_size = 240
        self.center = self.canvas_size / 2
        self.radius_outer = 100
        self.radius_inner = 80
        
        self.canvas = tk.Canvas(self, width=self.canvas_size, height=self.canvas_size, 
                                bg="#212328", highlightthickness=0)
        self.canvas.pack(pady=5)

        self.draw_ticks()

        self.canvas.create_oval(self.center-self.radius_inner-5, self.center-self.radius_inner-5, 
                                self.center+self.radius_inner+5, self.center+self.radius_inner+5, 
                                fill="#16171B", outline="#111215", width=2)
        self.canvas.create_oval(self.center-self.radius_inner, self.center-self.radius_inner, 
                                self.center+self.radius_inner, self.center+self.radius_inner, 
                                fill="#23262C", outline="#373B45", width=1)
        
        self.text_percent = self.canvas.create_text(self.center, self.center-5, text="-%", 
                                                    fill="#FFFFFF", font=("Helvetica", 36, "bold"))
        self.text_vol_lbl = self.canvas.create_text(self.center, self.center+25, text="VOL", 
                                                    fill="#8F939D", font=("Helvetica", 12))

        self.canvas.create_text(self.center-65, self.center+105, text="0", fill="#626670", font=("Helvetica", 10))
        self.canvas.create_text(self.center+65, self.center+105, text="100", fill="#626670", font=("Helvetica", 10))

        mute_container = ctk.CTkFrame(self, fg_color="#181A1F", corner_radius=20, height=40)
        mute_container.pack(pady=10)
        
        speaker_bg = ctk.CTkFrame(mute_container, fg_color="#3670B4", corner_radius=15, width=40, height=30)
        speaker_bg.pack(side="left", padx=5, pady=5)
        speaker_bg.pack_propagate(False)
        self.speaker_icon = ctk.CTkLabel(speaker_bg, text="🔊", font=("Helvetica", 28, "normal"), text_color="#FFFFFF")
        self.speaker_icon.place(relx=0.5, rely=0.5, anchor="center")

        self.btn_mute = ctk.CTkButton(mute_container, text="MUTE", fg_color="transparent", 
                                      hover_color="#2A2D35", text_color="#8F939D", font=("Helvetica", 12, "bold"),
                                      command=lambda: threading.Thread(target=self.on_mute_click, daemon=True).start(), width=60, cursor="hand2")
        self.btn_mute.pack(side="left", padx=(0, 10))

    def draw_ticks(self):
        start_ang = 135
        end_ang = -45
        total_ang = start_ang - end_ang
        num_ticks = 40
        for i in range(num_ticks + 1):
            angle_deg = start_ang - (i * (total_ang / num_ticks))
            angle_rad = math.radians(angle_deg)
            tick_len = 8 if i % 4 == 0 else 4
            r1 = self.radius_outer + 8
            r2 = r1 + tick_len
            x1 = self.center + r1 * math.cos(angle_rad)
            y1 = self.center - r1 * math.sin(angle_rad)
            x2 = self.center + r2 * math.cos(angle_rad)
            y2 = self.center - r2 * math.sin(angle_rad)
            color = "#454955" if i % 4 == 0 else "#2C2E36"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2 if i % 4 == 0 else 1)

    def update_dial(self):
        if hasattr(self, 'vol_arc'):
            self.canvas.delete(self.vol_arc)
        if hasattr(self, 'vol_arc_glow'):
            self.canvas.delete(self.vol_arc_glow)
        start_angle = 225 
        max_extent = -270
        current_extent = (self.volume / 100.0) * max_extent
        bounding_box = (self.center - self.radius_outer, self.center - self.radius_outer,
                        self.center + self.radius_outer, self.center + self.radius_outer)
        self.vol_arc_glow = self.canvas.create_arc(*bounding_box, start=start_angle, extent=current_extent, 
                                                   style=tk.ARC, outline="#1B5D8C", width=12)
        self.vol_arc = self.canvas.create_arc(*bounding_box, start=start_angle, extent=current_extent, 
                                              style=tk.ARC, outline="#2FB2FF", width=6)

    def on_ip_enter(self, event=None):
        self.allInputsEnable(False)
        ip_str = self.ip_entry.get().strip()
        try:
            _ = ipaddress.IPv4Address(ip_str)
            self.ip_entry.configure(state=ctk.DISABLED, text_color="#27C93F")
            self.device.updateIP(ip_str)
            self.allInputsEnable(True)
            self.update_ui()
            self.ip_entry.configure(state=ctk.NORMAL, text_color="#FFFFFF")
            
        except ipaddress.AddressValueError:
            self.ip_entry.delete(0, "end")
            self.ip_entry.configure(text_color="#FF5F56")
            self.ip_entry.insert(0, "Invalid IP!")
            
            def reset_error():
                self.ip_entry.delete(0, "end")
                self.ip_entry.configure(text_color="#FFFFFF")
                self.ip_entry.insert(0, ip_str)
                self.ip_entry.configure(state=ctk.NORMAL)
                
            self.after(800, reset_error)

    def update_ui(self):
        data = self.device.getVolumeStats()
        self.vol_entry.delete(0, "end")
        if data["volume"] != None:
            self.volume = data["volume"]
            self.canvas.itemconfig(self.text_percent, text=f"{self.volume}%")
            self.vol_entry.insert(0, str(self.volume))
            self.update_dial()
        else:
            self.canvas.itemconfig(self.text_percent, text=f"-%")

        if data["muted"] != None:
            self.is_muted = data["muted"]
            if self.is_muted:
                self.speaker_icon.configure(text="🔇")
                self.btn_mute.configure(text="UNMUTE")
            else:
                self.speaker_icon.configure(text="🔊")
                self.btn_mute.configure(text="MUTE")

    def set_volume(self, event=None):
        vol = max(0, min(100, int(self.vol_entry.get())))
        self.device.setVolume(vol)
        self.update_ui()

    def volume_up(self):
        self.device.volumeUp()
        self.update_ui()

    def volume_down(self):
        self.device.volumeDown()
        self.update_ui()

    def on_mute_click(self):
        self.is_muted = not self.is_muted
        self.device.mute(self.is_muted)
        self.update_ui()

    def allInputsEnable(self, state: bool):
        if state:
            self.ip_entry.configure(state=ctk.NORMAL)
            self.vol_entry.configure(state=ctk.NORMAL)
            self.btn_plus.configure(state=ctk.NORMAL)
            self.btn_minus.configure(state=ctk.NORMAL)
            self.btn_mute.configure(state=ctk.NORMAL)
        else:
            self.ip_entry.configure(state=ctk.DISABLED)
            self.vol_entry.configure(state=ctk.DISABLED)
            self.btn_plus.configure(state=ctk.DISABLED)
            self.btn_minus.configure(state=ctk.DISABLED)
            self.btn_mute.configure(state=ctk.DISABLED)


if __name__ == "__main__":
    app = VolumeControlApp()
    app.mainloop()