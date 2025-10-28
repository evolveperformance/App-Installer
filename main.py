import asyncio
import aiohttp
import os
import time
from pathlib import Path
from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

console = Console()

# ============================================================
# 🧩 ULTRON APP DATABASE
# ============================================================
apps = {
    # 🧭 Browsers
    "Brave": ("https://github.com/Lukefn123/Apps/releases/download/v1/BraveInstaller.exe", "Browsers"),
    "Chrome": ("https://github.com/Lukefn123/Apps/releases/download/v1/ChromeInstaller.exe", "Browsers"),
    "Firefox Installer": ("https://github.com/Lukefn123/Apps/releases/download/v1/Firefox.Installer.exe", "Browsers"),
    "Thorium": ("https://github.com/Alex313031/Thorium-Win/releases/download/M130.0.6723.174/thorium_SSE3_mini_installer.exe", "Browsers"),
    "Zen": ("https://github.com/Lukefn123/Apps/releases/download/v1/zen.installer.exe", "Browsers"),

    # ⚙️ System Tools
    "Affinity Tool": ("https://github.com/Lukefn123/GRAB/releases/download/v1/Affinity.Tool.exe", "System Tools"),
    "Autoruns": ("https://github.com/Lukefn123/Apps/releases/download/v1/Autoruns.exe", "System Tools"),
    "GPU-Z": ("https://github.com/Lukefn123/Apps/releases/download/v1/GPU-Z.2.53.0.exe", "System Tools"),
    "HWINFO64": ("https://github.com/Lukefn123/Apps/releases/download/v1/HWINFO64.exe", "System Tools"),
    "MSI Util": ("https://github.com/Lukefn123/GRAB/releases/download/v1/MSI_util_v3.exe", "System Tools"),
    "Nvclean": ("https://github.com/Lukefn123/GRAB/releases/download/v1/NVCleanstall.exe", "System Tools"),
    "Onboard Memory Manager": ("https://github.com/Lukefn123/Apps/releases/download/v1/OnboardMemoryManager.exe", "System Tools"),
    "ProcExplorer": ("https://github.com/Lukefn123/GRAB/releases/download/v1/procexp64.exe", "System Tools"),

    # 🔥 Overclocking
    "AIDA64 Extreme": ("https://github.com/Lukefn123/Apps/releases/download/v1/aida64extreme770.exe", "Overclocking"),
    "Asrock Timing Config": ("https://github.com/Lukefn123/Apps/releases/download/v1/AsrTCSetupv4.0.16.exe", "Overclocking"),
    "Memory Cleaner": ("https://github.com/Lukefn123/Apps/releases/download/v1/Memory.Cleaner.exe", "Overclocking"),
    "Memtest Vulkan": ("https://github.com/Lukefn123/Apps/releases/download/v1/memtest_vulkan-v0.5.0.exe", "Overclocking"),
    "MemTweakIt": ("https://github.com/Lukefn123/Apps/releases/download/v1/MemTweakIt.exe", "Overclocking"),
    "MLC": ("https://github.com/Lukefn123/Apps/releases/download/v1/mlc.exe", "Overclocking"),
    "More Power Tool": ("https://github.com/Lukefn123/Apps/releases/download/v1/MorePowerTool_Setup.exe", "Overclocking"),
    "OCCT": ("https://github.com/Lukefn123/Apps/releases/download/v1/OCCT.exe", "Overclocking"),
    "TestMem5": ("https://github.com/Lukefn123/Apps/releases/download/v1/TestMem5.zip", "Overclocking"),
    "YCruncher": ("https://github.com/Lukefn123/Apps/releases/download/v1/Y.Cruncher.zip", "Overclocking"),

    # 🎮 Gaming
    "Discord": ("https://github.com/Lukefn123/Apps/releases/download/v1/DiscordInstaller.exe", "Gaming"),
    "Epic Games": ("https://github.com/Lukefn123/Apps/releases/download/v1/EpicInstaller.msi", "Gaming"),
    "Steam": ("https://github.com/Lukefn123/Apps/releases/download/v1/SteamInstaller.exe", "Gaming"),
    "Valorant": ("https://github.com/Lukefn123/Apps/releases/download/v1/ValorantInstaller.exe", "Gaming"),

    # 🧰 Utilities
    "App Uninstaller": ("https://github.com/Lukefn123/GRAB/releases/download/v1/geek.exe", "Utilities"),
    "MPC Media Player": ("https://github.com/clsid2/mpc-hc/releases/download/2.5.1/MPC-HC.2.5.1.x64.exe", "Utilities"),
    "LightShot": ("https://github.com/Lukefn123/Apps/releases/download/v1/setup-lightshot.exe", "Utilities"),
    "ShareX": ("https://github.com/ShareX/ShareX/releases/download/v18.0.1/ShareX-18.0.1-setup.exe", "Utilities"),
    "MSI AfterBurner": ("https://github.com/Lukefn123/GRAB/releases/download/v1/MSIAfterburnerInstaller466Beta5.exe", "Utilities"),
    "OBS Studio": ("https://github.com/obsproject/obs-studio/releases/download/27.2.4/OBS-Studio-27.2.4-Full-Installer-x64.exe", "Utilities"),
    "Spotify": ("https://github.com/Lukefn123/Apps/releases/download/v1/SpotifyInstaller.exe", "Utilities"),
    "Visual Studio": ("https://github.com/Lukefn123/Apps/releases/download/v1/VisualStudioInstaller.exe", "Utilities"),
}

