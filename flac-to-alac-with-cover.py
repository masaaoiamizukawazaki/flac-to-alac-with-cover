import os
import subprocess
from pathlib import Path
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
import datetime
import shutil
import threading

import mutagen
from mutagen.flac import FLAC
from mutagen.mp4 import MP4, MP4Cover

LOG_FILE = "convert_log.txt"

def write_log(message):
    now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{now} {message}\n")
    print(f"{now} {message}", flush=True)

class ConverterApp:
    def __init__(self):
        self.stop_requested = False
        self.root = tk.Tk()
        self.root.title("FLAC to ALAC Converter & Cover Embedding Fix Tool")
        self.root.geometry("600x320")
        self.root.resizable(False, False)

        self.input_var = tk.StringVar()
        self.output_var = tk.StringVar()
        self.input_var.trace_add("write", self.on_input_change)

        self.create_widgets()

        self.result = {"input": None, "output": None}
        self.worker_thread = None

        # Get ffmpeg executable path (portable)
        self.ffmpeg_path = self.find_ffmpeg()

    def find_ffmpeg(self):
        # まず同じフォルダにある ffmpeg.exe を探す
        exe_name = "ffmpeg.exe" if os.name == "nt" else "ffmpeg"
        local_path = Path(__file__).parent / exe_name
        if local_path.exists():
            return str(local_path)
        # 見つからなければ環境PATHから
        return exe_name

    def write_log(self, message):
        now = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{now} {message}\n")
        print(f"{now} {message}", flush=True)

    def create_widgets(self):
        def add_row(label_text, var, browse_func):
            frame = ttk.Frame(self.root)
            frame.pack(fill="x", padx=10, pady=5)

            label = ttk.Label(frame, text=label_text, anchor="w", justify="left")
            label.pack(fill="x")

            entry_frame = ttk.Frame(frame)
            entry_frame.pack(fill="x", pady=(2, 0))

            entry = ttk.Entry(entry_frame, textvariable=var)
            entry.pack(side="left", fill="x", expand=True)

            button = ttk.Button(entry_frame, text="Browse...", command=browse_func)
            button.pack(side="left", padx=(5, 0))

            return entry

        self.input_entry = add_row("FLAC Folder:", self.input_var, self.browse_input)
        self.output_entry = add_row("Output Folder:", self.output_var, self.browse_output)

        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=10)
        self.ok_btn = ttk.Button(btn_frame, text="Start Conversion", command=self.on_ok)
        self.ok_btn.pack(side="left", padx=10)
        self.ok_btn["state"] = "disabled"  # Initially disabled

        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=self.on_cancel)
        cancel_btn.pack(side="left", padx=10)

        self.stop_btn = ttk.Button(btn_frame, text="Stop", command=self.request_stop)
        self.stop_btn.pack(side="left", padx=10)
        self.stop_btn["state"] = "disabled"

        bottom_btn_frame = ttk.Frame(self.root)
        bottom_btn_frame.pack(pady=(5, 15))

        self.check_non_flac_btn = ttk.Button(bottom_btn_frame, text="Check Non-FLAC Files", command=self.check_non_flac_files)
        self.check_non_flac_btn.pack(side="left", padx=5)
        self.check_non_flac_btn["state"] = "disabled"  # Initially disabled

        self.embed_cover_btn = ttk.Button(bottom_btn_frame, text="Fix ALAC Cover Embedding", command=self.on_fix_cover)
        self.embed_cover_btn.pack(side="left", padx=5)
        self.embed_cover_btn["state"] = "disabled"  # Initially disabled

    def browse_input(self):
        folder = filedialog.askdirectory(title="Select FLAC Folder")
        if folder:
            self.input_var.set(folder)

    def browse_output(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_var.set(folder)

    def on_input_change(self, *args):
        try:
            val = self.input_var.get()
            p = Path(val)
            if val and p.exists():
                # Auto set output folder if empty
                if not self.output_var.get():
                    default_output = p.parent / "ALAC"
                    self.output_var.set(str(default_output))

                if not self.stop_requested:
                    self.ok_btn["state"] = "normal"
                    self.embed_cover_btn["state"] = "normal"
                    self.check_non_flac_btn["state"] = "normal"
            else:
                self.ok_btn["state"] = "disabled"
                self.embed_cover_btn["state"] = "disabled"
                self.check_non_flac_btn["state"] = "disabled"
        except Exception:
            self.ok_btn["state"] = "disabled"
            self.embed_cover_btn["state"] = "disabled"
            self.check_non_flac_btn["state"] = "disabled"

    def on_ok(self):
        input_path = Path(self.input_var.get())
        output_text = self.output_var.get().strip()

        if not input_path.exists():
            self.input_entry.configure(background="#ffcccc")
            messagebox.showerror("Error", "Please set a valid FLAC folder.")
            return

        if output_text:
            output_path = Path(output_text)
        else:
            output_path = input_path.parent / "ALAC"
            self.output_var.set(str(output_path))

        self.result["input"] = input_path
        self.result["output"] = output_path

        self.ok_btn["state"] = "disabled"
        self.stop_btn["state"] = "normal"
        self.stop_requested = False

        self.worker_thread = threading.Thread(target=self.process_directory, args=(input_path, output_path), daemon=True)
        self.worker_thread.start()

    def on_cancel(self):
        if self.worker_thread and self.worker_thread.is_alive():
            self.request_stop()
        else:
            self.root.quit()

    def request_stop(self):
        self.stop_requested = True
        self.write_log("[INFO] User requested to stop the process.")

    def convert_flac_to_alac(self, flac_path: Path, alac_path: Path) -> bool:
        alac_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            process = subprocess.run(
                [
                    self.ffmpeg_path, "-y",
                    "-i", str(flac_path),
                    "-map", "0:a:0",
                    "-c:a", "alac",
                    str(alac_path)
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT
            )
            output = process.stdout.decode("utf-8", errors="replace")

            if process.returncode == 0:
                self.write_log(f"SUCCESS: {flac_path.name}")
                return True
            else:
                self.write_log(f"FFMPEG_FAILED: {flac_path.name}")
                self.write_log(output)
                if alac_path.exists():
                    alac_path.unlink()
                return False
        except Exception as e:
            self.write_log(f"ERROR: {flac_path.name} -> {e}")
            if alac_path.exists():
                alac_path.unlink()
            return False

    def determine_relative_path(self, flac_root: Path, flac_file: Path):
        rel = flac_file.relative_to(flac_root)
        if flac_root.name.lower() == "flac":
            return rel
        elif len(rel.parts) >= 2:
            return rel
        else:
            return Path(flac_file.name)

    def process_directory(self, flac_root: Path, alac_root: Path):
        for flac_file in flac_root.rglob("*.flac"):
            if self.stop_requested:
                self.write_log("[INFO] Process stopped by user.")
                break
            try:
                if "ALAC" in flac_file.parts:
                    continue
                rel_path = self.determine_relative_path(flac_root, flac_file)
                alac_file = alac_root / rel_path.with_suffix(".m4a")

                if alac_file.exists() and alac_file.stat().st_mtime >= flac_file.stat().st_mtime:
                    self.write_log(f"SKIPPED (up-to-date): {rel_path}")
                    continue

                success = self.convert_flac_to_alac(flac_file, alac_file)
                if not success:
                    if alac_file.exists():
                        alac_file.unlink()
                    if not any(alac_file.parent.glob("*")):
                        shutil.rmtree(alac_file.parent)
            except Exception as e:
                self.write_log(f"FAILED_TO_PROCESS: {flac_file} -> {e}")

        if self.stop_requested:
            self.root.after(0, lambda: self.on_process_finished(cancelled=True))
        else:
            self.root.after(0, self.on_process_finished)


    def on_process_finished(self, cancelled=False):
        self.stop_btn["state"] = "disabled"
        self.ok_btn["state"] = "normal"
        if cancelled:
            self.write_log("=== Conversion cancelled by user ===")
            messagebox.showinfo("Cancelled", "Conversion was cancelled.")
        else:
            self.write_log("=== FLAC to ALAC conversion finished ===")
            messagebox.showinfo("Done", "FLAC to ALAC conversion process finished.")

    # --- Cover embedding fix section ---

    def on_fix_cover(self):
        self.embed_cover_btn["state"] = "disabled"
        self.stop_btn["state"] = "normal"  # ← Stopボタン有効化
        self.stop_requested = False        # ← フラグ初期化
        threading.Thread(target=self.fix_covers, daemon=True).start()

    def fix_covers(self):
        flac_root = Path(self.input_var.get())
        alac_root = Path(self.output_var.get())
        if not flac_root.exists() or not alac_root.exists():
            messagebox.showerror("Error", "Please correctly set both FLAC and Output folders.")
            self.embed_cover_btn["state"] = "normal"
            self.stop_btn["state"] = "disabled"  # ← 状態戻す
            return

        for flac_file in flac_root.rglob("*.flac"):
            if self.stop_requested:
                self.write_log("[INFO] Cover fix stopped by user.")
                break
            try:
                rel_path = flac_file.relative_to(flac_root)
                alac_file = alac_root / rel_path.with_suffix(".m4a")
                if not alac_file.exists():
                    self.write_log(f"No ALAC file: {alac_file}")
                    continue

                flac_audio = FLAC(flac_file)
                alac_audio = MP4(alac_file)

                if "covr" in alac_audio and alac_audio["covr"]:
                    self.write_log(f"ALAC cover exists: {alac_file}")
                    continue

                if flac_audio.pictures:
                    pic = flac_audio.pictures[0]
                    self.write_log(f"Extracting cover from FLAC: {flac_file}")

                    cover_data = pic.data
                    if pic.mime == "image/jpeg":
                        mp4_cover = MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_JPEG)
                    elif pic.mime == "image/png":
                        mp4_cover = MP4Cover(cover_data, imageformat=MP4Cover.FORMAT_PNG)
                    else:
                        self.write_log(f"Unsupported image format: {pic.mime} {flac_file}")
                        continue

                    alac_audio["covr"] = [mp4_cover]
                    alac_audio.save()
                    self.write_log(f"Cover embedding done: {alac_file}")
                else:
                    self.write_log(f"No embedded cover in FLAC: {flac_file}")

            except Exception as e:
                self.write_log(f"Cover processing error: {flac_file} -> {e}")

        if self.stop_requested:
            messagebox.showinfo("Cancelled", "Cover embedding was cancelled.")
            self.write_log("=== Cover embedding fix cancelled ===")
        else:
            messagebox.showinfo("Done", "Cover embedding fix process finished.")
            self.write_log("=== Cover embedding fix finished ===")

        self.embed_cover_btn["state"] = "normal"
        self.stop_btn["state"] = "disabled"
        self.stop_requested = False

    # --- Check Non-FLAC files ---

    def check_non_flac_files(self):
        flac_root = Path(self.input_var.get())
        if not flac_root.exists():
            messagebox.showerror("Error", "Please set a valid FLAC folder.")
            return

        non_flac_files = []
        for file_path in flac_root.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() != ".flac":
                non_flac_files.append(str(file_path))

        if not non_flac_files:
            messagebox.showinfo("Check Result", "No non-FLAC files found.")
            return

        win = tk.Toplevel(self.root)
        win.title("Non-FLAC Files List")
        win.geometry("600x400")

        frame = ttk.Frame(win)
        frame.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set)
        for file in non_flac_files:
            listbox.insert("end", file)
        listbox.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

def main():
    app = ConverterApp()
    write_log("=== FLAC to ALAC Converter & Cover Embedding Fix Tool started ===")
    app.root.mainloop()
    if app.result["input"] and app.result["output"]:
        write_log(f"Input folder: {app.result['input']}")
        write_log(f"Output folder: {app.result['output']}")
    else:
        write_log("Cancelled or invalid paths")

if __name__ == "__main__":
    main()
