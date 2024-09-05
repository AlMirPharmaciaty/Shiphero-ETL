import subprocess

from config.settings import AUTH_TOKEN


if __name__ == "__main__":
    command = [
        "py", "-m", "sgqlc.introspection",
        "--exclude-deprecated",
        "--exclude-description",
        "-H", f"Authorization: Bearer {AUTH_TOKEN}",
        "https://public-api.shiphero.com/graphql",
        "config/shiphero_schema.json"
    ]
    command_two = ["sgqlc-codegen", "schema",
                   "config/shiphero_schema.json", "config/shiphero_schema.py"]
    try:
        subprocess.run(command, check=True)
        subprocess.run(command_two, check=True)
        print("Schema generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
