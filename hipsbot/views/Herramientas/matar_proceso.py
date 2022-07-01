import os


def kill_proceso(PID):
    try:
        os.system(f" sudo kill -9  {PID}")
    except Exception:
        print("Ocurrio un problema al matar el proceso")
    return "bien"
            