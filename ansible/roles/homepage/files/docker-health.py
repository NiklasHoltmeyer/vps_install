#!/usr/bin/env python3
import json
import os
import subprocess
import sys
import tempfile
from datetime import datetime, timezone


def collect_status():
    result = subprocess.run(
        ["docker", "ps", "-a", "--format", "{{.Names}}\t{{.State}}\t{{.Status}}"],
        capture_output=True,
        text=True,
        check=False,
    )

    if result.returncode != 0:
        return {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "total": 0,
            "running": 0,
            "healthy": 0,
            "problems": 1,
            "problem_containers": [
                {"name": "Docker", "status": "Status konnte nicht gelesen werden"}
            ],
        }

    containers = []
    for line in result.stdout.splitlines():
        if not line.strip():
            continue

        name, state, status = (line.split("\t", 2) + ["", ""])[:3]
        state = state.lower()

        if "(unhealthy)" in status:
            health = "unhealthy"
        elif "(healthy)" in status:
            health = "healthy"
        elif "(health: starting)" in status:
            health = "starting"
        else:
            health = "none"

        containers.append(
            {
                "name": name,
                "state": state,
                "status": status,
                "health": health,
            }
        )

    problems = [
        {"name": item["name"], "status": item["status"]}
        for item in containers
        if item["state"] != "running" or item["health"] == "unhealthy"
    ]

    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "total": len(containers),
        "running": sum(item["state"] == "running" for item in containers),
        "healthy": sum(item["health"] == "healthy" for item in containers),
        "problems": len(problems),
        "problem_containers": problems,
    }


def atomic_write(path, data):
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)

    fd, temporary = tempfile.mkstemp(prefix="status-", suffix=".json", dir=directory)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.chmod(temporary, 0o644)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)


def main():
    if len(sys.argv) != 2:
        raise SystemExit("usage: homepage-docker-health OUTPUT")

    atomic_write(sys.argv[1], collect_status())


if __name__ == "__main__":
    main()
