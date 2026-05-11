class MenuActionsSignals:
    """
    Contain set of static variables to store all menu signals. It allows to simplyfy signaling structure.
    By this approch, repeating signals in QMenuBar and QMenu is not necessarry.
    """

    SHOW_START_DISPLAY = "show_start_display"
    EXIT_APP = "exit_app"
    ABOUT_APP = "about_app"
