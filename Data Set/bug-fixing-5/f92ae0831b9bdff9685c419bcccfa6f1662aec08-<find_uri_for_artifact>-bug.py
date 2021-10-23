def find_uri_for_artifact(self, artifact):
    if (artifact.version == 'latest'):
        artifact.version = self.find_latest_version_available(artifact)
    if artifact.is_snapshot():
        path = ('/%s/maven-metadata.xml' % artifact.path())
        xml = self._request((self.base + path), 'Failed to download maven-metadata.xml', (lambda r: etree.parse(r)))
        timestamp = xml.xpath('/metadata/versioning/snapshot/timestamp/text()')[0]
        buildNumber = xml.xpath('/metadata/versioning/snapshot/buildNumber/text()')[0]
        for snapshotArtifact in xml.xpath('/metadata/versioning/snapshotVersions/snapshotVersion'):
            if ((len(snapshotArtifact.xpath('classifier/text()')) > 0) and (snapshotArtifact.xpath('classifier/text()')[0] == artifact.classifier) and (len(snapshotArtifact.xpath('extension/text()')) > 0) and (snapshotArtifact.xpath('extension/text()')[0] == artifact.extension)):
                return self._uri_for_artifact(artifact, snapshotArtifact.xpath('value/text()')[0])
        return self._uri_for_artifact(artifact, artifact.version.replace('SNAPSHOT', ((timestamp + '-') + buildNumber)))
    return self._uri_for_artifact(artifact, artifact.version)