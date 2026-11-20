# Kototoro Linux HiDPI（非官方构建）

这是 Kototoro 官方 Linux Compose Desktop 应用的非官方 Arch/CachyOS 构建。它在 Compose `LocalDensity` 中加入可调 UI 缩放，默认 150%，并通过 GitHub Actions 云端编译和 `makepkg` 生成 pacman 包。

本机无需 Android SDK、JDK 或 Gradle。

## 日常安装与升级

首次或每次有新包时：
1. 打开本仓库 **Actions**。
2. 选择 **Build Kototoro Linux HiDPI for Arch**，点击 **Run workflow**。如果是上游自动更新 PR，先在分支下拉框选择 `automation/update-kototoro-release`。
3. 等待两个 Job 都成功：Linux 编译/测试、Arch makepkg 打包。
4. 从该次运行的 **Artifacts** 下载 `Kototoro-Arch-HiDPI`，解压 ZIP。
5. 在 CachyOS 运行：
   ```bash
   sudo pacman -U ./kototoro-compose-hidpi-版本号-1-x86_64.pkg.tar.zst
   ```

pacman 会升级现有 `kototoro-compose-hidpi`，通常不需要先卸载旧版本。升级前建议备份 `~/.kototoro`。

## 自动检查上游更新

`.github/workflows/check-upstream.yml` 每天检查一次 Kototoro 官方 GitHub Releases。发现新版本时会：
- 验证官方 Windows x64 ZIP 的 SHA-256（用于准备 Mihon JVM 兼容运行时）；
- 解析 release tag 对应的源码 commit；
- 更新 `.github/upstream.env` 和 Arch PKGBUILD 版本；
- 创建/更新一个 `automation/update-kototoro-release` PR。

**更新采用人工审核，不会自动发布或覆盖你正在用的版本。** 打开 PR 后，在 Actions 页面手动运行构建工作流，并选择更新分支。两个构建 Job 成功后再合并 PR。合并到 main 后，再从 main 运行一次构建并安装 Artifact。

GitHub 默认不会让由 `GITHUB_TOKEN` 创建的 PR 自动触发其他 Actions 工作流，因此这里不假装 PR 一创建就已经验证。若你以后配置专用 PAT/应用令牌，可以再启用 PR 自动构建。

也可以在 **Actions → Check Kototoro upstream releases → Run workflow** 手动检查上游是否有新版本。

## UI 缩放

默认 150%。运行时可以临时调整：
```bash
KOTOTORO_UI_SCALE=2.0 kototoro
KOTOTORO_UI_SCALE=1.0 kototoro
```

## 维护说明与限制

- 固定源码版本和官方兼容 ZIP 校验值；若上游重构导致补丁不再适用，构建会失败，必须人工更新 `patches/compose-density.patch`。
- 构建包含 Xvfb 下的 Linux 自动化测试，不等于真实 KDE/Wayland/GPU 实机测试。
- Mihon 兼容输入取自官方 Windows x64 ZIP 中的 JVM 兼容文件；本构建不运行 Windows 程序。
- 这是非官方构建。Kototoro 上游更新可能改变依赖、构建参数或 UI 结构，不能保证自动适配。
- GitHub Actions Artifacts 有保留期限；请在到期前下载需要的安装包。
