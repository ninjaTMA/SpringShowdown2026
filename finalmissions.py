from pybricks.tools import hub_menu

# Menu to choose a launch to run
selected = hub_menu("1", "2", "3", "4", "5", "6", "7")

# Based on the selection, run a launch module
if selected == "1":
    import launches.launch1  # noqa: F401
elif selected == "2":
    import launches.launch2  # noqa: F401
