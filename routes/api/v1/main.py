def main():
    import bpy
    initArgs()
    print('Hello world!')


def initArgs():
    pass
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--taskname')
    args = parser.parse_args()
    if args.taskname:
        print('Taskname on')
    else:
        print('Taskname off, please try again')
        sys.exit()






if __name__ == "__main__":
    main()
