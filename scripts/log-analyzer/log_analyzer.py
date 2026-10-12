import argparse

def analyze_log(filename):
    failed_logins = {}
    try:
        with open(filename,"r") as file:
            for line in file:
                linea = line.strip()
                if not linea:
                    continue
                parts = line.split()
                if len(parts) != 3:
                    continue
                ip = parts[0]
                event = parts[1]
                user = parts[2]
                if event == "LOGIN_FAILED":
                    if ip in failed_logins:
                        failed_logins[ip] += 1
                    else:
                        failed_logins[ip] = 1
        return failed_logins
    except FileNotFoundError:
        return None

def show_alerts(failed_logins, threshold):
    for ip, attempts in failed_logins.items():
        if attempts >= threshold:
            print(f"{ip} -> {attempts} login falliti -> ALERT")
        elif attempts == 1:
            print(f"{ip} -> {attempts} login fallito")
        else:
            print(f"{ip} -> {attempts} login falliti")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description = "Analizza un log e rileva login falliti"
    )

    parser.add_argument(
        "filename",
        help = "File di log da analizzare"
    )

    parser.add_argument(
        "--threshold",
        type = int,
        default = 3,
        help = "Numero di login falliti necessario per generare un alert"
    )

    args = parser.parse_args()

    failed_logins = analyze_log(args.filename)

    if failed_logins is not None:
        show_alerts(failed_logins, args.threshold)
    else:
        print(f"Errore: file '{args.filename}' non trovato")




