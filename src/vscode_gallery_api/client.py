from typing import Iterator
import requests
from .models import *


MARKETPLACE_API_URI = "https://marketplace.visualstudio.com/_apis"

class VSCodeGalleryClient:
    def __init__(
        self,
        api_uri: str = MARKETPLACE_API_URI,
        session: requests.Session = None,
    ) -> None:
        self.session = session or requests.Session()
        self.api_uri = api_uri.removesuffix('/')

    def extensionquery(
        self, query: GalleryExtensionQuery | str | list[GalleryCriterium] | GalleryCriterium, **kwargs
    ) -> GalleryQueryResult:
        if not (isinstance(query, dict) and "filters" in query):
            query = GalleryExtensionQuery.create(query, **kwargs)
        resp = self.session.post(
            f"{self.api_uri}/public/gallery/extensionquery",
            json=query,
            headers={"Accept": "application/json;api-version=3.0-preview.1"},
        )
        return resp.json()

    def vspackage(self, publisher: str, extension: str, version: str, chunk_size=512)->Iterator[bytes]:
        uri =  f"{self.api_uri}/public/gallery/publishers/{publisher}/vsextensions/{extension}/{version}/vspackage"
        return self.session.get(uri, stream=True).iter_content(chunk_size=chunk_size)