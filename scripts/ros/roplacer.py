import tkinter as tk 
from tkinter import ttk, filedialog, messagebox, scrolledtext

BELS = ["A6LUT", "B6LUT", "C6LUT", "D6LUT"]

#base_prefix = ("design_1_i/AXI_RO_Count_0/U0/AXI_RO_Count_v1_0_S00_AXI_inst/"
             #  "RO_COUNT_INST/U0/gen_instances[{gen_inst}].TOP_inst/"
              # "ro_batch_inst/gen_ro[{ro}].ro_inst/")
base_prefix = ("toplevel_i/ROCount_AXI_v1_0_0/U0/rocount_axi_v1_0_S00_AXI_inst/"
               "ROCOUNT_INST/U0/gen_instances[{gen_inst}].TOP_inst/"
               "ro_batch_inst/gen_ro[{ro}].ro_inst/")
def place_lut(cell_path, bel, slice_x, slice_y):
    return (
        f"set_property BEL {bel} [get_cells {cell_path}]\n"
        f"set_property LOC SLICE_X{slice_x}Y{slice_y} [get_cells {cell_path}]\n"
    )

def generate_constraints(layout, x_step, y_step, start_x, start_y, optimal):
    output = ""
    max_x = 43
    max_y = 99
    current_x = start_x
    current_y = start_y

    for inst in range(16):  # gen_inst[0..15]
        for ro in range(3):  # ro[0..2]
            prefix = base_prefix.format(gen_inst=inst, ro=ro)

            if optimal:
               
                lut_positions = [
                    (0, 0), (1, 0),
                    (0, 1), (1, 1),
                    (0, 2), (1, 2),
                    (0, 3), (1, 3),
                    (0, 4), (1, 4)
                ]
                bels = [
                    "A6LUT", "B6LUT",
                    "C6LUT", "D6LUT",
                    "A6LUT", "B6LUT",
                    "C6LUT", "D6LUT",
                    "A6LUT", "B6LUT"
                ]
                cells = [
                    "LUT6_L_NAND0",
                    "LUT6_L_INV0", "LUT6_L_INV1", "LUT6_L_INV2",
                    "LUT6_L_INV3", "LUT6_L_INV4", "LUT6_L_INV5",
                    "LUT6_L_INV6", "LUT6_L_INV7", "LUT6_L_INV8"
                ]
                for (dx, dy), bel, cell in zip(lut_positions, bels, cells):
                    px = current_x + dx
                    py = current_y + dy
                    if px > max_x or py > max_y:
                        continue
                    output += place_lut(f"{prefix}{cell}", bel, px, py)
            else:
                slice_x = current_x
                slice_y = current_y
                output += place_lut(f"{prefix}LUT6_L_NAND0", "A6LUT", slice_x, slice_y)
                for i, bel in zip(range(3), BELS[1:]):
                    output += place_lut(f"{prefix}LUT6_L_INV{i}", bel, slice_x, slice_y)
                for i, bel in zip(range(3, 7), BELS):
                    output += place_lut(f"{prefix}LUT6_L_INV{i}", bel, slice_x, slice_y + 1)
                for i, bel in zip(range(7, 9), BELS[:2]):
                    output += place_lut(f"{prefix}LUT6_L_INV{i}", bel, slice_x, slice_y + 2)
                output += place_lut(f"{prefix}LUT6_L_INV8", "C6LUT", slice_x, slice_y + 2)

           
            if layout == "horizontal":
                current_x += x_step
                if current_x + 1 > max_x:  # Need 2 slices width
                    current_x = 0
                    current_y += 5
                    if current_y > max_y:
                        current_y = 0
            else:
                current_y += y_step * 5
                if current_y + 4 > max_y:
                    current_y = 0
                    current_x += 2
                    if current_x > max_x:
                        current_x = 0

    return output

