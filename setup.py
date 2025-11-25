from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="search_engine",
    version="1.0.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "run-crawler=run_crawler:main",
            "run-indexer=run_indexer:main",
            "run-processor=run_processor:main",
        ],
    },
    python_requires=">=3.12",
)