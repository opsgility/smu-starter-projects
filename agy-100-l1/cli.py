import argparse


def main() -> None:
    parser = argparse.ArgumentParser(prog="meridian-cli", description="Meridian Devworks logistics CLI")
    parser.add_argument("--inspect", type=str, help="Inspect a shipment by tracking number")
    args = parser.parse_args()
    if args.inspect:
        print(f"[meridian-cli] inspecting shipment {args.inspect}")


if __name__ == "__main__":
    main()
