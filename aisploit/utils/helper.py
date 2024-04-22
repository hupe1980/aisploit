def is_running_in_jupyter_notebook() -> bool:
    try:
        import IPython

        if IPython.get_ipython():
            return True
        else:
            return False
    except ImportError:
        return False
