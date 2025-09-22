import streamlit as st
import sys
import os
import subprocess
import socket
import time
import webbrowser
import platform
from pathlib import Path

def run_streamlit_commands(port=None, open_browser=True, timeout=10):
    """
    Launch a Streamlit server for this file in the current Python environment.

    - port: int or None. If None, finds a free port.
    - open_browser: whether to open the default browser to the app URL.
    - timeout: seconds to wait for the server to become responsive.

    This function spawns a detached subprocess so the caller doesn't block.
    """
    # If we're already running inside Streamlit's runner/reloader, don't re-launch.
    # Streamlit sets STREAMLIT_RUN_MAIN (and other envs). Also check a custom flag
    # we set on the spawned process so the child doesn't try to relaunch the server.
    if (
        os.environ.get("STREAMLIT_RUN_MAIN")
        or os.environ.get("_NKC_STREAMLIT_LAUNCHED") == "1"
        or any("streamlit" in str(a).lower() for a in sys.argv)
    ):
        return

    # Determine the file to run (this file)
    script_path = os.path.abspath(__file__)

    # Find a free port if none provided
    if port is None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            port = s.getsockname()[1]

    cmd = [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        script_path,
        "--server.port",
        str(port),
        "--server.headless",
        "true",
    ]

    env = os.environ.copy()
    # Ensure Streamlit doesn't try to open its own browser (we control it)
    env["BROWSER"] = "false"
    # Mark the child process so it knows it was launched by this helper and won't
    # try to re-launch Streamlit itself (prevents duplicate launches / browser tabs).
    env["_NKC_STREAMLIT_LAUNCHED"] = "1"

    creationflags = 0
    preexec_fn = None
    if platform.system() == "Windows":
        # CREATE_NEW_CONSOLE = 0x00000010, use DETACHED_PROCESS to avoid console window reuse
        # NOTE: I get a linter error here but it works fine when run. Ignore the error.
        creationflags = subprocess.CREATE_NEW_CONSOLE
    else:
        # Detach process group on POSIX so it keeps running after this process exits
        preexec_fn = os.setsid

    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            env=env,
            creationflags=creationflags,
            preexec_fn=preexec_fn,
            close_fds=True,
        )
    except Exception as e:
        raise RuntimeError(f"Failed to start Streamlit: {e}")

    url = f"http://localhost:{port}"

    # Wait for server to be responsive
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            # simple socket connect to check
            with socket.create_connection(("127.0.0.1", port), timeout=1):
                if open_browser:
                    try:
                        webbrowser.open_new_tab(url)
                    except Exception:
                        pass
                return proc  # return the subprocess handle
        except OSError:
            time.sleep(0.2)

    # If we reach here, server didn't start in time
    raise TimeoutError(f"Streamlit server did not start within {timeout} seconds on port {port}")

def interface_for_annual_import():
    changemaker_logo = Path(__file__).resolve().parent.parent / "Images" / "FullLogo_Transparent.png"
    nkco_logo = Path(__file__).resolve().parent.parent / "Images" / "no_kill_co_logo.png"

    # Layout: left image | centered title | right image
    cols = st.columns([1, 2, 1])
    with cols[0]:
        st.image(str(changemaker_logo), use_container_width=True)
    with cols[1]:
        # center the title in the middle column
        st.markdown("<h1 style='text-align:center; margin: 0;'>Annual Data Import Interface</h1>", unsafe_allow_html=True)
    with cols[2]:
        st.image(str(nkco_logo), use_container_width=True)

    st.write("This interface allows users to import annual data files.")
    data_year = st.text_input("Enter the year of data you are loadeing (e.g., 2023):", key="data_year")
    st.write("Drag and drop a CSV or Excel containing annual data below.")
    year_file = st.file_uploader("Choose a CSV file", key="year_file", type=["csv", "xlsx","xls"])
    st.write("Drag and drop a CSV or Excel containing the current PACFA data here.")
    pacfa_file = st.file_uploader("Choose a CSV file", key="pacfa_file", type=["csv", "xlsx","xls"])
    if year_file is not None and pacfa_file is not None and data_year:
        st.write("File uploaded successfully!")
        # Here you can add code to process the uploaded file
        # For example, read it into a pandas DataFrame

        return data_year, year_file, pacfa_file
    else:
        st.write("Waiting for file upload and year input...")

if __name__ == "__main__":  
    run_streamlit_commands(port=8501, open_browser=True, timeout=10) 
    interface_for_annual_import()
    print("Uploads complete.")