def run_gui():
    def on_generate():
        layout = layout_var.get()
        optimal = optimal_var.get()
        try:
            x_step = int(x_step_entry.get())
            y_step = int(y_step_entry.get())
            start_x = int(start_x_entry.get())
            start_y = int(start_y_entry.get())
        except ValueError:
            messagebox.showerror("Invalid input", "Step sizes and coordinates must be integers.")
            return

        constraints = generate_constraints(layout, x_step, y_step, start_x, start_y, optimal)
        preview_box.delete("1.0", tk.END)
        preview_box.insert(tk.END, constraints[:10000] + "\n... (truncated)")

        filename = filedialog.asksaveasfilename(
            defaultextension=".xdc",
            filetypes=[("XDC files", "*.xdc")],
            title="Save constraints"
        )
        if not filename:
            return
        with open(filename, "w") as f:
            f.write(constraints)
        messagebox.showinfo("Success", f" Constraints written to {filename}")

    def apply_preset(preset):
        presets = {
            "X0Y0": (0, 0),
            "X0Y50": (0, 50),
            "X22Y50": (22, 50),
            "X22Y0": (22, 0)
        }
        x, y = presets[preset]
        start_x_entry.delete(0, tk.END)
        start_x_entry.insert(0, str(x))
        start_y_entry.delete(0, tk.END)
        start_y_entry.insert(0, str(y))

    def close_app():
        root.destroy()

    root = tk.Tk()
    root.title("Dark XDC Generator")
    root.attributes('-fullscreen', True)

    bg_color = "#1e1e2e"
    accent_color = "#3a57a5"
    fg_color = "#e0e0e0"
    entry_bg = "#2a2a3d"
    highlight = "#414156"

    root.configure(background=bg_color)
    style = ttk.Style(root)
    style.theme_use("clam")

    style.configure("TLabel", background=bg_color, foreground=fg_color)
    style.configure("TButton", background=highlight, foreground=fg_color, padding=6)
    style.configure("TCheckbutton", background=bg_color, foreground=fg_color)
    style.configure("TCombobox", fieldbackground=entry_bg, background=entry_bg, foreground=fg_color)
    style.configure("TEntry", fieldbackground=entry_bg, background=entry_bg, foreground=fg_color)

    topbar = tk.Frame(root, bg=accent_color)
    topbar.pack(side="top", fill="x")

    title_label = tk.Label(topbar, text="  XDC Generator", bg=accent_color, fg="white", font=("Segoe UI", 12, "bold"))
    title_label.pack(side="left", padx=10, pady=5)

    exit_btn = tk.Button(topbar, text=" Exit", command=close_app, bg="#992222", fg="white", relief="flat", font=("Segoe UI", 10, "bold"))
    exit_btn.pack(side="right", padx=10)

    frame = tk.Frame(root, bg=bg_color)
    frame.pack(fill="both", expand=True, padx=40, pady=20)

    def make_label(text, row):
        ttk.Label(frame, text=text).grid(column=0, row=row, sticky="w", pady=4)

    make_label("Layout Direction:", 0)
    layout_var = tk.StringVar(value="vertical")
    layout_combo = ttk.Combobox(frame, textvariable=layout_var, values=["vertical", "horizontal"], width=20)
    layout_combo.grid(column=1, row=0, sticky="w", pady=4)

    make_label("X Step:", 1)
    x_step_entry = ttk.Entry(frame, width=10)
    x_step_entry.insert(0, "5")
    x_step_entry.grid(column=1, row=1, sticky="w", pady=4)

    make_label("Y Step:", 2)
    y_step_entry = ttk.Entry(frame, width=10)
    y_step_entry.insert(0, "3")
    y_step_entry.grid(column=1, row=2, sticky="w", pady=4)

    make_label("Start X:", 3)
    start_x_entry = ttk.Entry(frame, width=10)
    start_x_entry.insert(0, "0")
    start_x_entry.grid(column=1, row=3, sticky="w", pady=4)

    make_label("Start Y:", 4)
    start_y_entry = ttk.Entry(frame, width=10)
    start_y_entry.insert(0, "0")
    start_y_entry.grid(column=1, row=4, sticky="w", pady=4)

    make_label("Presets:", 5)
    presets_frame = tk.Frame(frame, bg=bg_color)
    presets_frame.grid(column=1, row=5, sticky="w", pady=4)
    for preset in ["X0Y0", "X0Y50", "X22Y50", "X22Y0"]:
        tk.Button(presets_frame, text=preset, command=lambda p=preset: apply_preset(p),
                  bg=highlight, fg=fg_color, relief="flat", width=8).pack(side=tk.LEFT, padx=4)

    # Optimal Placement Option
    optimal_var = tk.BooleanVar()
    optimal_check = ttk.Checkbutton(frame, text="Optimal (Criss-Cross) Placement", variable=optimal_var)
    optimal_check.grid(column=1, row=6, sticky="w", pady=4)

    generate_btn = tk.Button(frame, text=" Generate & Save", command=on_generate,
                             bg=accent_color, fg="white", relief="raised", font=("Segoe UI", 11, "bold"))
    generate_btn.grid(column=0, row=7, columnspan=2, pady=16)

    make_label("Preview:", 8)
    preview_box = scrolledtext.ScrolledText(
        frame, width=170, height=30, wrap=tk.NONE,
        bg=entry_bg, fg=fg_color, insertbackground=fg_color
    )
    preview_box.grid(column=0, row=9, columnspan=2, pady=8, sticky="nsew")

    root.bind("<Escape>", lambda e: close_app())
    root.mainloop()

if __name__ == "__main__":
    run_gui()
