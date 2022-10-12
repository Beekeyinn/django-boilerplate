import argparse
import json
import secrets
import string


def generate_secret_key(
    chars=string.ascii_letters + string.digits + "!@#$%^&*(-_+)", size=50
):
    return "".join(secrets.choice(chars) for i in range(size))


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--database",
        action="extend",
        nargs="+",
        type=str,
        help="Requires \n database_name \n database_user \n database_password \n database_port \n database_host",
    )
    parser.add_argument(
        "-e",
        "--email",
        action="extend",
        nargs="+",
        type=str,
        help="Requires \n email_address \n password",
    )

    args = parser.parse_args()
    database_name = None
    database_user = None
    database_password = None
    database_port = None
    database_host = None
    email = None
    password = None
    if args.database:
        if len(args.database) != 5:
            print("error parsing arguments")
            return False
        database_name = args.database[0]
        database_user = args.database[1]
        database_password = args.database[2]
        database_port = args.database[3]
        database_host = args.database[4]

    if args.email:
        if len(args.email) != 2:
            print("error parsing the arguments")
            return False

        email = args.email[0]
        password = args.email[1]

    secret_key = generate_secret_key(size=60)

    with open("config.json", "r") as config:
        data = json.load(config)

    with open(".env", "w") as env:
        env.write(f"SECRET_KEY={secret_key}")
        env.write(f"DEPLOYMENT_NAME={config['deployment_name']}")
        env.write(f"DEPLOYMENT_PREFIX={config['deployment_prefix']}")
        env.write(f"CHANNEL={config['channel']}")
        env.write(f"PRODUCTION={config['production']}")
        env.write(f"DB_NAME={database_name}")
        env.write(f"DB_USERNAME={database_user}")
        env.write(f"DB_PASSWORD={database_password}")
        env.write(f"DB_PORT={database_port}")
        env.write(f"DB_HOST={database_host}")
        env.write(f"EMAIL_HOST_USER={email}")
        env.write(f"EMAIL_USER_PASSWORD={password}")
        env.write(f"DEFAULT_FROM_EMAIL={email}")
    print("Environment file generated")


if __name__ == "main":
    parser()
