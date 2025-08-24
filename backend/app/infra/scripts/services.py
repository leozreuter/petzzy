import subprocess

def up():
    subprocess.run("docker compose -f app/infra/compose.yaml up -d", shell=True)

def down():
    subprocess.run("docker compose -f app/infra/compose.yaml down -v", shell=True)
