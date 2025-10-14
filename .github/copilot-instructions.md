## CARLA (UE4) — Quick instructions for AI coding agents

This file contains the concentrated, repository-specific knowledge an automated coding agent needs to be productive in this codebase.
Be concrete and conservative: only use and change files referenced here, and validate builds/tests after edits.

### Big-picture architecture (short)
- Two primary pieces: the Unreal Engine project (Unreal/CarlaUE4) that contains the simulator and assets, and the native C++ library + build system under `LibCarla` / `Build` that exposes the runtime. The Python client lives under `PythonAPI/carla` and is packaged as a wheel for test/dev usage.
- The project separates code and content: large assets live in `Unreal/CarlaUE4/Content/Carla` (maps, vehicles, blueprints). Code and engine integration live in `Unreal/CarlaUE4/` (plugins, C++ code) and `LibCarla/`.
- High level flow: C++/Unreal server runs the simulator => communicates via CARLA RPC & streaming ports => PythonAPI (wheel) connects to control agents and tests.

### Key files & directories to reference when making changes
- `Makefile` (repo root) — canonical developer commands (`make PythonAPI`, `make launch`, `make package`, `make help`).
- `Unreal/CarlaUE4/` — Unreal project, blueprints, and content. Example map file: `Unreal/CarlaUE4/Content/Carla/Maps/OpenDrive/Town01.xodr`.
- `PythonAPI/carla` — Python client, examples, tests (`PythonAPI/test/smoke`). Build output: `PythonAPI/carla/dist`.
- `LibCarla/` — C++ library used by the Python client and other components.
- `Build/` — toolchain and bootstrap assets used during builds (custom toolchains, boost archives).
- `Util/ContentVersions.txt` — references to content/archive versions and download links.
- `.github/workflows/` — CI pipelines. See `ue4_dev.yml` and `_ci-ubuntu.yml` for CI specifics and environment requirements.

### Developer workflows (concrete commands & gotchas)
- Set required environment variables before builds:
  - `export UE4_ROOT=~/UnrealEngine_4.26` (path to CARLA fork of UE4)
  - `export CARLA_UE4_ROOT=/path/to/carla` (root of this repo)
- Build steps (Linux):
  - Build UE4 (one-time): `./Setup.sh && ./GenerateProjectFiles.sh && make` inside your cloned UnrealEngine fork. Do NOT use `make -j$(nproc)` (can break the build).
  - Download content: either `./Update.sh` (automated) or `git clone -b master https://bitbucket.org/carla-simulator/carla-content ${CARLA_UE4_ROOT}/Unreal/CarlaUE4/Content/Carla`.
  - Build Python client: `python3 -m pip install --upgrade -r ${CARLA_UE4_ROOT}/PythonAPI/carla/requirements.txt` then `make PythonAPI`.
  - Launch editor/server: `make launch` (uses UE4Editor to open the project). First launch may be slow due to shader compilation.
  - Package for tests/CI: `make package` → run packaged server from `./Dist/CARLA_<id>/LinuxNoEditor/CarlaUE4.sh` with flags for headless/testing.

### Tests and examples
- Smoke tests: `make smoke_tests ARGS="--xml --python-version=<python_version> --target-wheel-platform=manylinux_2_31_x86_64"` — ensure you run the packaged server before.
- Example scripts: `PythonAPI/examples/generate_traffic.py`, `dynamic_weather.py`. Typical run: start simulator, then `python3 generate_traffic.py`.

### Project-specific conventions and pitfalls
- Very large repo and heavy builds: expect ~130GB free disk and long build times (UE4 + CARLA). Prefer editing & testing small units (PythonAPI) locally and run full builds in CI or dedicated build host.
- Python wheel build matters: the Python API is consumed via generated wheel in `PythonAPI/carla/dist`. Use virtualenvs when installing/ testing wheels to avoid version conflicts.
- Numpy >= 2.0 is known to break C++/Boost build steps. If encountering Boost/Python errors, check `python3 -m pip show numpy` and prefer `numpy<2.0` for build environments.
- Keep code/content separate: do not commit large asset files into the main repo; content is typically managed through `Update.sh` or the separate `carla-content` repository.

### Integration points & external dependencies
- Unreal Engine fork: must be cloned from `CarlaUnreal/UnrealEngine` with a GitHub account authorized by Epic Games.
- External content repo: `bitbucket.org/carla-simulator/carla-content` or downloaded archives referenced in `Util/ContentVersions.txt`.
- CI: `.github/workflows` encodes build matrixes for Ubuntu/Windows and artifact packaging. Look at `_ci-ubuntu.yml` for Linux toolchain details.

### Concrete examples for code edits and validations
- If you change Python API signatures: update `PythonAPI/carla`, run `make PythonAPI`, and run `PythonAPI/test/smoke` tests against a packaged server.
- If you touch C++/LibCarla: run `make package` then run smoke tests in a packaged server. Use `make rebuild` to clean and relaunch when uncertain.

### Safety and verification steps for agents
- Run `make help` first to discover available targets. Prefer `make PythonAPI` for fast iteration on Python changes.
- After edits, run quick Python smoke tests before larger packages. If packaging is needed, run `make package` and the smoke tests as described above.

### Where to look for more context
- Top-level: `README.md` and `Docs/build_linux.md` (contains detailed commands and edge cases).
- Tests & examples: `PythonAPI/examples/`, `PythonAPI/test/`.
- CI workflows: `.github/workflows/*`.

If any section is unclear or missing (for example, a new custom CI matrix or an internal developer script), tell me what area you want expanded and I'll iterate.
