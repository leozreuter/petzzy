import subprocess
import time

def check_postgres(container="postgres-dev", host="localhost", retry_delay=1):
    print("\n🏃💨 Waiting PgSQL is ready for connections...", end="", flush=True)

    while True:
        try:
            result = subprocess.run(
                ["docker", "exec", container, "pg_isready", "--host", host],
                capture_output=True,
                text=True,
            )

            if "accepting connections" in result.stdout:
                print("\n🎯 PgSQL is ready!\n")
                break
            else:
                print(".", end="", flush=True)

        except subprocess.CalledProcessError as e:
            print(f"\n❌ Error running pg_isready: {e}")
            time.sleep(retry_delay)

        time.sleep(retry_delay)

if __name__ == "__main__":
    check_postgres()
