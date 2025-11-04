def parse_input(user_input):
    if len(user_input.strip()) == 0:
        return ("",)
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
