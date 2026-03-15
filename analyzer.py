import subprocess
import hashlib
import re


def run(cmd):

    try:
        return subprocess.check_output(cmd, shell=True).decode(errors="ignore")
    except:
        return ""


def extract_ips(text):

    return re.findall(r"(?:\d{1,3}\.){3}\d{1,3}", text)


def extract_domains(text):

    return re.findall(r"[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)


def analyze_file(path):

    report = []

    # hash
    with open(path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()

    report.append(f"SHA256: {sha}")

    # file type
    report.append(run(f"file {path}"))

    # metadata
    report.append(run(f"exiftool {path}")[:1500])

    # strings
    strings = run(f"strings {path}")[:2000]
    report.append(strings)

    # ip extraction
    ips = extract_ips(strings)

    if ips:
        report.append("IPs found:\n" + "\n".join(set(ips)))

    # domains
    domains = extract_domains(strings)

    if domains:
        report.append("Domains:\n" + "\n".join(set(domains)))

    # binwalk
    report.append(run(f"binwalk {path}")[:800])

    return "\n\n".join(report)
