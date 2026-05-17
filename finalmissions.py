from pybricks.tools import hub_menu

# Make a menu to choose a letter. You can also use numbers.
selected = hub_menu("1", "2", "3", "4", "5", "6")

# Based on the selection, run a program.
if selected == "1":
    import m1
elif selected == "2":
    import m2
elif selected == "3":
    import m3
elif selected == "4":
    import m4
elif selected == "5":
    import m5
elif selected == "6":
    import m6new

