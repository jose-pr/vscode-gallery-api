from enum import Enum, IntEnum, IntFlag
import re as re
from typing import TypedDict

__all__ = []


# https://github.com/microsoft/vscode/blob/main/src/vs/platform/extensionManagement/common/extensionManagement.ts
class SortBy(IntEnum):
    NoneOrRelevance = 0
    LastUpdatedDate = 1
    Title = 2
    PublisherName = 3
    InstallCount = 4
    PublishedDate = 10
    AverageRating = 6
    WeightedRating = 12


__all__.append(SortBy.__name__)


class SortOrder(IntEnum):
    Default = 0
    Ascending = 1
    Descending = 2


__all__.append(SortOrder.__name__)


class AssetType(str, Enum):
    Icon = "Microsoft.VisualStudio.Services.Icons.Default"
    Details = "Microsoft.VisualStudio.Services.Content.Details"
    Changelog = "Microsoft.VisualStudio.Services.Content.Changelog"
    Manifest = "Microsoft.VisualStudio.Code.Manifest"
    VSIX = "Microsoft.VisualStudio.Services.VSIXPackage"
    License = "Microsoft.VisualStudio.Services.Content.License"
    Repository = "Microsoft.VisualStudio.Services.Links.Source"

    def mimetype(self):
        match self:
            case AssetType.Icon:
                return "image/png"
            case AssetType.Details:
                return "text/markdown"
            case AssetType.Changelog:
                return "text/markdown"
            case AssetType.Manifest:
                return "application/json"
            case AssetType.VSIX:
                return "application/zip"
            case _:
                return None


__all__.append(AssetType.__name__)


class PropertyType(str, Enum):
    Dependency = "Microsoft.VisualStudio.Code.ExtensionDependencies"
    ExtensionPack = "Microsoft.VisualStudio.Code.ExtensionPack"
    Engine = "Microsoft.VisualStudio.Code.Engine"
    PreRelease = "Microsoft.VisualStudio.Code.PreRelease"
    LocalizedLanguages = "Microsoft.VisualStudio.Code.LocalizedLanguages"
    WebExtension = "Microsoft.VisualStudio.Code.WebExtension"


__all__.append(PropertyType.__name__)


# https://github.com/microsoft/vscode/blob/main/src/vs/platform/extensionManagement/common/extensionGalleryService.ts


class GalleryExtensionFile(TypedDict):
    assetType: AssetType
    source: str


__all__.append(GalleryExtensionFile.__name__)


class GalleryExtensionProperty(TypedDict):
    key: PropertyType
    value: str


__all__.append(GalleryExtensionProperty.__name__)


class _Empty:
    ...


_EMPTY = _Empty()


class GalleryExtensionVersion(TypedDict):
    version: str
    lastUpdated: str
    assetUri: str
    fallbackAssetUri: str
    files: list[GalleryExtensionFile]
    properties: list[GalleryExtensionProperty]
    targetPlatform: str
    flags: str

    def get_asset(version: "GalleryExtensionVersion", type: AssetType, default=_EMPTY):  # type: ignore
        for asset in version["files"]:
            if asset["assetType"] == type:
                return asset
        if default is _EMPTY:
            raise KeyError(type)
        return default

    def get_asset_uri(version: "GalleryExtensionVersion", type: AssetType, default=_EMPTY):  # type: ignore
        return f"{version['assetUri']}/{type}"

    def get_property(version: "GalleryExtensionVersion", name: PropertyType, default=_EMPTY):  # type: ignore
        for property in version["properties"]:
            if property["key"] == name:
                return property["value"]
        if default is _EMPTY:
            raise KeyError(name)
        return default


__all__.append(GalleryExtensionVersion.__name__)


class GalleryExtensionStatistics(TypedDict):
    statisticName: str
    value: float


__all__.append(GalleryExtensionStatistics.__name__)


class GalleryExtensionPublisher(TypedDict):
    displayName: str
    publisherId: str
    publisherName: str
    domain: str
    isDomainVerified: bool


__all__.append(GalleryExtensionPublisher.__name__)


class InstallationTargets(str, Enum):
    VSCode = "Microsoft.VisualStudio.Code"


__all__.append(InstallationTargets.__name__)


class InstallationTarget(TypedDict):
    target: str
    targetVersion: str


__all__.append(InstallationTarget.__name__)


class GalleryExtension(TypedDict):
    extensionId: str
    extensionName: str
    displayName: str
    shortDescription: str
    publisher: GalleryExtensionPublisher
    versions: "list[GalleryExtensionVersion]"
    statistics: "list[GalleryExtensionStatistics]"
    tags: "list[str]"
    releaseDate: str
    publishedDate: str
    lastUpdated: str
    categories: "list[str]"
    flags: str
    installationTargets: "list[InstallationTarget]"

    def get_statistic(
        extension: "GalleryExtension", name: str, default=_EMPTY
    ):  # type:ignore
        for stat in extension["statistics"]:
            if name == stat["statisticName"]:
                return stat["value"]

        if default is _Empty:
            raise KeyError(name)
        return default

    def get_version(
        extension: "GalleryExtension", semver: str = None, default=_EMPTY
    ):  # type:ignore
        latest = None
        for version in extension["versions"]:
            _semver = version["version"]
            if _semver == semver:
                return version
            elif semver is None:
                if latest is None or latest["version"] < _semver:
                    latest = version
        if latest:
            return latest

        if default is _Empty:
            raise KeyError(semver)
        return default


__all__.append(GalleryExtension.__name__)


class GalleryExtensionQueryResultMetadataItem(TypedDict):
    name: str
    count: float


__all__.append(GalleryExtensionQueryResultMetadataItem.__name__)


