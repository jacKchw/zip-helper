import fire
from pathlib import Path
import zipfile
from tempfile import TemporaryDirectory
from os import remove


def delete(input, start=0, end=-1):
    inputFilePath = Path(input)
    if not inputFilePath.exists(follow_symlinks=True):
        raise Exception("File doesn't exist")

    with TemporaryDirectory() as tempDir:
        tempDirPath = Path(tempDir)
        # extract zip
        with zipfile.ZipFile(inputFilePath, "r") as zip:
            zipInfos = zip.infolist()
            zipInfos = [info for info in zipInfos if not info.is_dir()]

            if start > len(zipInfos):
                raise Exception("start index exceed")
            end = len(zipInfos) if end == -1 else end
            filteredZipInfos = [
                name
                for index, name in enumerate(zipInfos)
                if index < start or index > end
            ]
            for zipInfo in filteredZipInfos:
                zip.extract(zipInfo.filename, path=tempDirPath)

        # write in new zip file
        remove(inputFilePath)
        with zipfile.ZipFile(inputFilePath, "a") as zip:
            for zipInfo in filteredZipInfos:
                zip.write(tempDirPath / zipInfo.filename, zipInfo.filename)


if __name__ == "__main__":
    fire.Fire(delete)
