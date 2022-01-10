"""An app for tracking healthcare events and insurance costs.
Used to compare my Insurance options with ExtensisHR for 2022."""



'''
Two modes:
track
    loads history from peristent storage
    add and evaluate new expenses
    save back to persistent storage

compare
    load several plan options
    load a calendar of expected healthcare services
    compare costs between plans


'''
import argparse

version = '0.0.10'

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [OPTION] [MODE]...",
        description="An app for tracking healthcare events and insurance costs."
    )
    parser.add_argument(
        "-v", "--version", action="version",
        version = f"Insurance Tracker version {version}"
    )
    parser.add_argument("-m", "--mode",nargs=1)
    parser.add_argument("-p", "--plan-definition",nargs=1)
    parser.add_argument('--output-dir', nargs=1)

    return parser.parse_args()

def get_mode(mode):
    if mode and mode[0].lower() == 'compare':
        return 'compare'
    else:
        return 'track'



def main():
    args = init_argparse()
    mode = get_mode(args.mode)
    print(mode)



if __name__ == '__main__':
    main()