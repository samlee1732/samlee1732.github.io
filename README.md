# mainDL Lab 首页

根据提供的截图还原的静态首页，适合直接部署到 GitHub Pages。没有构建步骤，无须安装 Node.js 或任何依赖。页面不依赖第三方字体、脚本或图片服务。

## 本地查看

直接打开 `index.html`，或者在此目录执行：

```sh
python3 -m http.server 8080 --bind 127.0.0.1
```

然后访问 `http://127.0.0.1:8080`。

## 发布到 GitHub Pages

1. 创建或选择一个 GitHub 仓库。使用 GitHub Free 时，选择公开仓库。
2. 将此目录内的全部文件放到仓库根目录，确保 `index.html`、`assets/` 和 `.nojekyll` 均已提交。
3. 打开仓库 **Settings → Pages**。
4. 在 **Build and deployment → Source** 选择 **Deploy from a branch**。
5. 选择文件所在分支（通常为 `main`）和 **/(root)**，点击 **Save**。
6. 等待部署完成，使用 Settings → Pages 显示的网址访问。

个人主页可使用名为 `你的用户名.github.io` 的仓库，网址为 `https://你的用户名.github.io/`。普通项目仓库的网址为 `https://你的用户名.github.io/仓库名/`。资源全部采用相对路径，两种方式均可使用。后续修改并提交到发布分支后，GitHub Pages 会自动更新网站。

官方说明：
- https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages
- https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site

## 修改内容

- `index.html`：实验室名称、简介、导航和弹窗内容。
- `assets/styles.css`：配色、字体、间距、桌面和手机布局。
- `assets/main.js`：手机菜单、Teaching 下拉菜单和信息弹窗。

页面视觉参考用户提供的截图。中英文简介按作者新提供的个人经历更新，英文为对应译文；中文修正了“EEE → IEEE”和“2026毕业 → 2026年毕业”两处笔误，并依据作者个人站点统一了职称与学校名称。履历、论文数量及项目经历由作者提供，未做外部核实。

目前交付范围是首页。Publication 和 Team 展示作者提供的概览信息，完整论文与成员名单仍需补充；Teaching 展示《机器人学及应用》和《自动控制原理》两门课程，课程资料仍需补充。Log In 保留参考图外观，点击后明确提示成员登录暂未开放，不收集账号、密码或个人信息。真正的登录需要另行配置认证服务。

## 本项目的部署位置

- 仓库：https://github.com/samlee1732/samlee1732.github.io
- 主页：https://samlee1732.github.io/
- 发布来源：`main` 分支的仓库根目录（`/`）。

推送到 `main` 后，GitHub Pages 自动发布更新。部署进度可在仓库的 Actions 或 Settings → Pages 查看。

## 个人信息区

首页简介下方新增个人信息与联系方式，采用参考图中的逐行布局。姓名、讲师职称、机电工程学院和深圳职业技术大学的单位信息，来自作者指定的个人站点：

- http://www.senli.site/
- http://www.senli.site/index_zh.html

姓名显示为 Sen LI, Ph.D.（李森）。邮箱由作者直接提供，使用 `lisen3@szpu.edu.cn`，并让 `mailto:` 与显示地址一致。办公地址由作者直接提供，为“深圳职业技术大学西丽校区厚德楼4楼”，同时显示对应英文地址。未提供电话，页面没有添加电话。学校名称及职称已在简介和相关概览中同步统一。
