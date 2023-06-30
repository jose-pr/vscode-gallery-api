from vscode_gallery_api.client import VSCodeGalleryClient
from vscode_gallery_api.models import *


def test_get_extension():
    client = VSCodeGalleryClient()
    response = client.extensionquery(
        {"filterType": FilterType.ExtensionName, "value": "ms-python.python"},
        pageSize=1,
    )
    extension = response["results"][0]["extensions"][0]
    latest = GalleryExtension.get_version(extension)
    icon = GalleryExtensionVersion.get_asset(latest, AssetType.Icon)
    engine = GalleryExtensionVersion.get_property(latest, PropertyType.Engine)
    print(latest["version"])
    pass


if __name__ == "__main__":
    test_get_extension()
