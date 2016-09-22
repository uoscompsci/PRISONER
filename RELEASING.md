# Managing a PRISONER release

There are a number of steps which should be taken to manage a release of
PRISONER. Ideally this should get automated at some point!

## Towards a release
- Work towards a release should be in a branch following the naming convention
"vx.y.z". We use [semantic versioning](http://semver.org) to dictate version
numbers. If the scope of the branch changes (eg. a patch is becoming a minor
version), the local and remote branches should be renamed to best fit the
expected version number.

- Changes in the version are put at the top of CHANGELOG.md along with the 
(expected) release date.

## Release
- Add a blog post to the gh-pages branch under _posts/ with a summary of
the changes and the contents of the changelog for that version.

- Also on the gh-pages branch, edit getprisoner.html with the latest version
number and a link to what will be the latest release.

- Edit doc/conf.py and edit the "version" and "release" attributes with the new
version number.

- Raise a pull request to merge the in-development branch with master

- Create a new release, named "vx.y.z" using the changelog as the release notes.

- Docker Hub should automatically rebuild the prisoner and prisoner-demo images,
although it will probably take a while. If it doesn't happen, [manually trigger a
build](https://hub.docker.com/r/lhutton/prisoner/~/settings/automated-builds/)