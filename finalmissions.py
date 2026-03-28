from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu("1", "2", "3", "4", "5", "6", "7")

# Based on the selection, run a program.
if selected == "1":
    import m1
elif selected == "2":
    import m2

