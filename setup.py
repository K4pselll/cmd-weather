import os
import sys
import ctypes

try:
    import winreg
except ImportError:
    winreg = None

SCRIPT_NAME = os.path.basename(__file__)


def normalize_path(path: str) -> str:
    if not path:
        return ""
    return os.path.normcase(os.path.normpath(path.strip().rstrip("\\")))


def get_user_path() -> str:
    if winreg is None:
        raise RuntimeError("Windows registry support is required for this script.")
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_READ) as key:
        try:
            value, _ = winreg.QueryValueEx(key, "PATH")
            return value
        except FileNotFoundError:
            return ""


def set_user_path(path: str) -> None:
    if winreg is None:
        raise RuntimeError("Windows registry support is required for this script.")
    with winreg.CreateKey(winreg.HKEY_CURRENT_USER, r"Environment") as key:
        winreg.SetValueEx(key, "PATH", 0, winreg.REG_EXPAND_SZ, path)


def broadcast_environment_change() -> None:
    HWND_BROADCAST = 0xFFFF
    WM_SETTINGCHANGE = 0x001A
    SMTO_ABORTIFHUNG = 0x0002
    result = ctypes.c_ulong()
    ctypes.windll.user32.SendMessageTimeoutW(
        HWND_BROADCAST,
        WM_SETTINGCHANGE,
        0,
        "Environment",
        SMTO_ABORTIFHUNG,
        5000,
        ctypes.byref(result),
    )


def create_wrapper(wrapper_name: str) -> None:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    wrapper_path = os.path.join(script_dir, wrapper_name)
    if os.path.exists(wrapper_path):
        print(f"Wrapper already exists: {wrapper_path}")
        return

    python_launcher = "py" if sys.platform == "win32" else "python"
    content = f"@echo off\n{python_launcher} \"%~dp0\\Main.py\" %*\n"

    with open(wrapper_path, "w", encoding="utf-8") as wrapper_file:
        wrapper_file.write(content)

    print(f"Created command wrapper: {wrapper_path}")


def select_wrapper_name() -> str:
    name = input("Name the command to run Terminal weather (leave blank for default 'weather'): ").strip()
    if not name:
        name = "weather"
    if not name.lower().endswith(".cmd"):
        name += ".cmd"
    return name


def install() -> None:
    script_dir = os.path.abspath(os.path.dirname(__file__))
    current_dir_normalized = normalize_path(script_dir)
    existing_path = get_user_path()
    existing_paths = [normalize_path(p) for p in existing_path.split(";") if p.strip()]

    if current_dir_normalized in existing_paths:
        print(f"This folder is already in PATH: {script_dir}")
    else:
        new_path = existing_path.rstrip(";")
        if new_path:
            new_path += ";"
        new_path += script_dir
        set_user_path(new_path)
        os.environ["PATH"] = new_path
        broadcast_environment_change()
        print(f"Added folder to user PATH: {script_dir}")

    wrapper_name = select_wrapper_name()
    create_wrapper(wrapper_name)
    print("Installation complete. Open a new command prompt to use the new PATH setting.")


def main() -> int:
    if sys.platform != "win32":
        print("This setup script is designed for Windows.")
        return 1

    args = sys.argv[1:]
    if args and args[0] in {"-h", "--help"}:
        print(f"Usage: python {SCRIPT_NAME}\nInstalls the current project folder into your user PATH.")
        return 0

    install()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
