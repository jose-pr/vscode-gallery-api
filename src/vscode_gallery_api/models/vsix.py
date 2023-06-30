from typing import TypedDict
from zipfile import ZipFile
import xmltodict

from .gallery import *

Identity = TypedDict(
    "Identity", {"@Language": str, "@Version": str, "@Publisher": str, "@Id": str}
)
Property = TypedDict("Property", {"@Id": str, "@Value": str})


class Properties(TypedDict):
    Property: "list[Property]"


TextNode = TypedDict("TextNode", {"#text": str})


class Metadata(TypedDict):
    Identity: Identity
    DisplayName: str
    Description: TextNode
    Tags: str
    Categories: str
    GalleryFlags: str
    Badges: str
    Properties: Properties
    Icon: str


InstallationTarget = TypedDict("InstallationTarget", {"@Id": str})


class Installation(TypedDict):
    InstallationTarget: InstallationTarget


Asset = TypedDict("Asset", {"@Type": str, "@Path": str, "@Addressable": bool})


class Assets(TypedDict):
    Asset: "list[Asset]"


PackageManifest = TypedDict(
    "PackageManifest",
    {
        "@Version": str,
        "Metadata": Metadata,
        "Installation": Installation,
        "Dependencies": str,
        "Assets": Assets,
    },
)


class PackageManifest(PackageManifest):
    def into_gallery_extension(manifest: "PackageManifest"):  # type:ignore
        ext: GalleryExtension = {}
        ext["categories"] = manifest["Metadata"]["Categories"].split(",")
        ext["displayName"] = manifest["Metadata"]["DisplayName"]
        ext["extensionName"] = manifest["Metadata"]["Identity"]["@Id"]
        ext["flags"] = manifest["Metadata"]["GalleryFlags"].lower()
        ext["publisher"] = {}
        ext["publisher"]["displayName"] = ext["publisher"]["publisherName"] = manifest[
            "Metadata"
        ]["Identity"]["@Publisher"]
        ext["shortDescription"] = manifest["Metadata"]["Description"]["#text"]
        ext["tags"] = manifest["Metadata"]["Tags"].split(",")
        ext["installationTargets"] = [
            {
                "target": manifest["Installation"]["InstallationTarget"]["@Id"],
                "targetVersion": "",
            }
        ]
        ver: GalleryExtensionVersion = {}
        ver["flags"] = ext["flags"]
        ver["files"] = [
            {"assetType": asset["@Type"], "source": asset["@Path"]}
            for asset in manifest["Assets"]["Asset"]
        ]
        ver["properties"] = [
            {"key": prop["@Id"], "value": prop["@Value"]}
            for prop in manifest["Metadata"]["Properties"]["Property"]
        ]
        ver["version"] = manifest["Metadata"]["Identity"]["@Version"]
        ext["versions"] = [ver]

        return ext


class PackageManifestRoot(TypedDict):
    PackageManifest: PackageManifest

    @staticmethod  # type: ignore
    def deserialize(src: "str") -> "PackageManifestRoot":
        return xmltodict.parse(src)

    @classmethod  # type:ignore
    def from_vsix(cls, vsix: "str|ZipFile") -> "PackageManifestRoot":
        if isinstance(vsix, ZipFile):
            return cls.deserialize(vsix.read("extension.vsixmanifest").decode())
        else:
            with ZipFile(vsix, mode="r") as vsix:
                return cls.from_vsix(vsix)
