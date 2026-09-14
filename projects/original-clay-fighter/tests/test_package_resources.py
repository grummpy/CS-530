from __future__ import annotations

from fighter.resource_paths import asset_root, data_root, resource_path, resource_root


def test_resources_resolve_from_the_package_tree() -> None:
    root = resource_root()
    assert root.name == "resources"
    assert (data_root() / "fighters" / "master_chef.yaml").is_file()
    assert (asset_root() / "characters" / "master_chef" / "manifest.json").is_file()


def test_resource_resolver_rejects_escape_paths() -> None:
    for path in ("../data", "/data", "assets/../../data"):
        try:
            resource_path(path)
        except ValueError:
            pass
        else:
            raise AssertionError(f"{path} escaped the package resource root")
