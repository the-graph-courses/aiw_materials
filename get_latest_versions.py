import requests
import packaging.version as pv


def latest_stable(package: str, *, timeout=3) -> str:
    """Return the newest *non-pre*, *non-yanked* version on PyPI."""
    url = f"https://pypi.org/pypi/{package}/json"
    data = requests.get(url, timeout=timeout).json()
    versions = [
        v
        for v, files in data["releases"].items()
        if files  # skip empty yanks
        and not pv.parse(v).is_prerelease  # drop 1.0.0rc1 …
        and not files[0].get("yanked", False)  # drop yanked tags
    ]
    return str(max(map(pv.parse, versions)))  # newest wins


packages = ["plotly", "pandas", "jupyter", "ipykernel", "itables"]

print("Latest stable versions:")
for package in packages:
    version = latest_stable(package)
    print(f"{package}=={version}")
