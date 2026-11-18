#!/usr/bin/env python3
import json
import os
import time
from datetime import datetime


def get_uptime():
    with open("/proc/uptime", "r") as f:
        return float(f.readline().split()[0])


def get_loadavg():
    with open("/proc/loadavg", "r") as f:
        parts = f.readline().split()
        return {
            "load_1m": float(parts[0]),
            "load_5m": float(parts[1]),
            "load_15m": float(parts[2]),
        }


def get_meminfo():
    mem = {}
    with open("/proc/meminfo", "r") as f:
        for line in f:
            parts = line.split()
            key = parts[0].rstrip(":")
            if key in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
                mem[key] = int(parts[1])  # в килобайтах
    mem_used_kb = mem["MemTotal"] - mem["MemAvailable"]
    return {
        "mem_total_kb": mem["MemTotal"],
        "mem_used_kb": mem_used_kb,
        "mem_used_percent": round((mem_used_kb / mem["MemTotal"]) * 100, 2),
    }


def get_disk_root():
    stat = os.statvfs("/")
    total = stat.f_blocks * stat.f_frsize
    free = stat.f_bfree * stat.f_frsize
    used = total - free
    return {
        "disk_root_used_percent": round((used / total) * 100, 2)
    }


def main():
    now = datetime.now()
    log_filename = now.strftime("%y-%m-%d-awesome-monitoring.log")
    log_path = os.path.join("/var/log", log_filename)

    metrics = {
        "timestamp": int(time.time()),
        "uptime_sec": get_uptime(),
    }
    metrics.update(get_loadavg())
    metrics.update(get_meminfo())
    metrics.update(get_disk_root())

    with open(log_path, "a", encoding="utf-8") as log_file:
        log_file.write(json.dumps(metrics) + "\n")


if __name__ == "__main__":
    main()