# Inline in source code
class GalleryExtensionQueryResultMetadata(TypedDict):
    metadataType: str
    metadataItems: "list[GalleryExtensionQueryResultMetadataItem]"


__all__.append(GalleryExtensionQueryResultMetadata.__name__)


# Inline in source code
class GalleryExtensionQueryResult(TypedDict):
    extensions: "list[GalleryExtension]"
    resultMetadata: "list[GalleryExtensionQueryResultMetadata]"


__all__.append(GalleryExtensionQueryResult.__name__)


class GalleryQueryResult(TypedDict):
    results: "list[GalleryExtensionQueryResult]"


__all__.append(GalleryQueryResult.__name__)


class GalleryFlags(IntFlag):
    # None is used to retrieve only the basic extension details.
    NONE = 0x0
    # IncludeVersions will return version information for extensions returned
    IncludeVersions = 0x1
    # IncludeFiles will return information about which files were found
    # within the extension that were stored independent of the manifest.
    # When asking for files, versions will be included as well since files
    # are returned as a property of the versions.
    # These files can be retrieved using the path to the file without
    # requiring the entire manifest be downloaded.
    IncludeFiles = 0x2
    # Include the Categories and Tags that were added to the extension definition.
    IncludeCategoryAndTags = 0x4
    # Include the details about which accounts the extension has been shared
    # with if the extension is a private extension.
    IncludeSharedAccounts = 0x8
    # Include properties associated with versions of the extension
    IncludeVersionProperties = 0x10
    # Excluding non-validated extensions will remove any extension versions that
    # either are in the process of being validated or have failed validation.
    ExcludeNonValidated = 0x20
    # Include the set of installation targets the extension has requested.
    IncludeInstallationTargets = 0x40
    # Include the base uri for assets of this extension
    IncludeAssetUri = 0x80
    # Include the statistics associated with this extension
    IncludeStatistics = 0x100
    # When retrieving versions from a query, only include the latest
    # version of the extensions that matched. This is useful when the
    # caller doesn't need all the published versions. It will save a
    # significant size in the returned payload.
    IncludeLatestVersionOnly = 0x200
    # This flag switches the asset uri to use GetAssetByName instead of CDN
    # When this is used, values of base asset uri and base asset uri fallback are switched
    # When this is used, source of asset files are pointed to Gallery service always even if CDN is available
    Unpublished = 0x1000
    # Include the details if an extension is in conflict list or not
    IncludeNameConflictInfo = 0x8000


__all__.append(GalleryFlags.__name__)


_FILTER_TOKENS = {}


class FilterType(IntEnum):
    Tag = 1
    ExtensionId = 4
    Category = 5
    ExtensionName = 7
    Target = 8
    Featured = 9
    SearchText = 10
    ExcludeWithFlags = 12

    @property
    def token(self) -> re.Pattern:
        if self not in _FILTER_TOKENS:
            if self is FilterType.SearchText:
                prefix = ""
            else:
                prefix = f"{self.name.lower()}:"
            _FILTER_TOKENS[self] = re.compile(
                r"\b" + prefix + r'("([^"]*)"|([^"]\S*))(\s+|\b|$)',
                flags=re.IGNORECASE,
            )
        return _FILTER_TOKENS[self]


__all__.append(FilterType.__name__)


class GalleryCriterium(TypedDict):
    filterType: FilterType
    value: str

    @classmethod  # type: ignore
    def parse(cls, text: str):
        filters: list[GalleryCriterium] = []
        for ty in [FilterType.Category, FilterType.Tag]:

            def collect(match: re.Match):
                filters.append(cls(filterType=ty, value=match[1]))
                return ""

            text = ty.token.sub(collect, text)
        for match in FilterType.SearchText.token.findall(text):
            filters.append(cls(filterType=FilterType.SearchText, value=match[0]))
        return filters


__all__.append(GalleryCriterium.__name__)


# From request
class GalleryExtensionQueryFilter(TypedDict):
    pageNumber: float
    pageSize: float
    pagingToken: None
    sortBy: SortBy
    sortOrder: SortOrder
    criteria: "list[GalleryCriterium]"


__all__.append(GalleryExtensionQueryFilter.__name__)


class GalleryExtensionQuery(TypedDict):
    assetTypes: "list[AssetType]"
    filters: "list[GalleryExtensionQueryFilter]"
    flags: GalleryFlags

    @staticmethod
    def create(
        query: "str | list[GalleryCriterium] | GalleryCriterium",
        page: int = 1,
        pageSize: int = 50,
        sortBy: SortBy = SortBy.NoneOrRelevance,
        sortOrder: SortOrder = SortOrder.Default,
        flags: GalleryFlags = GalleryFlags.IncludeStatistics
        | GalleryFlags.IncludeAssetUri
        | GalleryFlags.ExcludeNonValidated
        | GalleryFlags.IncludeVersionProperties
        | GalleryFlags.IncludeCategoryAndTags
        | GalleryFlags.IncludeFiles
        | GalleryFlags.IncludeVersions,
    ) -> "GalleryExtensionQuery":  # type:ignore
        return {
            "filters": [
                {
                    "criteria": [
                        {
                            "filterType": FilterType.Target,
                            "value": InstallationTargets.VSCode,
                        },
                        {"filterType": FilterType.SearchText, "value": query},
                        {
                            "filterType": FilterType.ExcludeWithFlags,
                            "value": str(GalleryFlags.Unpublished.value),
                        },
                    ]
                    if isinstance(query, str)
                    else ([query] if isinstance(query, dict) else query),
                    "pageNumber": page,
                    "pageSize": pageSize,
                    "sortBy": sortBy,
                    "sortOrder": sortOrder,
                }
            ],
            "assetTypes": [],
            "flags": flags,
        }


__all__.append(GalleryExtensionQuery.__name__)
