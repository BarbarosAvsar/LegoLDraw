import os
import sys

import bpy


class DummyContext:
    def report(self, _types, message):
        print(message)


def main():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.append(repo_root)

    from loadldraw import loadldraw

    test_root = os.path.abspath(os.path.dirname(__file__))
    sample_path = os.path.join(test_root, "data", "sample.ldr")
    ldraw_path = os.path.join(test_root, "ldraw")

    loadldraw.Options.ldrawDirectory = ldraw_path
    loadldraw.Options.useColourScheme = "ldraw"
    loadldraw.Options.useUnofficialParts = False
    loadldraw.Options.useLogoStuds = False
    loadldraw.Options.useLSynthParts = False
    loadldraw.Options.addEnvironment = False
    loadldraw.Options.addGroundPlane = False
    loadldraw.Options.positionCamera = False
    loadldraw.Options.verbose = 0

    dummy_context = DummyContext()
    root_obj = loadldraw.loadFromFile(dummy_context, sample_path)
    if root_obj is None:
        raise SystemExit("Import failed: root object is None")

    print("Import succeeded", root_obj.name)


if __name__ == "__main__":
    main()
