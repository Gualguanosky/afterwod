# Aesthetic definitions for Militar Box Afterwod - Pink Edition
import customtkinter as ctk

class Styles:
    # Colors - Pink and Deep Black
    BG_COLOR = "#0D0D0D"         # Very dark background
    CARD_BG = "#1A1A1A"          # Subtle card background
    SIDEBAR_COLOR = "#121212"    # Sidebar color
    
    # Militar Box Pink
    ACCENT_COLOR = "#F4A2B9"     # The primary pink from the logo
    ACCENT_LIGHT = "#FFBCCF"     # Lighter pink
    ACCENT_HOVER = "#D17A91"     # Darker pink for hover
    
    TEXT_COLOR = "#FFFFFF"
    TEXT_SECONDARY = "#999999"
    
    # Action Colors
    SUCCESS = "#28A745"
    DANGER = "#DC3545"
    INFO = "#F4A2B9"             # Using pink as info as well
    
    # Border & Corner Radii
    CORNER_RADIUS = 15
    BORDER_WIDTH = 2
    BORDER_COLOR = "#252525"     # Subtle border
    
    # Fonts
    FONT_HEADER = ("Impact", 32) # More "military/gym" look
    FONT_SUBHEADER = ("Segoe UI", 22, "bold")
    FONT_CARD_TITLE = ("Segoe UI", 16, "bold")
    FONT_BODY = ("Segoe UI", 13)
    FONT_LABEL = ("Segoe UI", 12, "bold")

def apply_theme():
    ctk.set_appearance_mode("Dark")
    ctk.set_default_color_theme("blue")
