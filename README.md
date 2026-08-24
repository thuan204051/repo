# @thuanazura Cydia Repo

Flat APT repository for jailbroken iOS 7–9.

## Source URL

```text
https://thuan204051.github.io/repo/
```

## Packages

- PixelCore 1.4.3
- VivoFlip 1.1.6

## Publish on GitHub

1. Create the public repository `thuan204051/repo`.
2. Upload all files from this directory to the repository root, including `.nojekyll` and `.github/`.
3. Open **Settings → Pages** in GitHub.
4. Under **Build and deployment**, select **GitHub Actions**.
5. Push/commit once more if the Pages workflow has not started.
6. Wait for the **Deploy Cydia repository to GitHub Pages** action to finish.
7. Add `https://thuan204051.github.io/repo/` in Cydia → Sources.

## Add or update a DEB

Copy the file into `debs/`, then run:

```sh
./update_repo.sh
```

Commit the changed `Packages`, compressed indexes and `Release`.

## Notes for legacy iOS

GitHub Pages uses HTTPS/TLS. iOS 7–9 devices may require current root certificates or a TLS compatibility fix.
