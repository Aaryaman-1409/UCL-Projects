from pathlib import Path
from abc import ABC, abstractmethod
import subprocess
import shutil
import sys


class Build(ABC):
    def __init__(self):
        self.src_dir = Path(__file__).parent / "src"
        self.release_dir = Path(__file__).parent / "release"
        super().__init__()

    @abstractmethod
    def preBuild(self):
        raise NotImplementedError

    @abstractmethod
    def build(self):
        raise NotImplementedError

    @abstractmethod
    def postBuild(self):
        raise NotImplementedError

    @abstractmethod
    def fullBuild(self):
        raise NotImplementedError


class MotionInput(Build):
    def __init__(self) -> None:
        super().__init__()
        self.dir = self.src_dir / "MI_v3.2"
        self.build_dir = self.dir / "Release" / "motioninput_api.dist"
        self.dest_dir = self.release_dir / "MotionInput"

    def preBuild(self):
        print("Installing requirements..")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=self.dir,
            shell=True,
        )

    def build(self):
        print("Starting build..")
        subprocess.run(
            [sys.executable, "build.py", "motioninput_api.py"], cwd=self.dir, shell=True
        )

    def postBuild(self):
        print("Copying build files to final destination...")

        try:
            shutil.rmtree(str(self.dest_dir))
        except OSError:
            pass

        shutil.copytree(str(self.build_dir), str(self.dest_dir))

        print("Copied build files to final destination")

    def fullBuild(self):
        self.preBuild()
        self.build()
        self.postBuild()


class MotionInputServer(Build):
    def __init__(self) -> None:
        super().__init__()
        self.dir = self.src_dir / "motion-input-server"
        self.build_dir = self.dir / "Release" / "motioninput_server.dist"
        self.dest_dir = self.release_dir / "MotionInputServer"

    def preBuild(self):
        print("Installing requirements..")
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
            cwd=self.dir,
            shell=True,
        )

    def build(self):
        print("Starting build..")
        subprocess.run(
            [sys.executable, "build.py", "motioninput_server.py"], cwd=self.dir, shell=True
        )

    def postBuild(self):
        print("Copying build files to final destination...")

        try:
            shutil.rmtree(str(self.dest_dir))
        except OSError:
            pass

        shutil.copytree(str(self.build_dir), str(self.dest_dir))

        print("Copied build files to final destination")

    def fullBuild(self):
        self.preBuild()
        self.build()
        self.postBuild()


class WebExtension(Build):
    def __init__(self) -> None:
        super().__init__()
        self.dir = self.src_dir / "motion-input-web-extension"
        self.build_dir = self.dir / "build"
        self.dest_dir = self.release_dir / "MotionInputWebExtension"

    def preBuild(self):
        print("Installing requirements..")
        subprocess.run(["npm", "i"], cwd=self.dir, shell=True)

    def build(self):
        print("Starting build..")
        subprocess.run(["npm", "run", "build"], cwd=self.dir, shell=True)

    def postBuild(self):
        print("Copying build files to final destination...")

        presigned_xpi = self.dir / "MotionInputWebExtension.xpi"
        if Path.exists(presigned_xpi):
            print("Mozilla signed XPI already exists. Using that instead")
            shutil.copy(presigned_xpi, self.dest_dir.parent)
            return

        try:
            shutil.rmtree(str(self.dest_dir))
        except OSError:
            pass

        shutil.copytree(str(self.build_dir), str(self.dest_dir))

        print("Copied build files to final destination")

    def fullBuild(self):
        self.preBuild()
        self.build()
        self.postBuild()


class HospitalUI(Build):
    def __init__(self) -> None:
        super().__init__()
        self.dir = self.src_dir / "hospital-ui"
        self.build_dir = self.dir / "build"
        self.dest_dir = self.release_dir / "HospitalUI"

    def preBuild(self):
        print("Installing requirements..")
        subprocess.run(["npm", "i"], cwd=self.dir, shell=True)

    def build(self):
        print("Starting build..")
        subprocess.run(["npm", "run", "build"], cwd=self.dir, shell=True)

    def postBuild(self):
        print("Copying build files to final destination...")

        try:
            shutil.rmtree(str(self.dest_dir))
        except OSError:
            pass

        shutil.copytree(str(self.build_dir), str(self.dest_dir))

        print("Copied build files to final destination")

        print("Copying Hospital UI launcher into final destination...")
        shutil.copy(self.dir / "Start-Hospital-Demo.exe", self.dest_dir.parent)

    def fullBuild(self):
        self.preBuild()
        self.build()
        self.postBuild()


builds: dict[str, Build] = {
    "motion_input": MotionInput(),
    "motion_input_server": MotionInputServer(),
    "web_extension": WebExtension(),
    "hospital_ui": HospitalUI(),
}

if __name__ == "__main__":
    # specify which components to build
    to_build = ["motion_input_server", "motion_input", "hospital_ui", "web_extension"]

    for name in to_build:
        builds[name].fullBuild()

    print("Build completed")
