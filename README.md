# Kototoro Linux HiDPI（非官方构建）

使用 GitHub Actions 云端构建 Kototoro v2.4.9 的原生 Linux Compose Desktop 版本，在 **Compose LocalDensity** 中施加可调 UI 缩放，再通过 Arch Linux 的 `makepkg` 生成 CachyOS 可安装的 `.pkg.tar.zst`。

本机无需 Android SDK、JDK 或 Gradle。默认 UI 缩放 **150%**，可设置环境变量 `KOTOTORO_UI_SCALE`。

## 构建

在仓库 **Actions → Build Kototoro Linux HiDPI for Arch → Run workflow** 运行。首次提交工作流会尝试自动触发一次构建；以后手动运行。

工作流分两步：
1. Ubuntu 24.04 上用官方固定源码、上游提供的 Mihon 兼容输入及原生 Compose 发行任务，编译 Linux 桌面应用。
2. Arch Linux 容器里用 `makepkg` 制作 pacman 可安装包。

构建成功后，在对应 Actions 运行的 **Artifacts** 中下载 `Kototoro-Arch-HiDPI-v2.4.9`。解压后，在 CachyOS 上安装：

```bash
sudo pacman -U ./kototoro-compose-hidpi-2.4.9-2-x86_64.pkg.tar.zst
```

如与先前的 `kototoro-bin` 冲突，pacman 会提示替换/移除旧包。建议先备份 `~/.kototoro`。

运行和临时修改 UI 缩放：

```bash
kototoro
KOTOTORO_UI_SCALE=2.0 kototoro
KOTOTORO_UI_SCALE=1.0 kototoro
```

## 限制和安全边界

- **这是非官方构建，未在你的 KDE/Wayland 环境里实测。** UI 密度补丁对 Compose 布局生效的预期仍需实际验证，弹窗与独立窗口可能需要后续修复。
- 官方 Linux 构建依赖 Android SDK 37、Gradle、JDK 17/21 和 29 个 Mihon 兼容 JAR；全部在 GitHub 云端准备，不需要本地安装。
- 采用固定源码提交 `d9f1cdd826e3b5075885a216357b574f2f5e2484` 和官方 Windows 发行 ZIP 的 SHA-256。只从 ZIP 提取校验后的 JVM JAR，不运行 Windows 程序。
- 测试在 Xvfb 上运行，**不等于真实 GPU/Wayland 验证**。Windows 的 UI、视频超分、Mihon 插件跨平台表现仍需实机检查。
- 上游更新后须同时更新版本、源码提交、Windows 兼容 ZIP 校验值和适配补丁。
- GitHub Actions 运行时间与 Artifact 保存期受账户及仓库配置影响。

文件：
- `.github/workflows/build-kototoro.yml`：云端构建与 Arch 打包
- `patches/compose-density.patch`：原生 Compose UI 缩放修改
- `arch/PKGBUILD`：pacman 安装包
- `arch/kototoro-launcher`：启动器
- `arch/kototoro.desktop`：KDE 菜单入口

仓库不包含官方源代码或商业机密；构建时从官方 GitHub 获取固定版本。