categories = ["Browsers", "System Tools", "Overclocking", "Gaming", "Utilities"]
selected_apps = set()
app_order = []


def boot_animation():
    console.clear()
    console.print("[bold magenta]Initializing ULTRON OS...[/bold magenta]")
    for _ in range(3):
        console.print(".", end="", style="cyan")
        time.sleep(0.5)
    console.print("\n[bold green]System Ready.[/bold green]")
    time.sleep(0.8)
    console.clear()


def show_logo():
    logo = r"""
██╗   ██╗██╗     ████████╗██████╗  ██████╗ ███╗   ██╗
██║   ██║██║     ╚══██╔══╝██╔══██╗██╔═══██╗████╗  ██║
██║   ██║██║        ██║   ██████╔╝██║   ██║██╔██╗ ██║
╚██╗ ██╔╝██║        ██║   ██╔══██╗██║   ██║██║╚██╗██║
 ╚████╔╝ ███████╗   ██║   ██║  ██║╚██████╔╝██║ ╚████║
  ╚═══╝  ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
"""
    console.print(Panel.fit(logo, style="bold magenta"))
    console.print("[bold cyan]Welcome to the Ultron App Installer[/bold cyan]\n")


def build_app_order():
    grouped = {}
    for name, (_, cat) in apps.items():
        grouped.setdefault(cat, []).append(name)
    for cat in categories:
        if cat in grouped:
            app_order.extend(sorted(grouped[cat]))
    for other in sorted(set(grouped) - set(categories)):
        app_order.extend(sorted(grouped[other]))


def display_apps():
    console.clear()
    show_logo()

    grouped = {}
    for name, (_, cat) in apps.items():
        grouped.setdefault(cat, []).append(name)

    panels = []
    i = 1
    for cat in categories:
        if cat not in grouped:
            continue
        table = Table(show_header=False, box=None, pad_edge=False)
        for app in sorted(grouped[cat]):
            mark = "[green]✓[/green]" if app in selected_apps else "[red]✗[/red]"
            table.add_row(f"[cyan]{i:2})[/cyan] {mark} [white]{app}[/white]")
            i += 1
        panels.append(Panel(table, title=f"[bold cyan]{cat}[/bold cyan]", border_style="magenta"))

    grid = Group(*panels)
    console.print(grid)
    console.print(
        "\n[cyan][S][/cyan] Select all   [cyan][C][/cyan] Clear all   [cyan][D][/cyan] Download   [cyan][E][/cyan] Exit\n"
    )


async def download_file(session, url, path):
    async with session.get(url) as response:
        response.raise_for_status()
        total = int(response.headers.get("Content-Length", 0))
        with open(path, "wb") as f:
            with Progress() as progress:
                task = progress.add_task(f"Downloading {path.name}", total=total or 1)
                async for chunk in response.content.iter_chunked(8192):
                    f.write(chunk)
                    progress.update(task, advance=len(chunk))


async def download_selected():
    if not selected_apps:
        console.print("[yellow]No apps selected. Press Enter to continue...[/yellow]")
        input()
        return

    download_dir = Path.home() / "Downloads"
    download_dir.mkdir(parents=True, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        for app in selected_apps:
            url = apps[app][0]
            filename = Path(url).name
            target = download_dir / filename
            try:
                await download_file(session, url, target)
                console.print(f"[green]{app} downloaded successfully.[/green]")
            except Exception as e:
                console.print(f"[red]Error downloading {app}: {e}[/red]")

    console.print("\n[bold green]All downloads complete. Press Enter to continue...[/bold green]")
    input()


async def main():
    boot_animation()
    build_app_order()
    while True:
        display_apps()
        choice = input("> ").strip().upper()
        if choice == "E":
            break
        elif choice == "S":
            selected_apps.update(app_order)
        elif choice == "C":
            selected_apps.clear()
        elif choice == "D":
            await download_selected()
        elif choice.isdigit():
            index = int(choice)
            if 1 <= index <= len(app_order):
                app = app_order[index - 1]
                if app in selected_apps:
                    selected_apps.remove(app)
                else:
                    selected_apps.add(app)


if __name__ == "__main__":
    asyncio.run(main())
