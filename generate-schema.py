import subprocess

with open('token.txt', 'r', encoding='utf-8') as f:
    AUTH_TOKEN = f.read()


if __name__ == "__main__":
    command = [
        "py", "-m", "sgqlc.introspection",
        "--exclude-deprecated",
        "--exclude-description",
        "-H", f"Authorization: Bearer {AUTH_TOKEN}",
        "https://public-api.shiphero.com/graphql",
        "schema.json"
    ]
    command_two = ["sgqlc-codegen", "schema", "schema.json", "schema.py"]
    try:
        subprocess.run(command, check=True)
        subprocess.run(command_two, check=True)
        print("Schema generated successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")
