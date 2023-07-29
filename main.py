from dotenv import load_dotenv

from frontend import ProgramPainel

load_dotenv()


def main():
    run_prog = ProgramPainel()
    run_prog.startProgram()


main()
